from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    users = State()
    user = State()
    change_user_role = State()
    add_user = State()
    user_not_found = State()
    