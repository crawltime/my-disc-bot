# Import discord modules
import discord
from discord.errors import HTTPException
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
import sys
import subprocess

# Local files import
from cringe_list import keklist, cringelist
from charactersay import *

# Quick variables
intents = discord.Intents.default()
intents.members = True

prefix = "!!"
bot = commands.Bot(
    command_prefix=prefix,
    intents=intents,

    allowed_mentions = discord.AllowedMentions(

        replied_user=False,
        users=False

        )
    )
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
    try:
        if ctx.command.name != "dm":
            await ctx.message.add_reaction("💯")
    except discord.NotFound:
        pass

@bot.event
async def on_command_error(ctx, error):

    random_emoji = [
        "❌",
        "⛔"
    ]

    random_choice = random.choice(random_emoji)

    await ctx.message.add_reaction(random_choice)
    print(f"\n{error}\n")
    await ctx.reply(error)

@bot.event
async def on_member_join(member):
    print(member)
    guild = member.guild
    if guild.system_channel is not None:
        await guild.system_channel.send(f"Welcome {member.mention}")

@cmd()
async def unixepoch(ctx):
    await ctx.reply(f"UTC: (normal)\n`{datetime.utcnow().timestamp():.4f}`\nGMT +2: (live tid)\n`{datetime.now().timestamp():.4f}`")

@cmd()
async def helloworld(ctx, member: discord.Member):
    await ctx.reply(f"Hello world, {member.mention}")

@cmd()
async def ping(ctx):
    time1 = time.monotonic()
    msg = await ctx.reply(f"ping{datetime.utcnow().timestamp()}")
    time2 = time.monotonic()

    result = time2 - time1

    await msg.edit(content=f"Web socket/Gateway: {bot.latency * 1000:.3f}ms\HTTP requests: {result * 1000:.3f}ms")

@cmd()
async def request (ctx, arg=None):
    if arg == None:
        await ctx.reply("No argument.")
    else:
        try:
            msg = await ctx.reply("Alright.")
            current_ip = session.get("http://ipecho.net/plain", timeout = 10)
            req = session.get(arg, timeout = 10)

            await msg.edit(content=f"Upstream URL: {arg}\nGot a: {req.status_code} response at crawl time.\nTor exit node: {current_ip.text}", suppress=True)
        
        except ConnectionError as error:
            await msg.edit(content=f"ConnectionError raised when trying to reply a GET request to site: `{arg}`.\nSite either timed out or failed to establish a connection.")
            print(f"\n{error}\n")
        
        except Exception as error:
            await ctx.reply(error)
            print(f"\n{error}\n")

@cmd()
async def amount(ctx):
    if ctx.guild.member_count != 1:
        await ctx.reply(f"There are {ctx.guild.member_count} members in this server.")
    else:
        await ctx.reply(f"There is {ctx.guild.member_count} member in this server.")

@cmd()
async def calc(ctx, arg1, method, arg2):
    try:
        arg1, arg2 = float(arg1), float(arg2)
        if method == "+":
            await ctx.reply(arg1 + arg2)
        elif method == "-":
            await ctx.reply(arg1 - arg2)
        elif method == "*" or method == "x":
            await ctx.reply(arg1 * arg2)
        elif method == "/":
            await ctx.reply(arg1 / arg2)
        elif method == "%":
            await ctx.reply(arg1 % arg2)
        else:
            await ctx.reply("405, method not allowed <:troll:836073348957863976>")
    except ValueError:
        await ctx.reply(f"You seemed to have entered a non numerical parameter. An example of the calc command looks like this: `{prefix}calc 2 + 2`")
    except ZeroDivisionError:
        await ctx.reply("You can't divide by 0")

@cmd()
async def myspace(ctx, arg=None):
    if arg == None:
        await ctx.reply(f"Missing ID parameter. Example: `{prefix}myspace 51703`")
    else:
        msg = await ctx.reply("Alright.")
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

            await msg.add_reaction("🗑️")
            #if ctx.message.author 

        except discord.HTTPException as httperror:
            await msg.edit(content="Message is too large.")

        os.remove(f"text_dumps/myspace_json_dump{current_time}.txt")

@cmd()
async def duck(ctx, arg=None):
    if arg == None:
        await ctx.reply("Missing search keyword.")
    else:
        diction = session.get(f"https://duckduckgo.com/?q={arg}&format=json&pretty=1").json()

        for k, v in diction["FirstURL"]:
            await ctx.reply("Key: {k}\t\tValue: {v}")

@cmd(name="cowsay", aliases=["tuxsay"])
async def _cowsay(ctx, *, arg=None):
    
    if arg != None:
        arg = arg.replace("—", "--")
    
    available_characters = ["tux", "cow", "daemon"]

    try:
        if arg != None:
            arg = arg.replace("```", "`")

        if arg == None or arg.startswith("--list", 0, 6) or arg.startswith("--help", 0, 6):
            send_string = ""
            for i in available_characters:
                send_string = send_string + f" {i}"

            send_string = send_string.strip()

            await ctx.reply(f"Available characters: `{send_string}`\nExample command 2: `{prefix}cowsay Yo!`\nExample command: `{prefix}cowsay --tux Hey!`")

        elif arg.startswith("--beastie", 0, 9) or arg.startswith("--daemon", 0, 8):
            if arg.startswith("--daemon"):
                arg = arg[9:]
                await ctx.reply(f"```{daemonsay(arg)}```")
            else:
                arg = arg[10:]
                await ctx.reply(f"```{daemonsay(arg)}```")

        elif arg.startswith("--tux", 0, 5):
            arg = arg[6:]
            await ctx.reply(f"```{tuxsay(arg)}```")

        elif arg.startswith("--cow", 0, 5):
            arg = arg[6:]
            await ctx.reply(f"```{cowsay(arg)}```")

        else:
            await ctx.reply(f"```{cowsay(arg)}```")

    except discord.HTTPException as excepterror:
        print(excepterror)
        await ctx.reply("Sorry, message was too large. (Over 2000 chars)")

@cmd()
async def translate(ctx, *, arg):
    rnd = randint(0, 1)
    
    if rnd == 0:
        msg = await ctx.reply("Alright.")
    else:
        msg = await ctx.reply("On it.")

    req = requests.post("https://libretranslate.com/translate", headers={"Content-Type": "application/json"}, json={
        "q": arg,
        "source": "en",
        "target": "es"
    })

    final = req.json()

    await msg.edit(content = final["translatedText"])

@cmd()
async def about(ctx):
    try:
        platform = sys.platform
        py_ver = sys.version
        kernel = str(subprocess.check_output(["uname", "-r"]))
        discordpy = discord.__version__


        await ctx.reply(f"Operating System: {platform}\nPython version: {py_ver}\nKernel: {kernel[2:-3]}\nDiscord.py version: {discordpy}")

    except FileNotFoundError as filerr:
        print(filerr)
        await ctx.reply("Error fetching system information.")

@cmd(aliases=["say"])
async def echo(ctx, *, echo):
    print(f"ID: <{ctx.message.author.id}>, {ctx.message.author} executed this message with the {prefix}echo command: {echo}")
    au = discord.AllowedMentions(users=True)
    await ctx.message.delete()
    await ctx.send(echo, allowed_mentions=au)

@cmd(aliases=["bin"])
async def binary(ctx, *, arg):
    try:
        arg = int(arg)
        arg = bin(arg)
        arg = arg.replace("0b", "**0b** ")
        await ctx.reply(arg)
    except ValueError:
        await ctx.reply(f"You seemed to have entered a non numerical parameter. An example of the binary converter command looks like this: `{prefix}bin 40`")
    except discord.HTTPException:
        await ctx.reply(f"Failed to send, message seems to be too long. (over 2000 chars)")

@cmd(aliases=["hexadecimal"], name="hex")
async def _hex(ctx, arg):
    try:
        arg = int(arg)
        arg = hex(arg)
        arg = arg.replace("0x", "**0x** ")
        await ctx.reply(arg)
    except ValueError:
        await ctx.reply(f"You seemed to have entered a non numerical parameter. An example of the hexadecimal converter command looks like this: `{prefix}hex 3735928559`")
    except discord.HTTPException:
        await ctx.reply(f"Failed to send, message seems to be too long. (over 2000 chars)")

@cmd()
async def sussy(ctx):
    files = os.listdir("sussy/")
    index = random.choice(files)
    
    await ctx.reply(file = discord.File("sussy/"+index))

@cmd(name="reply")
async def _reply(ctx):
    await ctx.reply(f"Hey {ctx.author.mention}")

@cmd(name="channel")
async def _channel(ctx, *, arg):
    channel = bot.get_channel(801305585446027274)
    await channel.send(arg)

@cmd(name="dm")
async def _dm(ctx, member: discord.Member, *, arg):
    if member == bot.user:
        await ctx.reply("Stfu")
    else:
        try:
            await member.send(f"{ctx.author.mention}Said:\n\n{arg}")
            await ctx.message.add_reaction(":troll:836073348957863976")
        except discord.HTTPException:
            await ctx.reply("Possible 400 status code, bad request. Did you try to send this to a bot user?")

@cmd()
async def rust(ctx, *, arg):
    msg = await ctx.reply("Trying with a POST request to: <https://play.rust-lang.org/execute>")
    try:
        if arg.startswith("```rs", 0, 5) and arg.endswith("```") or arg.startswith("```rust", 0, 7) and arg.endswith("```"):
            arg = arg.replace("```rs", "")
            arg = arg.replace("```rust", "")
            arg = arg.replace("```", "", -1)

        req = session.post("https://play.rust-lang.org/execute",
        json={
            "channel": "stable",
            "mode": "debug",
            "edition": "2018",
            "crateType": "bin",
            "tests": False,
            "code": arg,
            "backtrace": False})

        final = req.json()

        final_out = final["stdout"].replace("`", "´")
        final_err = final["stderr"].replace("`", "´")

        print(final_out + "\n" + final_err)
        if final["success"] == True:
            await msg.edit(content=f"Stdout: ```\n{final_out}```\nStderr: ```{final_err.strip()}```", suppress=True)
        elif final["success"] == False:
            await msg.edit(content=f"Error, no stdout:\n```{final_err}```", suppress=True)
        else:
            await msg.edit(content="Unexpected JSON recieved.")
    
    except discord.HTTPException:
        await msg.edit("HTTPException raised, message is probably too large (over 2000 characters) to send.")
    except Exception as excep:
        await msg.edit(f"Something went wrong.\n{excep}")


bot.run(shittytokenread)
