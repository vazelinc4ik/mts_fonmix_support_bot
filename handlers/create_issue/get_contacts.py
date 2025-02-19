import re
from aiogram import Router
from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)

from aiogram.fsm.context import FSMContext


from constants import (
    CONFIRM_BUTTONS,
    INCORRECT_CONTACT_INFO_MESSAGE,
    SUMMARY_MESSAGE,

)
from core import CreateIssueState

from utils import (
    generate_kb,

)

router = Router()

@router.message(CreateIssueState.get_contacts)
async def get_contacts(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text.lower() == "оставить прежнее значение":
        contacts = user_data.get("contacts")
    else:
        contacts = message.text
        
    pattern = r'^(\+7|8|7)\d{10}$'
    
    words = contacts.split(" ")
    for word in words:
        match = re.search(pattern, word)
        if match:
            break
    
    if not match:
        await message.answer(
            INCORRECT_CONTACT_INFO_MESSAGE,
            reply_markup=generate_kb([], statement_kb=True)
        )
        return

    await state.update_data(contacts=contacts)
    await state.set_state(CreateIssueState.end_state)
    
    user_data = await state.get_data()
    store_code = user_data.get("store").code
    tv_name = user_data.get("tv_info").name
    description = user_data.get("description")
    photos = len(user_data.get("photo_ids", []))
    videos = len(user_data.get("video_ids", []))
    
    await message.answer(
        text=SUMMARY_MESSAGE.format(store_code, tv_name, description, contacts, photos, videos),
        reply_markup=generate_kb(CONFIRM_BUTTONS, adjustment=1)
    )
