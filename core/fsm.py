from aiogram.fsm.state import StatesGroup, State

class CreateIssueState(StatesGroup):
    get_store_number = State()
    get_tv_name = State()
    get_description = State()
    get_photos = State()
    get_videos = State()
    get_contacts = State()
    end_state = State()
    