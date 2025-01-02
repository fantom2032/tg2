# Aiogram
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

# Local
from src.bot.states import ExchangeStates, WheatherStates


master_router = Router()


@master_router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text="Здравствуйте, это мой тестовый бот")


@master_router.message(Command("exchange"))
async def select_currency(message: Message, state: FSMContext):
    sale = InlineKeyboardButton(text="SALE", callback_data="SALE")
    buy = InlineKeyboardButton(text="BUY", callback_data="BUY")
    markup = InlineKeyboardMarkup(inline_keyboard=[[sale], [buy]])
    await state.set_state(state=ExchangeStates.action_request)
    await message.answer(text="Выберите действие", reply_markup=markup)


@master_router.message(Command("wheather"))
async def command_wheather(message: Message, state: FSMContext):
    current = InlineKeyboardButton(
        text="current", callback_data="current"
    )
    forecast = InlineKeyboardButton(
        text="forecast", callback_data="forecast"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[current], [forecast]]
    )
    await state.set_state(
        state=WheatherStates.current_or_forecast
    )
    await message.answer(text="choose your destiny", reply_markup=markup)
