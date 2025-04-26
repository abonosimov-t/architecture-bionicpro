from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "BionicPRO API"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "Report API for BionicPRO"

    API_V1_STR: str = "/api/v1"

    KEYCLOAK_URL: str = ""
    KEYCLOAK_REALM: str = ""
    KEYCLOAK_CLIENT_ID: str = ""
    KEYCLOAK_CLIENT_SECRET: str = ""
    KEYCLOAK_PUBLIC_KEY: str = ""
    KEYCLOAK_ALGORITHMS: list[str] = ["RS256"]

    class Config:
        env_file = ".env"


settings = Settings()
