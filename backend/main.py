from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import models

from routes.words import router as words_router
from routes.relations import router as relations_router
from routes.graph import router as graph_router
from routes.literature import router as literature_router
from routes.search import router as search_router
from routes.voice import router as voice_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Tamil Literary Intelligence Explorer",
    description="Tamil lexical and literary intelligence API",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routes
app.include_router(words_router)
app.include_router(relations_router)
app.include_router(graph_router)
app.include_router(literature_router)
app.include_router(search_router)
app.include_router(voice_router)


@app.get("/")
def root():
    return {
        "message": "Tamil Literary Intelligence Explorer API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }