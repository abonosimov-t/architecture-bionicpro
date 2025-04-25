from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.reports import router as api_v1_router
from app.config import settings
from app.core.security import fetch_keycloack_public_hey


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.KEYCLOAK_PUBLIC_KEY = await fetch_keycloack_public_hey(
        settings.KEYCLOAK_URL, settings.KEYCLOAK_REALM
    )
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
