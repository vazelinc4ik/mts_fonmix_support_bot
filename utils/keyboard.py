from typing import List, Union

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder



def generate_kb(
        buttons: List[str], 
        adjustment: Union[int, List[int]]=1,
        statement_kb: bool = False
        ) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    for button in buttons:
        builder.add(KeyboardButton(text=button))
    
    if statement_kb:
        builder.add(KeyboardButton(text="Назад"))
        
    if isinstance(adjustment, int):
        builder.adjust(adjustment)
    else:
        builder.adjust(*adjustment)
        
    return builder.as_markup(resize_keyboard=True)