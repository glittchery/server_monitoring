from src.api.monitors import monitors_router
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




