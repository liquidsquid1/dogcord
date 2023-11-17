from config import *
import nextcord
from nextcord.ext import commands
from nextcord.utils import get
import requests

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="dog!", intents=intents)

bot.remove_command('help')

async def callapi():
    return requests.get(API_CALL_URL).json()["message"]

@bot.command(name="cord")
async def cord(ctx):
    image_link = await callapi()
    reactions = ["👍", "👎", "▶", "❎", "❤️"]
    m = await ctx.send(image_link)
    await ctx.message.delete()
    for name in reactions:
        emoji = get(ctx.guild.emojis, name=name)
        await m.add_reaction(emoji or name)

@bot.command(name="help")
async def help(ctx):
    image_link = await callapi()
    helpembed = nextcord.Embed(title = HELP_Title, description = HELP_Description)
    helpembed.set_image(url = image_link)
    helpembed.add_field(name = "dog!cord", value = HELP_cord, inline=True)
    helpembed.add_field(name = "dog!api", value = HELP_api, inline=True)
    helpembed.add_field(name = "dog!help", value = HELP_help, inline=True)
    m = await ctx.send(embed = helpembed)
    reactions = ["❎"]
    for name in reactions:
        emoji = get(ctx.guild.emojis, name=name)
        await m.add_reaction(emoji or name)

@bot.command(name="api")
async def api(ctx):
    m = await ctx.send(API_MAN)
    reactions = ["❎"]
    for name in reactions:
        emoji = get(ctx.guild.emojis, name=name)
        await m.add_reaction(emoji or name)

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    await bot.change_presence(activity = nextcord.Activity(type=nextcord.ActivityType.playing, name = STATUS))

@bot.event
async def on_reaction_add(reaction, user):
    print(user)
    if user != bot.user:
        if reaction.message.author == bot.user:
            if reaction.emoji == "▶":
                await reaction.remove(user)
                image_link = await callapi()
                reactions = ["▶"]
                m = await reaction.message.edit(image_link)
                for name in reactions:
                    emoji = get(reaction.message.guild.emojis, name=name)
                    await m.add_reaction(emoji or name)
                for react in reaction.message.reactions:
                    await react.remove(user)
            if reaction.emoji == "❎":
                await reaction.message.delete()
            if reaction.emoji == "❤️":
                try:
                    await user.send(reaction.message.content)
                except nextcord.errors.Forbidden:
                    e = await reaction.message.channel.send(f"{user.mention} {ERROR_favourite_DM_closed}")
                    reactions = ["❎"]
                    for name in reactions:
                        emoji = get(e.guild.emojis, name=name)
                        await e.add_reaction(emoji or name)

if __name__ == '__main__':
    bot.run(TOKEN)