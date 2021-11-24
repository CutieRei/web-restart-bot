from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager
from discord.ext import commands
import bot
import sys
import importlib
import asyncio
import dotenv
import discord
import os

dotenv.load_dotenv()

token = os.environ["TOKEN"]

def start_bot(app):
    get_bot =  importlib.reload(sys.modules["bot"]).get_bot
    bot = get_bot()
    asyncio.create_task(bot.start(token))
    app.state.bot = bot
    return bot

async def stop_bot(bot: commands.Bot):
    if not bot.is_closed():
        await bot.close()
    

@asynccontextmanager
async def lifespan(app):
    bot = start_bot(app)
    await bot.wait_until_ready()
    yield
    await stop_bot(bot)

app = Starlette(debug=True, lifespan=lifespan)

@app.route("/restart", methods=["POST"])
async def restart(request: Request):
    auth_type, auth_token = request.headers["Authorization"].split(maxsplit=1)
    if auth_token != token or auth_type != "Bot":
        return JSONResponse({"status": "failed"}, 403)
    channel, message = int(request.query_params["channel"]), int(request.query_params["message"])
    await stop_bot(request.app.state.bot)
    bot = start_bot(request.app)
    await bot.wait_until_ready()
    channel = bot.get_channel(channel)
    if channel is not None:
        message = channel.get_partial_message(message)
        asyncio.create_task(message.reply("Finished restarting"))
    return JSONResponse({"status": "done"})

