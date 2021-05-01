# Import discord modules
import discord
from discord.ext import commands

# Misc
import os
import requests
import json
from requests.exceptions import *
from random import *
import random
import time
from datetime import datetime
import asyncio

# Local files import
from cringe_list import keklist, cringelist
from charactersay import *

# Quick variables
prefix = "!!"
bot = commands.Bot(command_prefix=prefix)
cmd = bot.command

# Import token
with open("token.txt", "r") as shittytoken:
    shittytokenread = shittytoken.read()

# ----------------------------------------- #
#                                           #

# Tor daemon proxy
session = requests.session()
session.proxies = {
    "http": "socks5h://localhost:9050",
    "https": "socks5h://localhost:9050"
}

# ----------------------------------------- #

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("The prefix is:", prefix)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{bot.users} idiots | {prefix}help"), status=discord.Status.do_not_disturb)

@bot.before_invoke
async def invoke_before_command(ctx):

    random_emoji = [
        "👌",
        "🆗"
    ]

    random_choice = random.choice(random_emoji)

    await ctx.message.add_reaction(random_choice)

@bot.event # on_command_completion
async def on_command_completion(ctx):
    await ctx.message.add_reaction("💯")

@bot.event
async def on_command_error(ctx, error):

    random_emoji = [
        "❌",
        "⛔"
    ]

    random_choice = random.choice(random_emoji)

    await ctx.message.add_reaction(random_choice)
    print(f"\n{error}\n")
    await ctx.send(error)

@cmd()
async def unixepoch(ctx):
    await ctx.send(f"UTC: (normal)\n`{datetime.utcnow().timestamp():.4f}`\nGMT +2: (live tid)\n`{datetime.now().timestamp():.4f}`")

@cmd()
async def helloworld(ctx):
    await ctx.send("Hello world")

@cmd()
async def ping(ctx):
    time1 = time.monotonic()
    msg = await ctx.send(f"ping{datetime.utcnow().timestamp()}")
    time2 = time.monotonic()

    result = time2 - time1

    await msg.edit(content=f"Web socket/Gateway: {bot.latency * 1000:.3f}ms\nPing between message: {result * 1000:.3f}ms")

@cmd()
async def randomcringe(ctx, arg=None):
    print(arg)

    if arg == "--help":
        await ctx.send("""You can either execute the command with **kek**/**cringe** as parameters which will force the bot to print a kek or cringe video respectively. Or you could execute it with no parameters which will print a random one between those two "catagories".""")
        List = None

    if arg != None:
        arg = arg.lower()

    if arg == "kek":
        List = 0
    
    elif arg == "cringe":
        List = 1

    if arg == None:
        List = randint(0, 1)

    if List == 0:
        choice = random.choice(keklist)
        choice = "cringetiktoks/" + choice
        await ctx.send(f"You got **kek**!!!! Enjoy 😀😂😂😂😂😱😱\n{choice[14:]}")
        await ctx.send(file=discord.File(choice))

    elif List == 1:
        choice = random.choice(cringelist)
        choice = "cringetiktoks/" + choice
        await ctx.send(f"I'm sorry but 😫, y-you got **cringe**. 😞😔😔\n{choice[14:]}")
        await ctx.send(file=discord.File(choice))

@cmd()
async def request (ctx, arg=None):
    if arg == None:
        await ctx.send("No argument.")
    else:
        try:
            msg = await ctx.send("Alright.")
            current_ip = session.get("http://ipecho.net/plain", timeout = 10)
            req = session.get(arg, timeout = 10)

            await msg.edit(content=f"Upstream URL: {arg}", suppress=True)

            await ctx.send(f"Got a: {req.status_code} response at crawltime.\nTor exit node: {current_ip.text}")
        
        except ConnectionError as error:
            await msg.edit(content=f"ConnectionError raised when trying to send a GET request to site: `{arg}`.\nSite either timed out or failed to establish a connection.")
            print(f"\n{error}\n")
        
        except Exception as error:
            await ctx.send(error)
            print(f"\n{error}\n")

        
@cmd()
async def amount(ctx):

    if ctx.guild.member_count != 1:
        await ctx.send(f"There are {ctx.guild.member_count} members in this server.")
    else:
        await ctx.send(f"There is {ctx.guild.member_count} member in this server.")

@cmd()
async def calc(ctx, arg1, method, arg2):
    try:
        arg1, arg2 = float(arg1), float(arg2)
        if method == "+":
            await ctx.send(arg1 + arg2)
        elif method == "-":
            await ctx.send(arg1 - arg2)
        elif method == "*" or method == "x":
            await ctx.send(arg1 * arg2)
        elif method == "/":
            await ctx.send(arg1 / arg2)
        elif method == "%":
            await ctx.send(arg1 % arg2)
        else:
            await ctx.send("405, method not allowed <:troll:836073348957863976>")
    except ValueError:
        await ctx.send(f"You seemed to have entered a non numerical parameter. An example of the calc command looks like this: `{prefix}calc 2 + 2`")
    except ZeroDivisionError:
        await ctx.send("You can't divide by 0")

@cmd()
async def myspace(ctx, arg=None):
    if arg == None:
        await ctx.send(f"Missing ID parameter. Example: `{prefix}myspace 51703`")
    else:
        msg = await ctx.send("Alright.")
        try:
            diction = session.get("https://myspace.windows93.net/api.php?id="+arg).json()

            current_time = str(datetime.now().timestamp())
            current_time = current_time.replace(".", "")
            
            for k, v in diction.items():

                with open(f"text_dumps/myspace_json_dump{current_time}.txt", "a") as dump:
                    dump.write(f"Key: {k}\t\t\tValue: {v}\n")
            
            with open(f"text_dumps/myspace_json_dump{current_time}.txt", "r") as message:
                message = message.read()

            await msg.edit(content=f"""```json
{message}```""", suppress=True)

        except discord.HTTPException as httperror:
            await msg.edit(content="Message is too large.")

        os.remove(f"text_dumps/myspace_json_dump{current_time}.txt")

@cmd()
async def duck(ctx, arg=None):
    if arg == None:
        await ctx.send("Missing search keyword.")
    else:
        diction = session.get(f"https://duckduckgo.com/?q={arg}&format=json&pretty=1").json()

        for k, v in diction["FirstURL"]:
            await ctx.send("Key: {k}\t\tValue: {v}")

@cmd(name="cowsay", aliases=["tuxsay"])
async def _cowsay(ctx, *, arg):
    
    available_characters = ["tux", "cow", "daemon"]

    try:
        if arg.startswith("--help", 0, 6):
            send_string = ""
            for i in available_characters:
                send_string = send_string + f" {i}"

            send_string = send_string.strip()

            await ctx.send(f"Available characters: `{send_string}`\nExample command 2: `{prefix}cowsay Yo!`\nExample command: `{prefix}cowsay --tux Hey!`")

        elif arg.startswith("--beastie", 0, 9) or arg.startswith("--daemon", 0, 8):
            if arg.startswith("--daemon"):
                arg = arg[9:]
                await ctx.send(f"```{daemonsay(arg)}```")
            else:
                arg = arg[10:]
                await ctx.send(f"```{daemonsay(arg)}```")

        elif arg.startswith("--tux", 0, 5):
            arg = arg[6:]
            await ctx.send(f"```{tuxsay(arg)}```")

        elif arg.startswith("--cow", 0, 5):
            arg = arg[6:]
            await ctx.send(f"```{cowsay(arg)}```")

        else:
            await ctx.send(f"```{cowsay(arg)}```")

    except discord.HTTPException as excepterror:
        print(excepterror)
        await ctx.send("Sorry, message was too large. (Over 2000 chars)")

@cmd()
async def translate(ctx, *, arg):

    # Add so you can choose target and source translations

    rnd = randint(0, 1)
    
    if rnd == 0:
        msg = await ctx.send("Alright.")
    else:
        msg = await ctx.send("On it.")

    req = requests.post("https://libretranslate.com/translate", headers={"Content-Type": "application/json"}, json={
        "q": arg,
        "source": "en",
        "target": "es"
    })

    final = req.json()

    await msg.edit(content = final["translatedText"])

bot.run(shittytokenread)
