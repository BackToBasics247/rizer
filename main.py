from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routes.authRoute import authRouter


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        print("Fastapi app is starting")
        yield
        print("Fastapi app is closing!")
    except Exception as e:
        raise e


app = FastAPI(root_path="/app", version="1.0.0.0", lifespan=app_lifespan)
app.include_router(authRouter)
