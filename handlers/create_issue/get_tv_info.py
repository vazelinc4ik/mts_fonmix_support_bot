from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext


from constants import (
    GET_DESCRIPTION_INFO_MESSAGE,
    GET_DESCRIPTION_INFO_WITH_PREVIOUS_MESSAGE,
    INCORRECT_TV_NAME_MESSAGE,
    KEEP_DATA_BUTTONS
)
from core import CreateIssueState
from crud import TVDetailsCRUD

from utils import generate_kb

router = Router()

@router.message(CreateIssueState.get_tv_name)
@router.message(F.text.lower()=='изменить описание', CreateIssueState.end_state)
@router.message(F.text.lower()=='назад', CreateIssueState.get_photos)
async def get_tv_info(message: Message, state: FSMContext):
    if await state.get_state() == CreateIssueState.get_tv_name and message.text.lower() != "оставить прежнее значение":        
        tv_name = message.text
    else:
        tv_name = (await state.get_data())["tv_info"].name
        
    data = await state.get_data()
    store = data.get("store")
    
    data = {
        "store_id": store.id,
        "name": tv_name
    }
    
    tv_info = await TVDetailsCRUD.find_one_or_none(**data)
    
    if tv_info:
        user_data = await state.get_data()
        await state.update_data(tv_info=tv_info)
        
        if user_data.get("description"):
            description = user_data.get("description")
            await message.answer(
                text=GET_DESCRIPTION_INFO_WITH_PREVIOUS_MESSAGE.format(description),
                reply_markup=generate_kb(KEEP_DATA_BUTTONS, statement_kb=True)
            )
        else:
            await message.answer(
                text=GET_DESCRIPTION_INFO_MESSAGE,
                reply_markup=generate_kb([], statement_kb=True)
            )
            
        await state.set_state(CreateIssueState.get_description)
        return
    
    tv_names = await TVDetailsCRUD.find_all_names_by_store_id(store.id)
    
    await message.answer(
        text=INCORRECT_TV_NAME_MESSAGE,
        reply_markup=generate_kb(buttons=tv_names, adjustment=2, statement_kb=True)
    )
    