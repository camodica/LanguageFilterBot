#!/user/bin/python

# LanguageFilterBot.py
#
# This python file contains the logic for a Discord bot.
# It is designed to delete messages with offending content
# in their body and re-post them with the words replaced by
# some selected from a list of replacements. Requires admin
# priviliges!
#
# @author Corbin Modica

import os

import discord
from dotenv import load_dotenv

load_dotenv()

# Set a list of banned words to filter out later
banned_words = ["Nice meme!", "Nice meme 2!"]

# The token the bot uses for authentication to the discord servers. Stored as part of the environment for security
# and portability.
TOKEN = os.getenv('DISCORD_TOKEN')

# Connect to discord using the Client paradigm
client = discord.Client()

# Checks to see if a message (seen in variable content) contains any of the list of banned words (banned)
# A tuple with True and a list of all of the violating words found if any, and False and an empty list if none were found
def checkForViolations(content, banned):
    result = False
    words_found = []
    for ban in banned:
        if ban in content:
            words_found.append(ban)
            result = True
    return result, words_found

# Replaces all of the occurances of the given words in the given message with random choices from the
# given list of replacements
def removeViolatingWords(content, banned, replacements):
    editedContent = ""

    return editedContent

@client.event
async def on_ready():
    print(f'Bot connected to Discord as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check for banned words in the message posted by the user
    violating, violations = checkForViolations(message.content, banned_words)

    # If a banned word or word(s) is found, remove the message, admonish the user, and re-post the clean message 
    if violating:
        originalAuthor = message.author
        print("Bad message from user " + str(originalAuthor))

        editedMessage = "Not a nice meme!"
        editedMessage = str(originalAuthor) + ", that message violated language guidelines. The edited message is below:\n" + editedMessage

        await message.delete()
        await message.channel.send(editedMessage)

client.run(TOKEN)
