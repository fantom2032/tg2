from aiohttp import ClientSession, ClientResponseError
from src.settings.base import API_URL, logger, VOLUME
import aiofiles
from typing import Literal
import json

async def get_exchange_rate(currency: Literal["RUB", "KZT", "USD"]):
    async with ClientSession() as session:
        try:
            response = await session.get(url=API_URL + currency)
            response.raise_for_status()
        except ClientResponseError as cre:
            logger.error(f"Error while during request: {cre}")
            return None
        data: dict = await response.json()
    rates = data.get("conversion_rates")
    async with aiofiles.open(
        file=VOLUME + f"{currency}.json", mode="w"
    ) as file:
        data_json = json.dumps(obj=rates, indent=4)
        await file.write(data_json)
    logger.info(f"File {currency}.json created!")
    return rates

async def convert_currency(amount: float, from_currency: str, to_currency: str):
    from_rates = await get_exchange_rate(from_currency)
    if from_rates is None:
        return None

    if to_currency not in from_rates:
        logger.error(f"Target currency {to_currency} not found in exchange rates")
        return None

    conversion_rate = from_rates[to_currency]
    converted_amount = amount * conversion_rate
    return round(converted_amount, 2)