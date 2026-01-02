from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.routers import auth
from app.api.v1.routers import search
from app.db.session import create_db_and_tables
from app.api.v1.routers import hostels
from app.api.v1.routers.interactions import router as interactions_router
from app.api.v1.routers import recommend


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
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(hostels.router, prefix="/api/v1/hostels")
app.include_router(
    interactions_router, prefix="/api/v1/interactions", tags=["interactions"]
)
app.include_router(recommend.router, prefix="/api/v1/recommend", tags=["recommend"])


@app.get("/")
def root():
    return {"message": "Welcome To XenYou! 🚀"}
