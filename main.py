import os
import discord
import requests
from discord.ext import commands
from keep_alive import keep_alive  # Keeps bot alive on Replit

# Load bot token from environment variable
TOKEN = os.environ['DISCORD_TOKEN_PEAKFLOW']

# Your n8n webhook endpoint
N8N_WEBHOOK_URL = "https://peakflow.app.n8n.cloud/webhook/discord-bot"  # Replace with your real URL

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Handle DMs
    if isinstance(message.channel, discord.DMChannel):
        user_msg = message.content.strip()

        if user_msg.lower() == "test":
            await message.channel.send("work!")
            return

    # Handle public messages starting with !ask
    elif message.content.startswith("!ask "):
        user_msg = message.content[len("!ask "):].strip()

    else:
        return  # Ignore other messages

    # Send message to n8n
    payload = {
        "message": user_msg,
        "author": str(message.author),
        "channel_id": str(message.channel.id)
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        ai_reply = response.json().get("output", "I didn't understand that.")

        await message.channel.send(ai_reply, suppress_embeds=True)

    except Exception as e:
        print(f"Error sending to n8n: {e}")
        await message.channel.send(
            "There was an error contacting the AI agent.")

    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    await ctx.send("Bot is online and working.")


# Keep the bot alive on Replit
keep_alive()

# Start the bot
bot.run(TOKEN)
