from fastapi import APIRouter, Depends
from app.core.security import KeycloakAuth
from app.config import settings

router = APIRouter()
auth = KeycloakAuth(settings, ['prothetic_user'])


@router.get("/reports")
async def get_reports(payload=Depends(auth)):
    return {"reports": ["report1", "report2"]}
