from aiogram import Router
from .commands import router as cmd_router
from .create_issue import router as fsm_router
from .operator import router as op_router

router = Router()

router.include_router(cmd_router)
router.include_router(fsm_router)
router.include_router(op_router)