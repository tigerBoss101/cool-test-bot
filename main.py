"""
Main bot
"""

import hikari
import lightbulb
import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
BOT_TESTING_GUILD_ID = 889751389100732477
FRIENDS_GUILD_ID = 946326321963876392
GUILD_IDS = (BOT_TESTING_GUILD_ID, FRIENDS_GUILD_ID, 991990720959348796, 990234271258116106)
bot = lightbulb.BotApp(token=token, default_enabled_guilds=GUILD_IDS)
bot_testing_guild = bot.cache.get_guild(BOT_TESTING_GUILD_ID)


@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print("Bot has started!")
    latency = round(bot.heartbeat_latency * 1000, 2)
    print(f"Latency: {latency}ms")
    activity = hikari.Activity(name="Being a test subject")
    await bot.update_presence(activity=activity)


@bot.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("filename", "The name of the file", str)
@lightbulb.command("load", "loads an extension")
@lightbulb.implements(lightbulb.SlashCommand)
async def load(ctx: lightbulb.Context):
    bot.load_extensions(f"extensions.{ctx.options.filename}")
    await ctx.respond(f"{ctx.options.filename} has been loaded!", delete_after=True)


@bot.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("filename", "The name of the file", str)
@lightbulb.command("unload", "unloads an extension")
@lightbulb.implements(lightbulb.SlashCommand)
async def unload(ctx: lightbulb.Context):
    bot.unload_extensions(f"extensions.{ctx.options.filename}")
    await ctx.respond(f"{ctx.options.filename} has been unloaded!", delete_after=True)


@bot.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("filename", "The name of the file", str)
@lightbulb.command("reload", "reloads an extension")
@lightbulb.implements(lightbulb.SlashCommand)
async def reload(ctx: lightbulb.Context):
    bot.reload_extensions(f"extensions.{ctx.options.filename}")
    await ctx.respond(f"{ctx.options.filename} has been reloaded!", delete_after=True)


def main():
    for filename in Path(".").glob("extensions/*.py"):
        if "extension" in filename.stem:
            bot.load_extensions(f"extensions.{filename.stem}")

    bot.run()


if __name__ == "__main__":
    main()
