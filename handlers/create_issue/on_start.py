from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext


from constants import (
    KEEP_DATA_BUTTONS,
    GET_STORE_INFO_MESSAGE,
    GET_STORE_INFO_WITH_PREVIOUS_MESSAGE
)
from core import CreateIssueState
from utils import generate_kb

router = Router()


@router.message(F.text.lower()=='создать новое обращение')
@router.message(F.text.lower()=='изменить магазин', CreateIssueState.end_state)
@router.message(F.text.lower()=='назад', CreateIssueState.get_tv_name)
async def on_start(message: Message, state: FSMContext):
    if message.text.lower() in ['назад', 'изменить магазин']:
        user_data = await state.get_data()
        prev_store_code = user_data.get("store").code
        await message.answer(
            text=GET_STORE_INFO_WITH_PREVIOUS_MESSAGE.format(prev_store_code),
            reply_markup=generate_kb(KEEP_DATA_BUTTONS, statement_kb=True)
        )
    else:
        await message.answer(
            text=GET_STORE_INFO_MESSAGE,
            reply_markup=ReplyKeyboardRemove()
        )
        
    await state.set_state(CreateIssueState.get_store_number)
    