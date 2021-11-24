from discord.ext import commands
import discord
import aiohttp
import asyncio

def get_bot():
    bot = commands.Bot(command_prefix="example.")

    @bot.listen()
    async def on_ready():
        print(f"Logged in as {bot.user}")

    async def _worker(ctx, port):
        async with aiohttp.ClientSession() as sess:
            await sess.post(f"http://localhost:{port}/restart",     headers={"Authorization": f"Bot {bot.http.token}"}, params={"channel": ctx.channel.id, "message": ctx.message.id})

    @bot.command()
    @commands.is_owner()
    async def restart(ctx):
        await ctx.send("Restarting...")
        with open("port") as f:
            port = f.read()
        asyncio.create_task(_worker(ctx, port))
    return bot
