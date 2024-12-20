# Local
from src.bot.handlers.master import master_router
from src.bot.handlers.exchange import exchange_router


ROUTERS = [master_router, exchange_router]
