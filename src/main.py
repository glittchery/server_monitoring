import asyncio
from src.services.check_service import scheduler
from src.api.monitors import monitors_router
from src.api.checks import checks_router
from src.api.auth import auth_router
from fastapi import FastAPI
from src.database.queries import OrmQueries
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await OrmQueries.create_tables()
    task = asyncio.create_task(scheduler())
    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass



app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(monitors_router)
app.include_router(checks_router)







