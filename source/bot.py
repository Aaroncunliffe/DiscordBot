
import discord
import asyncio
import json
import datetime
import random


emptyjson = """
{ 
    "quotes": 
    {
        "0": {
            "addedby": "Zygon#0549",
            "content": "Yes, Arrays start at 0 and this quote has to be here to save me a lot of hassle, (devquote) - Aaron",
            "dateadded": "2017-08-23"
        }
    } 
}
"""

client = discord.Client()

def UpdateDB(jsonData, filename):
    with open(filename, 'w') as outfile:
        json.dump(jsonData, outfile, sort_keys=True, indent=4, ensure_ascii=False)

def AddRecord(json, addedBy, quote, dateAdded):
    length = len(json["quotes"])
    json["quotes"].update({"" + str(length) + "":
        {"addedBy":"" + str(addedBy) + "",
        "content":"" + str(quote) +"",
        "dateadded":"" + str(dateAdded) + ""
        }})
    return length

def AddRecordWithName(json, name, addedBy, quote, dateAdded):
    json["quotes"].update({"" + name + "":
        {"addedBy":"" + str(addedBy) + "",
        "content":"" + str(quote) +"",
        "dateadded":"" + str(dateAdded) + ""
        }})


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    for s in client.servers:
        filename = str(s) + ".json"
        try:
            with open(filename) as file:
                print("") # Stop indentation error...
        # do whatever
        except IOError: # File not created
            print("No store exists for {}, creating now".format(str(s)))
            if filename == "/r/nintendoswitch.json":
                return
            with open(filename, 'w') as outfile:
                parsed = json.loads(emptyjson)
                json.dump(parsed, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

@client.event
async def on_message(message):

    if message.author == client.user: # don't process messages sent by the bot
        return

    if message.content.startswith("!addquotewithname"):
        await AddQuoteWithName(message)

    elif message.content.startswith("!addquote"):
        await AddQuote(message)

    elif message.content == "!quote": # Grabs a random quote
        await SayRandomQuote(message)

    elif message.content.startswith("!quoteaddedby"):
        await WhoAddedQuote(message)

    elif message.content.startswith("!quote"):
        await SayQuote(message)

    elif message.content.startswith("!joinedwhen"):
        await SayWhenUserJoined(message)

    elif message.content.startswith("!popcorn"):
        await client.send_message(message.channel, "https://cdn.discordapp.com/attachments/129532002369142784/296736094966513675/6JfRpb7.png")
        
    elif message.content.startswith("!help"):
        await client.send_message(message.channel, 
            "!addquote - Add a quote to be stored \n" +
            "!addquotewithname - Add a quote to be stored that can be retrieved by name \n" +
            "!quote - get random quote stored with number only \n" +
            "!quote X - where X is the specific number of the quote \n" +
            "!quoteaddedby - retrieves what user added which quote \n"  )


async def AddQuote(message):
    with open(str(message.server) + ".json", 'r') as infile:
        parsed_json = json.load(infile)

    quote = message.content.replace("!addquote ", "") # remove the command from the message
    length = AddRecord(parsed_json, message.author, quote, message.timestamp.date()) # Update local variable holding json
    UpdateDB(parsed_json, str(message.server) + ".json") # Rewrite to file
    await client.send_message(message.channel, "quote {} added".format(length))

async def AddQuoteWithName(message):
    with open(str(message.server) + ".json", 'r') as infile:
        parsed_json = json.load(infile)

    quote = message.content.replace("!addquotewithname ", "") # remove the command from the message
    name = quote.split(' ')[0]
    quote = quote.replace(name + " ", "")
    length = AddRecordWithName(parsed_json, name, message.author, quote, message.timestamp.date()) # Update local variable holding json
    UpdateDB(parsed_json, str(message.server) + ".json") # Rewrite to file
    await client.send_message(message.channel, "quote '{}' added".format(name))

async def SayQuote(message):
    data = message.content.replace("!quote ", "")
    try:
        with open(str(message.server) + ".json", 'r') as infile:
            parsed_json = json.load(infile)
        quotenum = int(data)
        if quotenum > len(parsed_json["quotes"]):
            print(len(parsed_json["quotes"]))
            await client.send_message(message.channel, "Number too large, there are {} quotes".format(len(parsed_json["quotes"]) - 1))
            return
        await client.send_message(message.channel, parsed_json["quotes"][str(quotenum)]["content"])
    except ValueError:
        try:
            await client.send_message(message.channel, parsed_json["quotes"][data]["content"])
        except KeyError:
            await client.send_message(message.channel, "Error - No quote match that number or name")

async def SayRandomQuote(message):
    with open(str(message.server) + ".json", 'r') as infile:
        parsed_json = json.load(infile)
    num = random.randint(1, len(parsed_json["quotes"]) - 1)
    await client.send_message(message.channel, "quote " + str(num) + ": " + parsed_json["quotes"][str(num)]["content"])

async def WhoAddedQuote(message):
    data = message.content.replace("!quoteaddedby", "")
    try:
        with open(str(message.server) + ".json", 'r') as infile:
            parsed_json = json.load(infile)
        quotenum = int(data)
        if quotenum > len(parsed_json["quotes"]):
            print(len(parsed_json["quotes"]))
            await client.send_message(message.channel, "Number too large, there are {} quotes".format(len(parsed_json["quotes"]) - 1))
            return
        await client.send_message(message.channel, parsed_json["quotes"][str(quotenum)]["addedby"])
    except ValueError:
        await client.send_message(message.channel, "Error - quote requested must be by number")

async def SayWhenUserJoined(message):
     await client.send_message(message.channel, "{} joined on {}".format(message.author, message.author.joined_at.date()))


####################################################
client.run("INSERTTOKENHERE")