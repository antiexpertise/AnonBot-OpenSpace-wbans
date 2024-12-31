import asyncio

import logging

from src.throttling import ThrottlingMiddleware

from src.handlers import setup_message_routers


from src import dp, bot



async def main() -> None:


    message_routers = setup_message_routers()
    dp.include_router(message_routers)
    dp.message.middleware.register(ThrottlingMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # try:
    #     asyncio.run(main())
    # except:
    #     print("exit")
    asyncio.run(main())