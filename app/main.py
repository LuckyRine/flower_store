from contextlib import asynccontextmanager
from typing import Any

from aiormq import auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base
from app.database.sesion import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Helen Flowers API",
                  description="Backend API for flower shop - catalog, auth, order, payments, notifications",
                  debug=False,
                  lifespan=lifespan)

    app.add_middleware(CORSMiddleware,
                       allow_origins=["*"],
                       allow_methods=["*"],
                       allow_headers=["*"],
                       allow_credentials=True)

    # app.include_router(auth.router)

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {"message": "Hello World"}

    return app

create_app()