from src.api.monitors import monitors_router
from fastapi import FastAPI
from src.database.queries import OrmQueries
import os
import sys
import asyncio
sys.path.insert(1, os.path.join(sys.path[0], '..'))

app = FastAPI()
app.include_router(monitors_router)


OrmQueries.create_tables()

