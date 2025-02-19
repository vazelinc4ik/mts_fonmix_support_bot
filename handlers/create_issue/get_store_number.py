from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext


from constants import (
    GET_TV_INFO_MESSAGE,
    GET_TV_INFO_WITH_PREVIOUS_MESSAGE,
    INCORRECT_STORE_CODE_MESSAGE,
    KEEP_DATA_BUTTONS
)
from core import CreateIssueState
from crud import StoresCRUD
from models import Stores
from utils import generate_kb

router = Router()


@router.message(CreateIssueState.get_store_number)
@router.message(F.text.lower()=='изменить телевизор', CreateIssueState.end_state)
@router.message(F.text.lower()=='назад', CreateIssueState.get_description)
async def get_store_number(message: Message, state: FSMContext):
    
    if await state.get_state() == CreateIssueState.get_store_number and message.text.lower() != "оставить прежнее значение":
        store_code = message.text.upper()
    else:
        store_code = (await state.get_data())["store"].code
        
    store: Stores = await StoresCRUD.find_one_or_none(code=store_code)
    
    if store:
        await state.update_data(store=store)
        user_data = await state.get_data()
        tv_names = [tv.name for tv in store.tv_details]
        
        if user_data.get("tv_info"):
            adj = [2 for _ in range(0, len(tv_names), 2)]
            adj.append(1)
            tv_names.extend(KEEP_DATA_BUTTONS)
            prev_name = user_data.get("tv_info").name
            await message.answer(
                text=GET_TV_INFO_WITH_PREVIOUS_MESSAGE.format(prev_name),
                reply_markup=generate_kb(tv_names, adj, statement_kb=True)
            )
        else:
            await message.answer(
                text=GET_TV_INFO_MESSAGE,
                reply_markup=generate_kb(buttons=tv_names, adjustment=2, statement_kb=True)
            )
        await state.set_state(CreateIssueState.get_tv_name)
        return
    
    await message.answer(
        text=INCORRECT_STORE_CODE_MESSAGE
    )