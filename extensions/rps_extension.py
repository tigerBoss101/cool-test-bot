"""
Rock paper scissors lightbulb plugin
"""

import hikari
import lightbulb
from .rps import Game, Shape

plugin = lightbulb.Plugin("RPS")
games: dict[hikari.Snowflake, Game] = {}


@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent):

    member = event.member
    message = event.message
    content = event.content
    snowflake = member.id

    if snowflake not in games:
        return

    game = games[snowflake]
    try:
        user_choice = Shape[content.upper()]
    except KeyError:
        return
    embed = game.advance_round(user_choice)
    response_msg = await message.respond(embed=embed)
    if game.game_over:
        del games[snowflake]
    else:
        for emoji in Game.EMOJIS.values():
            await response_msg.add_reaction(emoji)


@plugin.listener(hikari.GuildReactionAddEvent)
async def on_reaction_add(event: hikari.GuildReactionAddEvent):

    message_id = event.message_id
    message = plugin.app.cache.get_message(message_id)
    member = event.member
    snowflake = member.id

    if snowflake not in games or message.author.id != 889752405237972993:
        return

    game = games[snowflake]

    for shape in Game.EMOJIS:
        if event.emoji_name == Game.EMOJIS[shape]:
            user_choice = shape
            break

    embed = game.advance_round(user_choice)
    response_msg = await message.respond(embed=embed)
    if game.game_over:
        del games[snowflake]
    else:
        for emoji in Game.EMOJIS.values():
            await response_msg.add_reaction(emoji)


@plugin.command
@lightbulb.command(name="rps", description="Rock Paper Scissors command group")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def rps(ctx):
    pass


@rps.child
@lightbulb.option("points", "The number of points you want to play to", int)
@lightbulb.command(name="play", description="Starts a Rock Paper Scissors against the computer", aliases=["rock-paper-scissors"])
@lightbulb.implements(lightbulb.SlashSubCommand)
async def play(ctx: lightbulb.Context):

    member = ctx.member
    snowflake = member.id

    if snowflake in games:
        embed = hikari.Embed(title="Rock Paper Scissors",
                             description="You have already started a game!")
        await ctx.respond(embed=embed)
        return

    game = Game(member, ctx.options.points)
    games[snowflake] = game
    response = await ctx.respond(embed=game.create_template_embed())
    message = await response.message()
    for reaction in Game.EMOJIS.values():
        await message.add_reaction(reaction)


@rps.child
@lightbulb.command(name="stop", description="Stops the current game of Rock Paper Scissors")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def stop(ctx: lightbulb.Context):

    member = ctx.member
    snowflake = member.id

    if snowflake not in games:
        embed = hikari.Embed(title="Rock Paper Scissors",
                             description="You aren't currently in a game!")
        await ctx.respond(embed=embed)
        return

    del games[snowflake]
    embed = hikari.Embed(title="Rock Paper Scissors",
                         description="Game stopped.")
    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.command(name="show_rps_game", description="Shows the Rock Paper Scissors game object")
@lightbulb.implements(lightbulb.SlashCommand)
async def show_rps_game(ctx: lightbulb.Context):

    await ctx.respond(games)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
