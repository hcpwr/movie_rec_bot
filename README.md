# Movie Recommendation Bot

This is a Python code for a movie recommendation bot that recommends movies based on user-provided genres, actors, and keywords. The bot uses the CountVectorizer and cosine_similarity functions from the sklearn library to find similar movies from a dataset of 10,000 movies taken from Kaggle.

# Requirements

    Python 3.x
    pandas
    numpy
    sklearn
    telebot

# Dataset

The dataset used in this code consists of metadata, credits, and keywords of 10,000 movies taken from Kaggle.

# Bot Features

The bot has two main features:

    Start command: Sends a greeting message with instructions on how to use the bot.
    Input message: The user inputs their preferred genres, actors, and keywords separated by commas. The bot then processes the user's inputs and recommends three movies based on their preferences.

# Deployment
To deploy the bot, you will need to create a bot on Telegram and obtain a bot token. Once you have the token, replace the bot = telebot.TeleBot('YOUR BOT TOKEN') line with your bot token.
