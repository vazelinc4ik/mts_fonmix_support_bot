from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext

from constants import (
    GET_CONTACT_INFO_MESSAGE,
    GET_CONTACT_INFO_WITH_PREVIOUS_MESSAGE,
    ON_VIDEO_UPLOAD_MESSAGE,
    KEEP_DATA_BUTTONS,
    SKIP_BUTTONS
)
from core import CreateIssueState
from utils import generate_kb

router = Router()

@router.message(F.media_group_id, CreateIssueState.get_videos)
async def get_videos_album(message: Message, state: FSMContext, album: list[Message]):
    user_data = await state.get_data()
    for msg in album:
        if msg.video:
            if "video_ids" not in user_data or user_data.get("old_videos"):
                user_data["video_ids"] = []
                user_data["old_videos"] = False
            user_data["video_ids"].append(msg.video.file_id)
    await state.update_data(user_data)
    await message.answer(
        text=ON_VIDEO_UPLOAD_MESSAGE,
        reply_markup=generate_kb(SKIP_BUTTONS, adjustment=1, statement_kb=True)
    )

@router.message(CreateIssueState.get_videos)
@router.message(F.text.lower()=="изменить контактные данные", CreateIssueState.end_state)
async def get_video(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.video:
        if "video_ids" not in user_data or user_data.get("old_videos"):
            user_data["video_ids"] = []
            user_data["old_videos"] = False
        user_data["video_ids"].append(message.video.file_id)
        await state.update_data(user_data)
        await message.answer(
            text=ON_VIDEO_UPLOAD_MESSAGE,
            reply_markup=generate_kb(SKIP_BUTTONS, adjustment=1, statement_kb=True)
        )
        
    elif (
        message.text.lower() == "далее" or 
        message.text.lower() == "оставить прежнее значение" or 
        message.text.lower() == 'назад' or 
        message.text.lower() == 'изменить контактные данные'
    ):
        if user_data.get('contacts'):
            contacts = user_data.get('contacts')
            await message.answer(
                text=GET_CONTACT_INFO_WITH_PREVIOUS_MESSAGE.format(contacts),
                reply_markup=generate_kb(KEEP_DATA_BUTTONS, statement_kb=True)
            )
        else:
            await message.answer(
                text=GET_CONTACT_INFO_MESSAGE,
                reply_markup=generate_kb([], statement_kb=True)
            )
        await state.set_state(CreateIssueState.get_contacts)
