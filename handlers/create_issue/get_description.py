from aiogram import Router, F
from aiogram.types import (
    Message,
    InputMediaPhoto
)
from aiogram.fsm.context import FSMContext


from constants import (
    GET_ISSUE_PHOTOS_MESSAGE,
    PREVIOUS_PHOTO_MESSAGE,
    KEEP_DATA_BUTTONS,
    SKIP_BUTTONS
)
from core import CreateIssueState
from crud import TVDetailsCRUD

from utils import generate_kb

router = Router()

@router.message(CreateIssueState.get_description)
@router.message(F.text.lower()=='изменить фото', CreateIssueState.end_state)
@router.message(F.text.lower()=='назад', CreateIssueState.get_videos)
async def get_description(message: Message, state: FSMContext):
    if await state.get_state() == CreateIssueState.get_description and message.text.lower() != "оставить прежнее значение":
        description = message.text
        await state.update_data(description=description)
        
    user_data = await state.get_data()
    if user_data.get('photo_ids'):
        photo_ids = user_data.get('photo_ids')
        media = [InputMediaPhoto(media=photo_id) for photo_id in photo_ids]
        
        await state.update_data(old_photos=True)
        await message.answer_media_group(media=media)
        await message.answer(
            text=PREVIOUS_PHOTO_MESSAGE,
            reply_markup=generate_kb(KEEP_DATA_BUTTONS, statement_kb=True)
        )
    else:
        await message.answer(
            text=GET_ISSUE_PHOTOS_MESSAGE,
            reply_markup=generate_kb(SKIP_BUTTONS, adjustment=1, statement_kb=True)
        )

    await state.set_state(CreateIssueState.get_photos)
    
