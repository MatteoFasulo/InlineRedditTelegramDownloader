import logging
from html import escape
from uuid import uuid4
import os
import yaml
import re
import praw
from prawcore.exceptions import Forbidden, Redirect
from dotenv import load_dotenv
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_token():
    if not os.path.isdir("token"):
        os.mkdir("token")
    if not os.path.isfile(f"token{os.sep}token.yaml"):
        creds = {}
        creds["client_id"] = input("Client_id: ")
        creds["client_secret"] = input("client_secret: ")
        creds["user_agent"] = input("user_agent: ")
        creds["username"] = input("username: ")
        creds["password"] = input("password: ")
        with open(f'token{os.sep}token.yaml', 'w') as file:
            documents = yaml.dump(creds, file)
    else:
        with open(f'token{os.sep}token.yaml', 'r') as file:
            creds = yaml.safe_load(file)
    return creds

def createIstance():
    creds = create_token()
    istance = praw.Reddit(
    client_id=creds.get("client_id"),
    client_secret=creds.get("client_secret"),
    user_agent=creds.get("user_agent"),
    username=creds.get("username"),
    password=creds.get("password"))
    return istance


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hi!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")




async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    if query == "":
        return

    results = [InlineQueryResultArticle(id=str(uuid4()), title=subreddit.display_name, input_message_content=InputTextMessageContent(f"r/{subreddit.display_name}")) for subreddit in createIstance().subreddits.search_by_name(query=query)]

    await update.inline_query.answer(results)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5713821446:AAG_z1Gg5jAYTELsxH90aKJKCebeAyUHbdI").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()