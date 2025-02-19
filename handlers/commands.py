from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants import (
    START_MESSAGE, 
    ON_START_BUTTONS
)
from utils import generate_kb


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=START_MESSAGE,
        reply_markup=generate_kb(
            buttons=ON_START_BUTTONS,
            adjustment=[1, 2]
        )
    )
    

    
    
    