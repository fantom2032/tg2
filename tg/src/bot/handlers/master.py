# Aiogram
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

# Local
from src.bot.states import ExchangeStates
from src.bot.utils.rate_exchange import convert_currency

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

@master_router.message(Command("convert"))
async def convert_command(message: Message):
    await message.answer("Введите сумму и валюты для конвертации в формате: 100 USD to RUB")

@master_router.message(lambda message: message.text and len(message.text.split()) == 4)
async def handle_conversion(message: Message):
    try:
        amount, from_currency, _, to_currency = message.text.split()
        amount = float(amount)
        result = await convert_currency(amount, from_currency.upper(), to_currency.upper())
        if result is not None:
            await message.answer(f"{amount} {from_currency.upper()} = {result} {to_currency.upper()}")
        else:
            await message.answer("Не удалось выполнить конвертацию. Проверьте введенные данные.")
    except ValueError:
        await message.answer("Неверный формат. Используйте формат: 100 USD to RUB")