# Aiogram
from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext

# Local
from src.bot.states import WheatherStates
from src.bot.utils.wheather import get_current_wheather
from src.bot.utils.wheather import get_wheather_forecast

wheather_router = Router()


@wheather_router.callback_query(
    WheatherStates.current_or_forecast, F.data == "current"
)
async def request_for_city_current(
    callback: CallbackQuery, state: FSMContext
):
    await state.update_data(data={"status": callback.data})
    await state.set_state(state=WheatherStates.request_for_city)
    await callback.message.answer(text="Введите название города")


@wheather_router.callback_query(
    WheatherStates.current_or_forecast, F.data == "forecast"
)
async def request_for_city_forecast(
    callback: CallbackQuery, state: FSMContext
):
    await callback.message.answer(text="Функция пока не реализована")


@wheather_router.message(WheatherStates.request_for_city)
async def wait_city_current(message: Message, state: FSMContext):
    data = await state.get_data()
    status = data.get("status")
    if status == "forecast":
        return
    current_wheather: dict = await get_current_wheather(
        city_name=message.text
    )
    if not current_wheather:
        await message.answer(
            text="Что-то пошло не так, введите название города корректно!"
        )
    else:
        temp = current_wheather["temp_c"]
        condition = current_wheather["condition"]["text"]
        wind = current_wheather["wind_kph"]
        humidity = current_wheather["humidity"]
        template = f"""Температура воздуха {temp}, кондиция {condition},
        ветер {wind} км/ч, влажность воздуха {humidity}."""
        await state.clear()
        await message.answer(text=template)

@wheather_router.callback_query(
    WheatherStates.current_or_forecast, F.data == "forecast"
)
async def request_for_city_forecast(
    callback: CallbackQuery, state: FSMContext
):
    await state.update_data(status="forecast")
    await state.set_state(WheatherStates.request_for_city)
    await callback.message.answer(text="Введите название города для прогноза погоды")

@wheather_router.message(WheatherStates.request_for_city)
async def wait_city_forecast(message: Message, state: FSMContext):
    data = await state.get_data()
    status = data.get("status")
    if status == "current":
        return await wait_city_current(message, state)
    
    forecast = await get_wheather_forecast(city_name=message.text, days_count=3)
    if not forecast:
        await message.answer(
            text="Что-то пошло не так, введите название города корректно!"
        )
    else:
        forecast_text = "Прогноз погоды на 3 дня:\n\n"
        for day in forecast['forecast']['forecastday']:
            date = day['date']
            max_temp = day['day']['maxtemp_c']
            min_temp = day['day']['mintemp_c']
            condition = day['day']['condition']['text']
            forecast_text += f"{date}:\n"
            forecast_text += f"Макс. температура: {max_temp}°C\n"
            forecast_text += f"Мин. температура: {min_temp}°C\n"
            forecast_text += f"Условия: {condition}\n\n"
        
        await state.clear()
        await message.answer(text=forecast_text)