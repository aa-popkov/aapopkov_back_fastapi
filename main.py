import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_v1 import api_v1_router
from utils.config import config, ModeType
from utils.startup import on_startup

description = """
# Backend API
## API Documentation
- Site - [https://aapopkov.su/](aapopkov.su)
- GIT - [https://github.com/aa-popkov/](https://github.com/aa-popkov)
"""

app = FastAPI(
    title="AAPopkov API",
    description=description,
    openapi_url=None if config.APP_MODE == ModeType.prod else "/openapi.json",
    docs_url=None if config.APP_MODE == ModeType.prod else "/docs",
    redoc_url=None,
)

app.include_router(router=api_v1_router)

origins = ["https://aa-popkov.github.io", "95.139.197.164"]
if config.APP_MODE == ModeType.dev:
    origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    asyncio.run(on_startup())
    uvicorn.run(app=app, host="0.0.0.0", port=8000, proxy_headers=True, forwarded_allow_ips="*")
