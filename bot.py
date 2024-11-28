import discord
from openai import OpenAI
import os

# Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
discord_token = os.getenv("DISCORD_BOT_TOKEN")

# Instantiate OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

# Set up Discord bot intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "hello":
        await message.channel.send("Hello! I'm alive and ready to help!")

    if message.content.lower().startswith("ai"):
        user_input = message.content[3:].strip()

        try:
            # Call OpenAI chat API
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send(f"Error: {e}")

client.run(discord_token)

