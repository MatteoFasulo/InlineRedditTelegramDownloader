# InlineRedditTelegramDownloader
Inline Python Telegram Bot to download contents from subreddits

# Libraries
```
pip install -r requirements.txt
```
* Latest release of [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (v20)
* Python 3.8
* PRAW (Reddit API)
* PyYAML
* Python-Dotenv

# Token and token.yaml (Reddit)
You need a Reddit APP to use this bot. 
1. Create a new App on [reddit website](https://www.reddit.com/prefs/apps)
2. Select `script` (personal use) 
3. Insert an App name
4. Insert http://localhost as `redirect uri` and `about url`
5. Copy the `client_id` (below the personal use script row) and `secret`
6. Insert `client_id`, `client_secret`, `password`, `user_agent` (app name), `username` (reddit username)

# BotFather Token (bot)
Remember to create a new bot on [@BotFather](https://telegram.me/BotFather) and insert the token into `.env` file

# How it works?
`main.py` file guides you through reddit token creation and runs the bot istance. User data will be stored in `settings.json` where each user will have his configuration of the bot including which content to download as well as the number of contents and filter of subreddit. Bot's menu is completely inline with callback queries empowered by the **ConversationHandler**
