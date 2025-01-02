# Python
from typing import Literal
import json

# Third-Party
from aiohttp import ClientSession, ClientResponseError
import aiofiles

# Local
from src.settings.base import API_URL, logger, VOLUME


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
    return
