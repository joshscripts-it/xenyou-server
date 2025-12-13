from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.routers import auth
from app.db.session import create_db_and_tables


# from app.api.v1 import search  # new

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    print("Xenyou Server is starting up...")
    await create_db_and_tables()
    yield
    # shutdown code
    print("Xenyou Server is shutting down...")


app = FastAPI(lifespan=lifespan)


# create tables at startup (dev convenience)
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])


@app.get("/")
def root():
    return {"message": "Welcome To XenYou! 🚀"}
