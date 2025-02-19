from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    InputMediaVideo
)
from aiogram.fsm.context import FSMContext

from constants import (
    GET_ISSUE_VIDEOS_MESSAGE,
    ON_PHOTO_UPLOAD_MESSAGE,
    PREVIOUS_VIDEO_MESSAGE,
    KEEP_DATA_BUTTONS,
    SKIP_BUTTONS
)
from core import CreateIssueState
from utils import generate_kb

router = Router()

@router.message(F.media_group_id, CreateIssueState.get_photos)
async def get_photos_album(message: Message, state: FSMContext, album: list[Message]):
    user_data = await state.get_data()
    for msg in album:
        if msg.photo:
            if "photo_ids" not in user_data or user_data.get("old_photos"):
                user_data["photo_ids"] = []
                user_data["old_photos"] = False
            user_data["photo_ids"].append(msg.photo[-1].file_id)
    await state.update_data(user_data)
    await message.answer(
        text=ON_PHOTO_UPLOAD_MESSAGE,
        reply_markup=generate_kb(SKIP_BUTTONS, adjustment=1, statement_kb=True)
    )

@router.message(CreateIssueState.get_photos)
@router.message(F.text.lower()=='назад', CreateIssueState.get_contacts)
@router.message(F.text.lower()=='изменить видео', CreateIssueState.end_state)
async def get_photo(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.photo:
        if "photo_ids" not in user_data or user_data.get("old_photos"):
            user_data["photo_ids"] = []
            user_data["old_photos"] = False
        user_data["photo_ids"].append(message.photo[-1].file_id)
        await state.update_data(user_data)
        await message.answer(
            text=ON_PHOTO_UPLOAD_MESSAGE,
            reply_markup=generate_kb(SKIP_BUTTONS, adjustment=1, statement_kb=True)
        )
        
    elif (
        message.text.lower() == "далее" or 
        message.text.lower() == "оставить прежнее значение" or 
        message.text.lower() == 'назад' or 
        message.text.lower() == "изменить видео"
    ):
        if user_data.get('video_ids'):
            video_ids = user_data.get('video_ids')
            media = [InputMediaVideo(media=video_id) for video_id in video_ids]
                    
            await state.update_data(old_videos=True)
            await message.answer_media_group(media=media)
            await message.answer(
                text=PREVIOUS_VIDEO_MESSAGE,
                reply_markup=generate_kb(KEEP_DATA_BUTTONS, statement_kb=True)
            )
        else:
            await message.answer(
                text=GET_ISSUE_VIDEOS_MESSAGE,
                reply_markup=generate_kb(SKIP_BUTTONS, adjustment=1, statement_kb=True)
            )
        await state.set_state(CreateIssueState.get_videos)


