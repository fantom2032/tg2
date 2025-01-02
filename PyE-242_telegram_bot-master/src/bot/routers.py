# Local
from src.bot.handlers.master import master_router
from src.bot.handlers.exchange import exchange_router
from src.bot.handlers.wheather import wheather_router


ROUTERS = [master_router, exchange_router, wheather_router]
