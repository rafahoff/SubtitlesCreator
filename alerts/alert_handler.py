from alerts import telegram_connector
import asyncio


def alert(message):
    asyncio.run(telegram_connector.send(message))
    print(message)

##TODO: Implement email alert
