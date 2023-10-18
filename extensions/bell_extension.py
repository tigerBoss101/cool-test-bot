"""
Bell game lightbulb plguin
"""

import hikari
import lightbulb
import random


plugin = lightbulb.Plugin("bell")
bell_player: hikari.User | None = None
answer: int = 0


@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent):
    global bell_player
    author = event.author
    if bell_player is None or author != bell_player:
        return
    if event.message.content == str(answer):
        await event.message.respond("You are correct!")
    else:
        await event.message.respond(f"Sorry! The correct number of bells is {answer}")
    bell_player = None


@plugin.command
@lightbulb.command(name="bell", description="Play the bell game")
@lightbulb.implements(lightbulb.SlashCommand)
async def bell(ctx: lightbulb.Context):
    global answer
    global bell_player
    prompts = ["How many bells do I have?", "How many?", "How many bells?", "Now, how many bells?", "Now, how many?"]
    selected = random.choice(prompts)
    answer = len(selected.split())
    await ctx.respond("In this game, you have to guess how many bells I have.\n" + selected)
    bell_player = ctx.author


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
