# InlineRedditTelegramDownloader
Inline Python Telegram Bot to download contents from subreddits

# Libraries
```
pip install -r requirements.txt
```
* Latest release of [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (v20)
* Python 3.8
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
