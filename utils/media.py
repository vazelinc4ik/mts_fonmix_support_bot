from typing import Dict, List, Union

from aiogram.types import Message

def proceed_msg(user_data: Dict[str, Union[str, List[str]]], msg: Message):
    if msg.photo:
        photo = msg.photo[-1]
        if "photo_ids" not in user_data:
            user_data["photo_ids"] = []
        user_data["photo_ids"].append(photo.file_id)
    if msg.video:
        if "video_ids" not in user_data:
            user_data["video_ids"] = []
        user_data["video_ids"].append(msg.video.file_id)
    if msg.text:
        user_data["description"] = msg.text
        