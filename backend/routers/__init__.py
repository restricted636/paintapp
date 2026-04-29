from .auth import router as user_router
from .palettes import router as palette_router
from .colors import router as color_router

__all__ = ["user_router", "palette_router", "color_router"]