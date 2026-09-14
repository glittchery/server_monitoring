from src.api.monitors import monitors_router
from src.api.checks import checks_router
from src.api.auth import auth_router
from fastapi import FastAPI
from src.database.queries import OrmQueries
from contextlib import asynccontextmanager
# import os
# import sys
import asyncio
# sys.path.insert(1, os.path.join(sys.path[0], '..'))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await OrmQueries.create_tables()
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(monitors_router)
app.include_router(checks_router)
app.include_router(auth_router)






