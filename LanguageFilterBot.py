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

import random

import csv

import re

import discord
from dotenv import load_dotenv

load_dotenv()

#
# Script scope variables
#

# TODO: Replace these lists with OI/files so that they are not magic data structures?
# Set a list of banned words to filter out later
# banned_words = ["fucking", "fuck"]

with open('bad_words.txt', newline='') as f:
    reader = csv.reader(f)
    tmp = list(reader)

    banned_words = tmp[0]
    banned_words = [word.strip() for word in banned_words]

# Set a list of replacement words to filter out later
# replacement_words = ["derply", "ploobert"]

with open('funny_words.txt', newline='') as f:
    reader = csv.reader(f)
    tmp = list(reader)

    replacement_words = tmp[0]
    replacement_words = [word.strip() for word in replacement_words]

# A dictionary that tracks userIDs and the number of times that they have violated guidelines!
user_strikes = {}

# The token the bot uses for authentication to the discord servers. Stored as part of the environment for security
# and portability.
TOKEN = os.getenv('DISCORD_TOKEN')

# Connect to discord using the Client paradigm
client = discord.Client()

#
# Utility Functions
#

# Checks to see if a message (seen in variable content) contains any of the list of banned words (banned)
# A tuple with True and a list of all of the violating words found if any, and False and an empty list if none were found
def checkForViolations(content, banned):
    result = False
    words_found = []
    for ban in banned:

        # create regex for the banned word (case and jerund/spelling agnostic)
        # TODO: make this more fancy for better matches
        regex = ban

        # find all the matches (case agnostic)
        matches = re.findall(regex, content, re.IGNORECASE)

        # add all the matches found to the words_found list
        for match in matches:
            if match not in words_found:
                words_found.append(match)
                result = True # TODO there should be a smarter way to do this that doesnt require reassigning every loop
        
        # if ban.toLower() in content.toLower():
        #     words_found.append(ban)
        #     result = True

            
    return result, words_found

# Replaces all of the occurances of the given words in the given message with random choices from the
# given list of replacements
def removeViolatingWords(content, violations, replacements):
    edited_content = content

    # For each violating word, replace that word with a random funny word
    for word in violations:
        edited_content = edited_content.replace(word, random.choice(replacements))

    return edited_content

#
# Listeners
#

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

        # Increment the number of strikes that this user has
        if originalAuthor in user_strikes:
            user_strikes[originalAuthor] = user_strikes[originalAuthor] + 1
        else:
            user_strikes[originalAuthor] = 1

        # Console message about the user's message
        print("Bad message from user " + str(originalAuthor))
        print("   That user has " + str(user_strikes[originalAuthor]) + " strikes!")

        # Replace the offending message in the server
        editedMessage = removeViolatingWords(message.content, violations, replacement_words)
        editedMessage = str(originalAuthor) + ", that message violated language guidelines. The edited message is below:\n" + editedMessage

        await message.delete()
        await message.channel.send(editedMessage)

# Start the bot!
client.run(TOKEN)
