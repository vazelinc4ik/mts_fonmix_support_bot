from aiogram import Router

from .end_stmt import router as end_stmt_router
from .get_contacts import router as get_contacts_router
from .get_description import router as get_description_router
from .get_photos import router as get_photos_router
from .get_store_number import router as get_store_number_router
from .get_tv_info import router as get_tv_info_router
from .get_videos import router as get_videos_router
from .on_start import router as on_start_router

router = Router()

router.include_router(on_start_router)
router.include_router(get_store_number_router)
router.include_router(get_tv_info_router)
router.include_router(get_description_router)
router.include_router(get_photos_router)
router.include_router(get_videos_router)
router.include_router(get_contacts_router)
router.include_router(end_stmt_router)





