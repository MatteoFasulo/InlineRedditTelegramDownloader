import logging
import os
import re
import json
import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, InlineQueryHandler, filters, ConversationHandler, CallbackQueryHandler
from dotenv import load_dotenv
from urllib.request import Request, urlopen

from buttons import *
from utils import *

# Settings JSON filename
filename='settings.json'

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

#States
LEVEL1, LEVEL2, LEVEL3, LEVEL4 = range(4)

#Menus
SETTINGS, HELP = range(2)

DOWNLOAD_LIMIT, CONTENT_FILTER, CONTENT_TYPE, BACK = range(4)

UPDATE_LIMIT, UPDATE_FILTER, UPDATE_TYPE, BACK = range(4)


### MAIN MENU HANDLER
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global userId
    userId = str(update.message.from_user.username)
    await update.message.reply_text(f"WELCOME *{userId.upper()}*\nEnjoy your time here!\n",parse_mode=ParseMode.MARKDOWN)
    
    with open(filename, 'r', encoding='utf-8') as usersList:
        usersList = json.load(usersList)

    if not str(update.message.chat.id) in list(set().union(*(d.keys() for d in usersList))):
        userData = {
            update.message.chat.id : {
                'id' : update.message.chat.id,
                'limit': 10,
                'content_filter' : 'top',
                'content_type' : 'all',
            }   
        }
        usersList.append(userData)
        with open(filename, 'w', encoding='utf-8') as settingsFile:
            json.dump(usersList, settingsFile, indent=4)
    
    button1 = InlineKeyboardButton(
        b1, callback_data=str(SETTINGS)
    )
    button2 = InlineKeyboardButton(
            b2, callback_data=str(HELP)
    )

    message = "Tap on these buttons if you want to modify Bot settings or if you need help!"

    await update.message.reply_text(
                text = message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup = InlineKeyboardMarkup([
                    [button1, button2]
                ])
            )
    return LEVEL2

### RESTART CONV HANDLER
async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   query = update.callback_query
   await query.answer()
   button1 = InlineKeyboardButton(
        b1, callback_data=str(SETTINGS)
   )
   button2 = InlineKeyboardButton(
        b2, callback_data=str(HELP)
   )

   message = "Tap on these buttons if you want to modify Bot settings or if you need help!"
   await query.edit_message_text(
            text = message,
            reply_markup = InlineKeyboardMarkup([
                [button1, button2]
            ])
        )
   return LEVEL2

### SETTINGS HANDLER
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    button3 = InlineKeyboardButton(
        b3, callback_data=str(DOWNLOAD_LIMIT)
    )
    button4 = InlineKeyboardButton(
        b4, callback_data=str(CONTENT_FILTER)
    )
    button5 = InlineKeyboardButton(
        b5, callback_data=str(CONTENT_TYPE)
    )
    button20 = InlineKeyboardButton(
        b20, callback_data=str(BACK)
    )

    with open(filename, 'r', encoding='utf-8') as usersList:
        usersList = json.load(usersList)
    chatID = str(update.callback_query.message.chat.id)
    
    ID = [chatID in i for i in usersList].index(True)
    message = f"""*Current Settings*

Limit: {usersList[ID][chatID]['limit']}
Content Filter: {usersList[ID][chatID]['content_filter']}
Desired Content: {usersList[ID][chatID]['content_type']}
"""
    await query.edit_message_text(
        text= message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup = InlineKeyboardMarkup([
            [button3],
            [button4, button5],
            [button20]
            ])
        )
    return LEVEL3

### HELP HANDLER
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    button20 = InlineKeyboardButton(
        b20, callback_data=str(BACK)
    )

    message = f"""*H E L P*

/start - 
/help - 
/settings -
               
*_______________*
"""

    await query.edit_message_text(
        text= message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup = InlineKeyboardMarkup([[button20]])
        )
    return LEVEL1

async def download_limit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chatID = str(update.callback_query.message.chat.id)
    query = update.callback_query
    with open(filename, 'r', encoding='utf-8') as usersList:
        usersList = json.load(usersList)
    ID = [chatID in i for i in usersList].index(True)

    await query.answer()

    button20 = InlineKeyboardButton(
        b20, callback_data=str(BACK)
    )
    keyboard = [[InlineKeyboardButton(str(i), callback_data=f"{str(UPDATE_LIMIT)} | {str(i)}") for i in range(5, 30, 5)],
                [button20]]
    message = f"Choose the desired download limit.\nCurrent: {usersList[ID][chatID]['limit']}"
    await query.edit_message_text(
        text=message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup = InlineKeyboardMarkup(keyboard)
        )
    return LEVEL4

async def content_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chatID = str(update.callback_query.message.chat.id)
    query = update.callback_query
    with open(filename, 'r', encoding='utf-8') as usersList:
        usersList = json.load(usersList)
    ID = [chatID in i for i in usersList].index(True)
   
    await query.answer()

    button6 = InlineKeyboardButton(
        b6, callback_data=f"{str(UPDATE_FILTER)} | {b6}"
    )
    button7 = InlineKeyboardButton(
        b7, callback_data=f"{str(UPDATE_FILTER)} | {b7}"
    )
    button9 = InlineKeyboardButton(
        b9, callback_data=f"{str(UPDATE_FILTER)} | {b9}"
    )
    button10 = InlineKeyboardButton(
        b10, callback_data=f"{str(UPDATE_FILTER)} | {b10}"
    )
    button20 = InlineKeyboardButton(
        b20, callback_data=str(BACK)
    )
    message = f"Choose the desired content filter.\nCurrent: {usersList[ID][chatID]['content_filter']}"
    await query.edit_message_text(
        text= message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup = InlineKeyboardMarkup([
            [button6],
            [button7],
            [button9],
            [button10],
            [button20]
            ])
        )
    return LEVEL4

async def content_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chatID = str(update.callback_query.message.chat.id)
    query = update.callback_query
    with open(filename, 'r', encoding='utf-8') as usersList:
        usersList = json.load(usersList)
    ID = [chatID in i for i in usersList].index(True)
   
    await query.answer()

    button11 = InlineKeyboardButton(
        b11, callback_data=f"{str(UPDATE_TYPE)} | {b11}"
    )
    button12 = InlineKeyboardButton(
        b12, callback_data=f"{str(UPDATE_TYPE)} | {b12}"
    )
    button13 = InlineKeyboardButton(
        b13, callback_data=f"{str(UPDATE_TYPE)} | {b13}"
    )
    button14 = InlineKeyboardButton(
        b14, callback_data=f"{str(UPDATE_TYPE)} | {b14}"
    )
    button20 = InlineKeyboardButton(
        b20, callback_data=str(BACK)
    )
    message = f"Choose the desired content type.\nCurrent: {usersList[ID][chatID]['content_type']}"
    await query.edit_message_text(
        text= message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup = InlineKeyboardMarkup([
            [button11, button12, button13],
            [button14],
            [button20]
            ])
        )
    return LEVEL4

async def update_limit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chatID = str(update.callback_query.message.chat.id)
    query = update.callback_query
    await query.answer()
    button20 = InlineKeyboardButton(
        b20, callback_data=str(BACK)
    )
    newLimit = int(query.data.split('|')[-1])

    ### Update newlimit in JSON
    with open(filename, 'r', encoding='utf-8') as usersList:
        usersList = list(json.load(usersList))

    ID = [chatID in i for i in usersList].index(True)
    
    userDict = usersList[ID][chatID]
    userDict['limit'] = newLimit
    userDict.update(userDict)
    usersList.pop(ID)
    usersList.append({
        chatID: userDict
    })

    with open(filename, 'w', encoding='utf-8') as settingsFile:
            json.dump(usersList, settingsFile, indent=4)


    message = f"Succesfully changed the limit to {newLimit}!"
    await query.edit_message_text(
        text=message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup = InlineKeyboardMarkup([
                [button20]
            ])
    )
    return LEVEL1

async def update_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chatID = str(update.callback_query.message.chat.id)
    query = update.callback_query
    await query.answer()
    button20 = InlineKeyboardButton(
        b20, callback_data=str(BACK)
    )
    newFilter = query.data.split('|')[-1].strip().lower()

    ### Update newlimit in JSON
    with open(filename, 'r', encoding='utf-8') as usersList:
        usersList = list(json.load(usersList))
    
    ID = [chatID in i for i in usersList].index(True)
    
    userDict = usersList[ID][chatID]
    userDict['content_filter'] = newFilter
    userDict.update(userDict)
    usersList.pop(ID)
    usersList.append({
        chatID: userDict
    })

    with open(filename, 'w', encoding='utf-8') as settingsFile:
            json.dump(usersList, settingsFile, indent=4)


    message = f"Succesfully changed the content filter to {newFilter}!"
    await query.edit_message_text(
        text=message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup = InlineKeyboardMarkup([
                [button20]
            ])
    )
    return LEVEL1

async def update_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chatID = str(update.callback_query.message.chat.id)
    query = update.callback_query
    await query.answer()
    button20 = InlineKeyboardButton(
        b20, callback_data=str(BACK)
    )
    newType = query.data.split('|')[-1].strip().lower()

    ### Update newlimit in JSON
    with open(filename, 'r', encoding='utf-8') as usersList:
        usersList = list(json.load(usersList))
    
    ID = [chatID in i for i in usersList].index(True)
    
    userDict = usersList[ID][chatID]
    userDict['content_type'] = newType
    userDict.update(userDict)
    usersList.pop(ID)
    usersList.append({
        chatID: userDict
    })

    with open(filename, 'w', encoding='utf-8') as settingsFile:
            json.dump(usersList, settingsFile, indent=4)


    message = f"Succesfully changed the content filter to {newType}!"
    await query.edit_message_text(
        text=message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup = InlineKeyboardMarkup([
                [button20]
            ])
    )
    return LEVEL1
 

async def subreddit_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subr = str(update.message.text)
    subr = subr.split("/")[-1]
    print(f"[i] Executing request for subreddit r/{subr} made by @{update.message.chat.username}")
    await bulk_subreddit_downloader(subr, update, context)
    await update.message.reply_markdown(f'Finished to send everything from _{subr}_',
        reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(b1, callback_data=str(SETTINGS)), 
                        InlineKeyboardButton(b2, callback_data=str(HELP))]
                        ])
        )
    print(f"[i] Finished request of @{update.message.chat.username}")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query

    if query == "":
        return

    results = [InlineQueryResultArticle(
        id=subreddit.display_name, 
        title=subreddit.display_name, 
        input_message_content=InputTextMessageContent(f"r/{subreddit.display_name}")) async for subreddit in createIstance().subreddits.search_by_name(query=query)]

    await update.inline_query.answer(results)


async def bulk_subreddit_downloader(subr, update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(filename, 'r', encoding='utf-8') as usersList:
        usersList = list(json.load(usersList))
        userDict = [sub[str(update.message.chat.id)] for sub in usersList][0]

    def checkLinkActive(url):
        request = requests.head(url)
        if request.status_code == 200:
            return True
        else:
            return False
    
    def parseContent(content):
        if '.png' in content or '.jpg' in content or '.jpeg' in content:
            return 'image'
        elif 'redgifs' in content:
            return 'redgifs'
        elif 'v.redd' in content:
            return 'video'
        else:
            return None # prolly gallery item

    def redgifs(url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        request_url = Request(url, headers=headers)
        CONTENT_RE = re.compile(r'https:\/\/[a-z0-9]+.redgifs.com\/\w+.mp4')

        with urlopen(request_url) as response:
            html = response.read().decode('utf-8')

        content = re.search(CONTENT_RE, html).group(0)
        return content

    async def download(limit: int, subReddit: str):
        istance = createIstance()
        try:
            subreddit = await istance.subreddit(subReddit)
            await update.message.reply_markdown(f'Ok I will download all the available content from _{subr}_...')
            ### Check Content Filter for Subreddit
            if userDict['content_filter'] == "top":
                async for submission in subreddit.top(limit=limit):
                    try:
                        contentType = parseContent(submission.url) # filter content type
                        ### Content Type
                        if userDict['content_type'] == "all":
                            image, video, gifs = True, True, True
                        elif userDict['content_type'] == "photo":
                            image = True
                        elif userDict['content_type'] == "video":
                            video = True
                        elif userDict['content_type'] == "gif":
                            gifs = True

                        if contentType == 'image' and checkLinkActive(submission.url) and image:
                            url = re.findall(r"(.*\.jpg|.*\.png).*",submission.url)[0]
                            try:
                                await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_PHOTO)
                                await context.bot.send_photo(
                                chat_id=update.message.chat_id,
                                photo=requests.get(f"{url}").content,
                                )
                            except Exception as e:
                                print(e)
                                continue

                        elif contentType == 'video' and video:
                            try:
                                video = requests.get(f"{submission.url.lower()}/DASH_240.mp4").content
                            except Exception:
                                video = requests.get(f"{submission.url.lower()}/DASH_480.mp4").content
                            try:
                                await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_VIDEO)
                                await context.bot.send_video(
                                chat_id=update.message.chat_id,
                                video=video,
                                supports_streaming=True,
                                )
                            except Exception as e:
                                print(e)
                                continue

                        elif contentType == 'redgifs' and gifs:
                            try:
                                gif = requests.get(f"{redgifs(submission.url)}").content
                                await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_DOCUMENT)
                                await context.bot.send_video(
                                chat_id=update.message.chat_id,
                                video=gif,
                                supports_streaming=True,
                                )
                            except Exception as e:
                                print(e)
                                continue 
                        else:
                            continue
                    
                    except Exception:
                        continue
            elif userDict['content_filter'] == "new":
                async for submission in subreddit.new(limit=limit):
                        try:
                            contentType = parseContent(submission.url) # filter content type
                            ### Content Type
                            if userDict['content_type'] == "all":
                                image, video, gifs = True, True, True
                            elif userDict['content_type'] == "photo":
                                image = True
                            elif userDict['content_type'] == "video":
                                video = True
                            elif userDict['content_type'] == "gif":
                                gifs = True

                            if contentType == 'image' and checkLinkActive(submission.url) and image:
                                url = re.findall(r"(.*\.jpg|.*\.png).*",submission.url)[0]
                                try:
                                    await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_PHOTO)
                                    await context.bot.send_photo(
                                    chat_id=update.message.chat_id,
                                    photo=requests.get(f"{url}").content,
                                    )
                                except Exception as e:
                                    print(e)
                                    continue

                            elif contentType == 'video' and video:
                                try:
                                    video = requests.get(f"{submission.url.lower()}/DASH_240.mp4").content
                                except Exception:
                                    video = requests.get(f"{submission.url.lower()}/DASH_480.mp4").content
                                try:
                                    await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_VIDEO)
                                    await context.bot.send_video(
                                    chat_id=update.message.chat_id,
                                    video=video,
                                    supports_streaming=True,
                                    )
                                except Exception as e:
                                    print(e)
                                    continue

                            elif contentType == 'redgifs' and gifs:
                                try:
                                    gif = requests.get(f"{redgifs(submission.url)}").content
                                    await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_DOCUMENT)
                                    await context.bot.send_video(
                                    chat_id=update.message.chat_id,
                                    video=gif,
                                    supports_streaming=True,
                                    )
                                except Exception as e:
                                    print(e)
                                    continue 
                            else:
                                continue
                        
                        except Exception:
                            continue

            elif userDict['content_filter'] == "rising":
                async for submission in subreddit.rising(limit=limit):
                        try:
                            contentType = parseContent(submission.url) # filter content type
                            ### Content Type
                            if userDict['content_type'] == "all":
                                image, video, gifs = True, True, True
                            elif userDict['content_type'] == "photo":
                                image = True
                            elif userDict['content_type'] == "video":
                                video = True
                            elif userDict['content_type'] == "gif":
                                gifs = True

                            if contentType == 'image' and checkLinkActive(submission.url) and image:
                                url = re.findall(r"(.*\.jpg|.*\.png).*",submission.url)[0]
                                try:
                                    await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_PHOTO)
                                    await context.bot.send_photo(
                                    chat_id=update.message.chat_id,
                                    photo=requests.get(f"{url}").content,
                                    )
                                except Exception as e:
                                    print(e)
                                    continue

                            elif contentType == 'video' and video:
                                try:
                                    video = requests.get(f"{submission.url.lower()}/DASH_240.mp4").content
                                except Exception:
                                    video = requests.get(f"{submission.url.lower()}/DASH_480.mp4").content
                                try:
                                    await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_VIDEO)
                                    await context.bot.send_video(
                                    chat_id=update.message.chat_id,
                                    video=video,
                                    supports_streaming=True,
                                    )
                                except Exception as e:
                                    print(e)
                                    continue

                            elif contentType == 'redgifs' and gifs:
                                try:
                                    gif = requests.get(f"{redgifs(submission.url)}").content
                                    await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_DOCUMENT)
                                    await context.bot.send_video(
                                    chat_id=update.message.chat_id,
                                    video=gif,
                                    supports_streaming=True,
                                    )
                                except Exception as e:
                                    print(e)
                                    continue 
                            else:
                                continue
                        
                        except Exception:
                            continue

            elif userDict['content_filter'] == "hot":
                async for submission in subreddit.hot(limit=limit):
                        try:
                            contentType = parseContent(submission.url) # filter content type
                            ### Content Type
                            if userDict['content_type'] == "all":
                                image, video, gifs = True, True, True
                            elif userDict['content_type'] == "photo":
                                image = True
                            elif userDict['content_type'] == "video":
                                video = True
                            elif userDict['content_type'] == "gif":
                                gifs = True

                            if contentType == 'image' and checkLinkActive(submission.url) and image:
                                url = re.findall(r"(.*\.jpg|.*\.png).*",submission.url)[0]
                                try:
                                    await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_PHOTO)
                                    await context.bot.send_photo(
                                    chat_id=update.message.chat_id,
                                    photo=requests.get(f"{url}").content,
                                    )
                                except Exception as e:
                                    print(e)
                                    continue

                            elif contentType == 'video' and video:
                                try:
                                    video = requests.get(f"{submission.url.lower()}/DASH_240.mp4").content
                                except Exception:
                                    video = requests.get(f"{submission.url.lower()}/DASH_480.mp4").content
                                try:
                                    await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_VIDEO)
                                    await context.bot.send_video(
                                    chat_id=update.message.chat_id,
                                    video=video,
                                    supports_streaming=True,
                                    )
                                except Exception as e:
                                    print(e)
                                    continue

                            elif contentType == 'redgifs' and gifs:
                                try:
                                    gif = requests.get(f"{redgifs(submission.url)}").content
                                    await context.bot.sendChatAction(chat_id=update.message.chat_id , action=ChatAction.UPLOAD_DOCUMENT)
                                    await context.bot.send_video(
                                    chat_id=update.message.chat_id,
                                    video=gif,
                                    supports_streaming=True,
                                    )
                                except Exception as e:
                                    print(e)
                                    continue 
                            else:
                                continue
                        
                        except Exception:
                            continue

        except Exception:
            return
        
        await istance.close()

    ### Fetch the limit from JSON
    return await download(limit=int(userDict['limit']), subReddit=subr)


def main() -> None:
    settingsConfig()
    botFatherToken()
    assert(load_dotenv())
    API_KEY = os.getenv('API_KEY')
    application = Application.builder().token(API_KEY).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
      entry_points=[CommandHandler('start', main_menu)],
      states={
         LEVEL1: [
            CallbackQueryHandler(start_over, pattern=str(BACK))
         ],
         LEVEL2: [
            CallbackQueryHandler(start_over, pattern=str(BACK)),
            CallbackQueryHandler(settings, pattern=str(SETTINGS)),
            CallbackQueryHandler(help, pattern=str(HELP)),
         ],
         LEVEL3: [
            CallbackQueryHandler(start_over, pattern=str(BACK)),
            CallbackQueryHandler(download_limit, pattern=str(DOWNLOAD_LIMIT)),
            CallbackQueryHandler(content_filter, pattern=str(CONTENT_FILTER)),
            CallbackQueryHandler(content_type, pattern=str(CONTENT_TYPE)),
         ],
         LEVEL4: [
            CallbackQueryHandler(start_over, pattern=str(BACK)),
            CallbackQueryHandler(update_limit, pattern=str(UPDATE_LIMIT)),
            CallbackQueryHandler(update_filter, pattern=str(UPDATE_FILTER)),
            CallbackQueryHandler(update_type, pattern=str(UPDATE_TYPE)),
         ]
      },
      fallbacks=[CommandHandler('start_over', start_over)],
      allow_reentry=True,
      per_message=False,
   )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('start', start_over))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(MessageHandler(filters.Regex(pattern=r'^r\/'), subreddit_name))
    

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()


