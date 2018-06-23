#!/usr/bin/python3
import discord, asyncio, aiofiles
from os.path import isdir,join
from os import makedirs

logFolder = "Userlogs" #Folder with log files.
fileExt = ".log" #The extension of the userlogs, if changed after logs are created multiple files will be created.
avoidMsg = ["Image made with","Loading...","t!"] #Avoids messages containing one of these substrings.
cmdPrefix = '$' #The prefix to the commands.
tokenKey = "Ezh1NzEwNTMxDzU4NzuYdzY4.Dco2xQ.r3jHprruoNuIGDdfxroYa9G40Sk" #<< Not actual token, just an example.

client = discord.Client()
print("Initiating logger")
@client.event
async def on_ready():
    print("Logged in as: "+client.user.name)
    print(client.user.id)
    print("Command prefix: "+cmdPrefix)
    print("Log folder: {0}, log file extension: {1}".format(logFolder, fileExt))
    print("-------------")
    if not(isdir(logFolder)):
        makedirs(logFolder)
        print("Created log folder: "+logFolder)
@client.event
async def on_message(message):
    try:
        i=0;msgContained=False;
        while i<len(avoidMsg):
            if(avoidMsg[i] in message.content):
                print("Avoiding message: {0} | By {1}".format(message.content.replace("\n"," "), message.author.name))
                msgContained=True
            i+=1
        if not(msgContained):
            Targetfile=join(logFolder,message.author.name+fileExt)
            MsgText=message.content.replace("\n"," ")+' '
            #open(Targetfile,'a').write(MsgText) #Replaced with aiofiles, for async support and support writing multiple files at a time.
            async with aiofiles.open(Targetfile, mode='a') as f:
                await f.write(MsgText)
            print('Wrote: "{0}" to "{1}"'.format(MsgText,str(Targetfile)))
    except Exception as e:
        print("Exception: "+str(e))
    
    if message.content.startswith(cmdPrefix+"ping"): #Used as a template for commands
        if(message.author.bot):
            return False
        print("Ping recieved, responding")
        counter = 0
        tmp = await client.send_message(message.channel, "Pong")
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

client.run(tokenKey)
