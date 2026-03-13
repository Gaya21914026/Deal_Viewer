from fastapi import APIRouter

router = APIRouter(prefix="/health-check", tags=["Health-check"])

@router.get("/")
def health_check():
    return {"ping": "pong"}