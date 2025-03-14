from .create_handler import router as create_router
from .handler import base_router

routers = [
    create_router,
    base_router,
]