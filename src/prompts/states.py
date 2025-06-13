from aiogram.fsm.state import State, StatesGroup

class PromptStates(StatesGroup):
    prompts = State()
    prompt = State()
    prompt_action = State()
    