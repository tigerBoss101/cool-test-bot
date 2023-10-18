"""
Fun stuff lightbulb plguin
"""

import hikari
import lightbulb
import random

plugin = lightbulb.Plugin("Fun")


@plugin.command
@lightbulb.option(name="message", description="Message to give to the 8ball", type=str)
@lightbulb.command(name="8ball", description="Returns a fortune from 8ball")
@lightbulb.implements(lightbulb.SlashCommand)
async def eight_ball(ctx: lightbulb.Context):
    responses = ("I believe that it will",
                 "That will be unlikely",
                 "I disagree with that statement",
                 "That is likely to happen",
                 "There is a possibility that it will happen",
                 "I believe otherwise")
    selected = random.choice(responses)
    embed = hikari.Embed(title="8ball prediction", description="This is a fortune from the mighty 8ball")
    author = ctx.author
    author_img = (author.avatar_url or author.default_avatar_url).url
    embed.set_author(name=author.username, icon=author_img)
    embed.add_field(name="Prediction", value=ctx.options.message)
    embed.add_field(name="Fortune", value=selected)
    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.option(name="user", description="User to fetch avatar image from", type=hikari.User)
@lightbulb.command(name="avatar", description="Fetches avatar image from a user")
@lightbulb.implements(lightbulb.SlashCommand)
async def avatar(ctx: lightbulb.Context):
    user = ctx.options.user
    avatar_url = user.avatar_url or user.default_avatar_url
    avatar_img_data = await avatar_url.read()
    await ctx.respond(attachment=avatar_img_data)


@plugin.command
@lightbulb.command(name="random", description="Selects a random user from the server")
@lightbulb.implements(lightbulb.SlashCommand)
async def random_user(ctx: lightbulb.Context):
    guild = ctx.get_guild()
    members = [member for member in dict(guild.get_members()).values() if not member.is_bot]
    members.append(ctx.member)
    selected = random.choice(members)
    await ctx.respond(f"The chosen user is....\n{selected.mention}")


@plugin.command
@lightbulb.command(name="audit", description="Selects an amount of the latest audit events from the audit log")
@lightbulb.implements(lightbulb.SlashCommand)
async def audit(ctx: lightbulb.Context):
    audit_log = plugin.app.rest.fetch_audit_log(ctx.guild_id)
    async for event in audit_log.limit(5):
        print(event)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
