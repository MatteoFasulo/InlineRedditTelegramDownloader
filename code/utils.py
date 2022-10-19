import os
import asyncpraw
import yaml
import json

filename = "settings.json"

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
    istance = asyncpraw.Reddit(
    client_id=creds.get("client_id"),
    client_secret=creds.get("client_secret"),
    user_agent=creds.get("user_agent"),
    username=creds.get("username"),
    password=creds.get("password"))
    return istance

def settingsConfig():
    if not os.path.isfile(filename):
        usersList = []
        with open(filename, 'w', encoding='utf-8') as settingsFile:
            json.dump(usersList, settingsFile, indent=4)
    return

def botFatherToken():
    if not os.path.isfile('.env'):
        correct = False
        while not correct:
            try:
                API_KEY = input('API KEY: ')
                correct = True
            except Exception:
                continue
        with open('.env', 'w', encoding='utf-8') as tokenFile:
            tokenFile.write(f'API_KEY = {API_KEY}')

    return