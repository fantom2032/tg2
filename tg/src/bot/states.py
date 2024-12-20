# Aiogram
from aiogram.fsm.state import State, StatesGroup


class ExchangeStates(StatesGroup):
    action_request = State()
    currency_request = State()
    exchange_currency = State()
    wait_sum = State()



