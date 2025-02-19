

from constants import BASE_DESCRIPTION

def generate_issue_description(user_data: dict):
    store = user_data.get("store")
    tv_info = user_data.get("tv_info")
    description = user_data.get("description")
    contacts = user_data.get("contacts")
    
    return BASE_DESCRIPTION.format(store.code, tv_info.point_number, description, contacts)

def create_issue_data(user_data: dict):
    description = generate_issue_description(user_data)
    return {
        "project": "SUPPORT",
        "issuetype": "FONMIX",
        "summary": "Проблема с вещанием видео, МТС",
        "description": description,
        "customfield_12548": {'value': 'Россия'},
        "customfield_12542": {'value': "Чаты"},
        "customfield_12537": {'value': "Инцидент"},
    }