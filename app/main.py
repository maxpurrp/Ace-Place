from fastapi import FastAPI
from .router import Router

import logging
from logging.handlers import RotatingFileHandler


handler = RotatingFileHandler('my_log.log', maxBytes=2000, backupCount=10)
logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s] %(levelname)s: %(message)s",
                    datefmt='%Y/%m/%d %H:%M:%S', handlers=[handler])

app = FastAPI()
router = Router()
app.include_router(router.router)
