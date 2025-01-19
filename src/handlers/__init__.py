from aiogram import Router



def setup_message_routers() -> Router:
    from . import start, bot_messages, ban

    router = Router()
    router.include_router(start.router)
    router.include_router(ban.router)
    router.include_router(bot_messages.router)

    return router