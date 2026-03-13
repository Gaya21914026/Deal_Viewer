from fastapi import FastAPI
from deal_viewer.config.database import  database
from deal_viewer.routes.health_check import router as health_check_router
from deal_viewer.routes.deal_router import router as deal_router
from deal_viewer.routes.template_router import router as template_router
from deal_viewer.routes.get_deal import router as get_deal_router


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.database=database


BASE_DIR = Path(__file__).resolve().parents[3]
FRONT_DIR = BASE_DIR / "front"


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# servir les fichiers front
app.mount("/front", StaticFiles(directory=FRONT_DIR), name="front")

# page principale
@app.get("/")
def frontend():
    return FileResponse(FRONT_DIR / "index.html")


app.include_router(health_check_router)
app.include_router(deal_router)
app.include_router(template_router)
app.include_router(get_deal_router, prefix="/get-deal", tags=["Get-deal"])