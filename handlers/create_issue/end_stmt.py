import os
from aiogram import Router, F
from aiogram.types import (
    Message,
)
from aiogram.fsm.context import FSMContext


from constants import (
    CONFIRM_BUTTONS,
    CHANGE_ISSUE_DATA_BUTTONS,
    EDIT_ISSUE_MESSAGE,
    ISSUE_CREATED_MESSAGE,
    ON_START_BUTTONS,

)
from core import CreateIssueState, jira
from utils import (
    create_issue_data,
    generate_kb,
)

router = Router()

@router.message(F.text.lower() == "отправить", CreateIssueState.end_state)
async def confirm(message: Message, state: FSMContext):
    user_data = await state.get_data()
    issue_data = create_issue_data(user_data)
    issue = jira.create_issue(fields=issue_data)
    
    photo_ids = user_data.get("photo_ids", [])
    video_ids = user_data.get("video_ids", [])
    
    if photo_ids or video_ids:
        await message.answer(
            text="К Вашему обращению прикрепляются загруженные медиа. Пожалуйста ожидайте."
        )
    
    for photo_id in photo_ids:
        file = await message.bot.get_file(photo_id)
        photo_path = f"temp_photos/{photo_id}.jpg"
        os.makedirs(os.path.dirname(photo_path), exist_ok=True)
        await message.bot.download_file(file.file_path, destination=photo_path)
        with open(photo_path, "rb") as file:
            jira.add_attachment(issue, file)
        os.remove(photo_path)
        
    for video_id in video_ids:
        file = await message.bot.get_file(video_id)
        video_path = f"temp_videos/{video_id}.mp4"
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        await message.bot.download_file(file.file_path, destination=video_path)
        with open(video_path, "rb") as file:
            jira.add_attachment(issue, file)
        os.remove(video_path)
        
    await message.answer(
        text=ISSUE_CREATED_MESSAGE.format(issue.key),
        reply_markup=generate_kb(ON_START_BUTTONS)
    )
        
    await state.clear()
    
@router.message(F.text.lower() == "внести изменения", CreateIssueState.end_state)
async def edit_issue(message: Message, state: FSMContext):
    await message.answer(
        text=EDIT_ISSUE_MESSAGE,
        reply_markup=generate_kb(CHANGE_ISSUE_DATA_BUTTONS, adjustment=2)
    )
    
@router.message(CreateIssueState.end_state)
async def error(message: Message, state: FSMContext):
    await message.answer(
        text="Пожалуйста выберите 1 из опций",
        reply_markup=generate_kb(CONFIRM_BUTTONS, adjustment=1)
    )