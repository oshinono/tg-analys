from aiogram.fsm.state import State, StatesGroup

class ModerationStates(StatesGroup):
    index = State()
    unapproved_prompts = State()
    unapproved_prompt = State()
    want_to_reject = State()