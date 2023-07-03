from datetime import datetime
import logging
from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent)
import os
from db import *
from peewee import fn

logging.basicConfig(filename='inline_predictions_bot.log', encoding='utf-8', level=logging.INFO) # logging

api_id = os.getenv('API_ID') # bot settings
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
bot_short_name = "inline_predictions_bot"

app = Client( # bot initialization
    bot_short_name,
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)
admins = [965840090]


@app.on_inline_query()
async def answer(client, inline_query): # get random prediction from database
    logging.info("Inline query from " + str(inline_query.from_user.first_name) + " - " + str(inline_query.from_user.id))
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="Стопроцентно точный прогноз",
                input_message_content=InputTextMessageContent(
                    inline_query.from_user.first_name + ", " + Prediction.select().order_by(fn.Random()).limit(1)[0].text
                ),
                description="Узнайте свое будущее здесь и сейчас!\nНикогда не ошибаемся!"
            )
        ],
        cache_time=0
    )


@app.on_message(filters.command(['start'])) # explaining how to use it
async def start(bot, message):
    logging.info("/start query from " + str(message.from_user.first_name) + " - " + str(message.from_user.id))
    await bot.send_message(message.chat.id, text="Привет, я inline бот, который может предсказать твое будущее!\nЧтобы воспользоваться мной, набери @"+bot_short_name+" и поставь пробел, затем выбери нужный пункт")

@app.on_message(filters.command(['add_new'])) # add new prediction
async def start(bot, message):
    logging.info("/add_new query from " + str(message.from_user.first_name) + " - " + str(message.from_user.id))
    if message.from_user.id not in admins:
        await bot.send_message(message.chat.id, text="А ты еще кто такой?")
        logging.info("rejected" "/add_new query from " + str(message.from_user.first_name) + " - " + str(message.from_user.id))
    else:
        if message.text != "/add_new" and message.text != "/add_new ":
            prediction = Prediction(text=message.text[9:], date_modified=datetime.now())
            prediction.save()
            logging.info("Added new prediction from " + str(message.from_user.first_name) + " - " + str(message.from_user.id) + " : " + prediction.text)
            await bot.send_message(message.chat.id, text="Успешный успех! Я добавил новое предсказание")
        else:
            logging.info('Empty /add_new')
            await bot.send_message(message.chat.id, text="Дурак, куда ты жмешь")


logging.info('Working...')
app.run()
