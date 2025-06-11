from aiogram.fsm.state import StatesGroup, State

class ChannelsStates(StatesGroup):
    channels = State()
    channel = State()
    add_channel = State()
    