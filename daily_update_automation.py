import discord
import asyncio
import json

# Specify the path to your JSON file
path_to_token = 'discord_token.json'

# Open the JSON file and load its contents
with open(path_to_token, 'r') as file:
    data = json.load(file)

TOKEN = data['token']
SERVER_ID = "1007198475642994768"
CHANNEL_ID = "1120657824947634317"
THREAD_ID = "1171697957775609937"

# Initialize bot
client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

async def send_message(thread_id: int, channel_id: int, server_id: int, message: str):
    try:
        # Fetch the server
        server = await client.fetch_guild(server_id)
        if server is None:
            print(f"Server with ID {server_id} not found.")
            return
        
        # Fetch the channel
        channel = await server.fetch_channel(channel_id)
        if channel is None:
            print(f"Channel with ID {channel_id} not found in server {server.name}.")
            return

        # Fetch the thread
        thread = await channel.fetch_thread(thread_id)
        if thread is None:
            print(f"Thread with ID {thread_id} not found in channel {channel.name}.")
            return

        # Send the message to the thread
        await thread.send(message)
        print(f"Message sent to thread {thread_id} in channel {channel.name}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the bot
async def main():
    await client.start(TOKEN)
    await send_message(
        thread_id=THREAD_ID, 
        channel_id=CHANNEL_ID, 
        server_id=SERVER_ID, 
        message="Test Message"
    )
    await asyncio.sleep(5)  # Wait for 5 seconds before closing the connection
    await client.close()

asyncio.run(main())
