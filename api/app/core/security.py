from fastapi import Depends, HTTPException, status, Security
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
import httpx
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.exceptions import AccessVaiolation


security = HTTPBearer()


async def fetch_keycloack_public_hey(keycloak_url: str, realm: str) -> dict:
    url = f"{keycloak_url}/realms/{realm}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}/protocol/openid-connect/certs")
            response.raise_for_status()
            return response.json()["keys"][0]
    except (httpx.RequestError, KeyError) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to fetch Keycloak public key: {str(e)}",
        )


class KeycloakAuth:
    def __init__(self, settings: "Settings", roles=None) -> None:
        self.settings = settings
        self.roles = roles

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        try:
            token = credentials.credentials
            payload = jwt.decode(
                token,
                key=self.settings.KEYCLOAK_PUBLIC_KEY,
                algorithms=self.settings.KEYCLOAK_ALGORITHMS,
                audience=self.settings.KEYCLOAK_CLIENT_ID,
            )
            self.check_roles(payload)
            return payload

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        except AccessVaiolation:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access denied",
            )

    def check_roles(self, payload: dict):
        if not self.roles:
            return
        roles = payload.get("realm_access", {}).get("roles", [])
        if not any((role in roles for role in self.roles)):
            raise AccessVaiolation
