# Aiogram
from aiogram.fsm.state import State, StatesGroup


class ExchangeStates(StatesGroup):
    action_request = State()
    currency_request = State()
    exchange_currency = State()
    wait_sum = State()


class WheatherStates(StatesGroup):
    current_or_forecast = State()
    request_for_city = State()
    request_for_days = State()
