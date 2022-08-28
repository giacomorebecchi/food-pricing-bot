from telegram import Update


def message(update: Update, message: str) -> str:
    return f"chat_id: {update.message.chat_id} \t {message}"


def new_user(update: Update) -> str:
    return "New player with CHAT_ID: %s, FULL_NAME: %s" % (
        update.message.chat_id,
        update.message.from_user.full_name,
    )


def cancelled_user(update: Update) -> str:
    return "User with CHAT_ID: %s used command /cancel" % update.message.chat_id


def stopped_playing(update: Update) -> str:
    return "User with CHAT_ID: %s used command /stop" % update.message.chat_id
