from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from models import Base
from database import engine
from routes_auth import router as auth_router

# Crea le tabelle del database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurazione CORS - permettiamo tutte le origini per il test
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Usiamo la lista delle origini consentite
    allow_credentials=True,
    allow_methods=["*"],  # Permettiamo tutti i metodi
    allow_headers=["*"],  # Permettiamo tutti gli headers
)

# Monta le routes per l'autenticazione
app.include_router(auth_router)

# Configurazione per servire i file statici
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/{filename:path}")
async def serve_static(filename: str):
    file_path = os.path.join(frontend_path, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(frontend_path, "index.html"))