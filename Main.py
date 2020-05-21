import requests
import discord
from discord.ext import commands
import json

client = commands.Bot(command_prefix=">")
client.remove_command("help")
file1 = "already_used_keys.json"
file2 = "whitelisted_users.json"
Bot_Name = "Bot_Name"


def add_key(key, user):
    _ret = False
    data_tx_read = open(file1, "r").read()
    to_json = json.loads(data_tx_read)
    data_tx_read2 = open(file2, "r").read()
    to_json2 = json.loads(data_tx_read2)

    if not (key in to_json) and not (user in to_json2):
        key_data = {key: ''}
        username_data = {user: ''}
        to_json.update(key_data)
        to_json2.update(username_data)
        _ret = "You have been whitelisted, use '>getrole' in the discord to get the 'Buyer' role!"
    elif user in to_json2:
        _ret = "You are already whitelisted!"
    elif key in to_json:
        _ret = "Key has already been redeemed!"

    old = str(to_json).replace("'", '"')
    open(file1, "w").close()
    open(file1, "w").write(old)

    old2 = str(to_json2).replace("'", '"')
    open(file2, "w").close()
    open(file2, "w").write(old2)
    return _ret


@client.event
async def on_ready():
    print("Bot is ready!")


@client.command(pass_context=True)
async def ping(ctx):
    await ctx.send("> `Pong! " + str(round(client.latency * 1000)) + "ms`")


@client.command(pass_context=True)
async def redeem(ctx, key=""):
    if key == "":
        await ctx.send("> `Missing Arg {Key}`")
    else:
        data_tx_read = open(file1, "r").read()
        to_json = json.loads(data_tx_read)
        key_list = requests.get(
            "http://gameovers.net/Scripts/Paid/ABDMUniversal/4chdqwPEmOk2mPbaZHl4/usedWhitelistKeys.txt").text.split(
            "\n")
        if str(key) in key_list and str(key) in to_json:
            await ctx.send("> `Key has already been redeemed!`")
        elif str(key) in key_list:
            response = add_key(str(key), str(ctx.message.author.id))
            await ctx.send("> `" + response + "`")
        else:
            await ctx.send("> `Invalid Key.`")


@client.command(pass_context=True)
async def getrole(ctx):
    data_tx_read = open(file2, "r").read()
    to_json = json.loads(data_tx_read)

    if str(ctx.message.author.id) in to_json and not("Direct Message with" in str(ctx.message.channel)):
        member = ctx.message.author
        role = discord.utils.get(member.guild.roles, name="Buyer")
        await member.add_roles(role)

        await ctx.send("> `You have been given buyer role!`")
    elif "Direct Message with" in str(ctx.message.channel):
        await ctx.send("> `Please use this command in the discord server!`")
    else:
        await ctx.send("> `You aren't authorized to use this command!`")


client.run("NjY2NzY5Nzg4NTk2NTE4OTQy.XsMFIQ.rCS0amTRPrEZykFDPLtnetYfMHY")
