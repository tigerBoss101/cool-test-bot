"""
TUN News lightbulb plguin
"""

import datetime
import hikari
import lightbulb
import requests
from bs4 import BeautifulSoup


plugin = lightbulb.Plugin("TUN")


@plugin.command
@lightbulb.command("tun", "Gets the recent news from the TUN website")
@lightbulb.implements(lightbulb.SlashCommand)
async def tun(ctx: lightbulb.Context):
    url = "http://www.tun.ac.th/mainpage"
    headers = {
        "Cookie": "PHPSESSID=22q35sof30pq4alej91igk4tv2",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
        "Host": "www.tun.ac.th"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    news_list = soup.find("table", {"class", "news_index"})
    news_links = news_list.find_all("a", {"class": "link"})
    embed = hikari.Embed(title="TUN News",
                         description="The latest TUN news from the TUN website",
                         color=hikari.Color(0xff6da3),
                         timestamp=datetime.datetime.now().astimezone())
    for news in news_links:
        title = news["title"]
        link = news["href"]
        if not str(link).startswith("http://tun.ac.th/"):
            link = "http://tun.ac.th/" + link
        embed.add_field(title, link)
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)

