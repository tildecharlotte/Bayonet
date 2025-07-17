# /\/\/\/\/\/\/\
# IMPORTANT: MAKE SURE THIS TOKEN DOES NOT LEAK, YOU ARE FULLY REPONSIBLE SHOULD ANYTHING LEAK
token = 'x'

import discord
from discord.ext import commands
import logging
import asyncio
import sys
import re

print("Validating Token...")


# this fun stuff below makes the bot work
handler = logging.FileHandler(filename='bayonet.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', status=discord.Status.do_not_disturb, intents=intents)

# g check
async def check_token(token):
    try:
        temp_client = discord.Client(intents=discord.Intents.none())
        await temp_client.login(token)
        await temp_client.close()
        print("Token Validated. Loading Bayonet...")
        return True
    except discord.LoginFailure:
        print("Invalid token. Exiting...")
        return False
    except Exception as e:
        print(f"Exception occured. Output:{e}")
        return False


if not asyncio.run(check_token(token)):
    sys.exit(1)

# this HAS to be here because discord.py fucking sucks and tries to reinvent the wheel
bot.remove_command('help')

# regex patterns
# TODO: // ADD MORE SHIT HERE
patterns = {
    "twitter": re.compile(r"(https?://(?:www\.)?(?:x|twitter)\.com/\w+/status/\d+)"),
    "bsky": re.compile(r"(https?://(?:www\.)?bsky\.app/profile/[^/]+/post/[a-zA-Z0-9]+)"),
    "tiktok": re.compile(r"https?://(?:www\.)?tiktok\.com/@[^/]+/video/\d+"),
    "instagram": re.compile(r"https?://(?:www\.)?instagram\.com/(?:p|reel|tv|stories)/[^/]+"),
    "threads": re.compile(r"https?://(?:www\.)?threads\.net/@[^/]+/post/\d+"),
    "reddit": re.compile(r"https?://(?:www\.)?reddit\.com/r/[^/]+/comments/\w+"),
    "pixiv": re.compile(r"https?://(?:www\.)?pixiv\.net/en/artworks/\d+"),
    "deviantart": re.compile(r"https?://(?:www\.)?deviantart\.com/[^/]+/art/[^/?#]+-\d+"),
    "twitch": re.compile(r"https?://(?:www\.)?twitch\.tv/(?:videos/\d+|[^/]+/clip/[^/?#]+|[^/]+)"),
    "youtube": re.compile(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w\-]{11}"),
    "tumblr": re.compile(r"https?://(?:www\.)?[a-zA-Z0-9\-]+\.tumblr\.com/post/\d+"),
    "spotify": re.compile(r"https?://open\.spotify\.com/(?:track|album|playlist|show|episode)/[a-zA-Z0-9]+"),
    "bilibili": re.compile(r"https?://(?:www\.)?bilibili\.com/video/(?:BV|av)\w+"),
}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    converted_links = []

    for name, pattern in patterns.items():
        matches = pattern.findall(message.content)
        for match in matches:
            if name == "twitter":
                converted_links.append(match.replace("x.com", "vxtwitter.com").replace("twitter.com", "vxtwitter.com"))
            elif name == "bsky":
                converted_links.append(match.replace("bsky.app", "bskyx.app"))
            elif name == "tiktok":
                converted_links.append(match.replace("tiktok.com", "tiktokez.com"))
            elif name == "instagram":
                converted_links.append(match.replace("instagram.com", "instagramez.com"))
            elif name == "threads":
                converted_links.append(match.replace("threads.net", "fixthreads.net"))
            elif name == "reddit":
                converted_links.append(match.replace("reddit.com", "rxddit.com"))
            elif name == "pixiv":
                converted_links.append(match.replace("pixiv.net", "phixiv.net"))
            elif name == "deviantart":
                converted_links.append(match.replace("devianart.com", "fixdeviantart.com"))
            elif name == "twitch":
                converted_links.append(match.replace("www.twitch.tv", "fxtwitch.seria.moe"))
#            this... sucks, discords default embeds do a better job.
#            elif name == "youtube":
#                converted_links.append(match.replace("www.youtube.com", "koutu.be"))
            elif name == "tumblr":
                converted_links.append(match.replace("tumblr.com", "tpmblr.com"))
            elif name == "spotify":
                converted_links.append(match.replace("open.spotify.com", "open.fxspotify.com"))
            elif name == "bilibili":
                converted_links.append(match.replace("www.bilibili.com", "fxbilibili.seria.moe"))

    if converted_links:
        try:
            await message.edit(suppress=True) 
        except discord.HTTPException as e:
            print(f"Exception Occured: {e}")

        await message.reply("\n".join(converted_links))

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Bayonet loaded, logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Invalid Command",
            description="The command you are trying to use is invalid or has not been implemented yet.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        raise error



@bot.command()
async def help(ctx):
    embed = discord.Embed(
        description='Below are a list of (hopefully) helpful commands to get you started, the prefix for all commands is `.`',
        color=discord.Color.dark_blue()
    )
    embed.set_author(name="Help!")
    embed.add_field(name="Embeds", value="`No command necessary! Just paste your link, I will do the work for you.`", inline=False )
    embed.add_field(name="Silly", value="`to be announced`", inline=False)
    embed.add_field(name="Utility", value="`status` `ping` `whoami` `rapsheet` `ban` `sban` `dropkick` `skick` `dropkick` `timeout` `warn` `nuke` `github`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):
    embed = discord.Embed(
        title="Status",
        description="Bot Status:",
        color=discord.Color.orange()
        )
    embed.add_field(name="Connection to Discord:", value=":white_check_mark: Assuming cloudflare hasnt shat the bed.", inline=False)
    embed.add_field(name="Bayonet Backend", value=":white_check_mark: Fine", inline=False)
    embed.add_field(name="Your Connection", value=":x: Fucked", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    # note here the latency is fucked on purpose, you can just remove anything past * 1000 for the real results
    latency = round(bot.latency * 1000 * 400 / 2)
    embed = discord.Embed(
        title="Ping!",
        description=f"Bot operational. (**{latency}**ms)",
        color=discord.Color.dark_green()
    )
    await ctx.send(embed=embed)




bot.run(token, log_handler=handler, log_level=logging.DEBUG)
# /\/\/\/\/\/\/\
