import asyncio
import logging
import re

from telegram import __version__ as TG_VER

from food_pricing_bot.utils.db import (
    get_last_question,
    set_new_answer,
    set_new_question,
    set_new_user,
)

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This package is not compatible with your current PTB version {TG_VER}.\n"
        "Version 20.0.0 is required."
    )
from telegram import InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from food_pricing_bot.utils import bot_logging, data, sampling, settings, texts

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = settings.get_settings().TOKEN

Y_OR_N_REGEX = f"^({texts.P_ANSWER}|{texts.N_ANSWER})$"
PLAY_REGEX = (
    rf"^(?P<YoN>{texts.P_ANSWER}|{texts.N_ANSWER})|"  # first round
    r"\D*\d+\D*\d{0,2}\D*$"  # price
)

INSTRUCTIONS, PLAY = range(2)

SLEEP_SECONDS = 5


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and explains the rules of the game."""
    logging.info(bot_logging.new_user(update))

    reply_keyboard = [[texts.P_ANSWER, texts.N_ANSWER]]
    for text in texts.WELCOME_TEXTS:
        await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(SLEEP_SECONDS)

    await update.message.reply_text(
        texts.START_TEXT,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Scopriamo in cosa consiste il gioco?",
        ),
    )

    await set_new_user(update=update)

    return INSTRUCTIONS


async def instructions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the game if the player is ready, else it says goodbye."""
    if update.message.text == texts.N_ANSWER:
        await update.message.reply_text(
            texts.NOT_READY_TEXT, reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    elif update.message.text == texts.P_ANSWER:
        for text in texts.READY_TEXTS:
            await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(SLEEP_SECONDS)
        reply_keyboard = [[texts.P_ANSWER, texts.N_ANSWER]]
        await update.message.reply_text(
            texts.INSTRUCTIONS_TEXT,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                input_field_placeholder="Pronto ad iniziare?",
            ),
        )
        return PLAY
    else:
        raise ValueError("Unrecognised answer.")


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Plays one round of the game."""
    chat_id = update.message.chat_id
    regex_dict = re.match(PLAY_REGEX, update.message.text).groupdict()
    if regex_dict["YoN"] == texts.P_ANSWER:
        await update.message.reply_text(
            texts.START_PLAYING_TEXT, reply_markup=ReplyKeyboardRemove()
        )
    elif regex_dict["YoN"] == texts.N_ANSWER:
        await update.message.reply_text(
            texts.NOT_UNDERSTOOD_INSTRUCTIONS_TEXT, reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    elif regex_dict["YoN"] is None:
        previous_item_id = await get_last_question(chat_id)
        correct_price = data.get_correct_price(previous_item_id)
        await update.message.reply_text(
            texts.correct_price_text(correct_price), reply_markup=ReplyKeyboardRemove()
        )
        await set_new_answer(
            chat_id=chat_id,
            item_id=previous_item_id,
            answer=update.message.text,
        )

    new_item_id = await sampling.sample_new_item(chat_id)
    await set_new_question(chat_id=chat_id, item_id=new_item_id)
    img = await data.get_img(new_item_id)
    txt = data.get_txt(new_item_id)
    media = InputMediaPhoto(media=img, caption=txt)
    await update.message.reply_media_group(media)
    return PLAY


async def stop_playing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stops the game and ends the conversation."""
    logger.info(bot_logging.stopped_playing(update))
    await update.message.reply_text(texts.STOP_TEXT, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    logger.info(bot_logging.cancelled_user(update))
    await update.message.reply_text(texts.CANC_TEXT, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states READY, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INSTRUCTIONS: [MessageHandler(filters.Regex(Y_OR_N_REGEX), instructions)],
            PLAY: [
                MessageHandler(filters.Regex(PLAY_REGEX), play),
                CommandHandler("stop", stop_playing),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
