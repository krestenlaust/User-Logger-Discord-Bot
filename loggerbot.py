#!/usr/bin/python3
import discord
import asyncio
import aiofiles
from os.path import isdir, join
from os import makedirs
from re import sub

class Config(object):
    LOG_DIRECTORY = "Userlogs"  # Folder with log files.
    fileExt = ".log"  # The extension of the userlogs, if changed after logs are created multiple files will be created.
    avoidMsg = ["/", "t!"]  # Avoids messages containing one of these substrings.
    CMD_PREFIX = '$'  # The prefix to the commands.
    IGNORE_PREFIX = '£'  # Place this char infront of message to not store message.
    #TOKEN_KEY = "NDYwMDQwOTExNDg1OTI2nDY1.DG_yJw.iY19n6GzjWC-IqT1slIgySUbyAM"  # << Not actual token, just an example.
    TOKEN_KEY = "NTIzNTcxMTc3MDk3MTM0MDkx.XMFlow.jxaS93k0TvCu-WOLUphCtnlPxV4"
    SEPERATION_CHAR = '\n'  # The charactor that seperates new messages. Blank for none.


client = discord.Client()
print("Initiating logger")

@client.event
async def on_ready():
    print("Logged in as: " + client.user.name)
    print(client.user.id)
    print("Command prefix: " + repr(Config.CMD_PREFIX))
    print("Seperation char: " + repr(Config.SEPERATION_CHAR))
    print("Mute prefix: " + repr(Config.IGNORE_PREFIX))
    print("Log directory: {0}, log file extension: {1}".format(Config.LOG_DIRECTORY, Config.fileExt))
    print("-------------")
    if not isdir(Config.LOG_DIRECTORY):
        makedirs(Config.LOG_DIRECTORY)
        print("Created log folder: " + Config.LOG_DIRECTORY)

@client.event
async def on_message(message):
    if message.content.startswith(Config.CMD_PREFIX + "ping"):  # Used as a template for commands
        if message.author.bot:
            return False

        print("Ping recieved, responding")
        counter = 0
        tmp = await client.send_message(message.channel, "Pong")
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        return
    


    Nickname = ""

    if message.content[0] == Config.IGNORE_PREFIX or message.content[0] == Config.CMD_PREFIX:
        return

    for i in range(len(Config.avoidMsg)):
        if Config.avoidMsg[i] in message.content:
            print("Avoiding message: {0} | By {1}".format(message.content.replace("\n"," "), message.author.name))
            return
            #msg_contained = True

    Targetfile = join(Config.LOG_DIRECTORY, message.author.name + Config.fileExt) #Combines paths with relevant variables.
    Message_Text=sub("[^a-zA-Z -<>.,':]+", "", message.content.replace("\n"," "))+' ' #Sorts out not supported-chars.

    if len(Message_Text) < 1:
        return

    async with aiofiles.open(Targetfile, mode='a') as f:
        await f.write(Message_Text + Config.SEPERATION_CHAR)

    if not message.author.name == message.author.display_name:
        Nickname = "(" + str(message.author.display_name) + ")"

    print('{1}{2} said: {0}'.format(Message_Text, str(message.author.name), Nickname))

client.run(Config.TOKEN_KEY)
