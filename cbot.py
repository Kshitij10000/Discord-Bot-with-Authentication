import mysql.connector
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

prefix = "!"
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
token = "MTE4NDQ3NDUyOTU4Njc0OTQ3MQ.Gohpkb.7k2fV7qpEvz4_raAc1xFl2GQrP6BpWult4gBtc"

# MySQL Database Connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qwerty@123",
    database="cbot"
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='hello')
async def hello(ctx, auth_token=""):
    sender_name = ctx.author.name
    server_name = ctx.guild.name
  # Check if auth_token is provided
    if not auth_token:
        await ctx.send('Please provide an authentication token with the !hello command.')
        return

    # Check if the provided auth_token is valid for the server_id
    if is_valid_token(server_name, auth_token):
        await ctx.send(f'Hello world {sender_name} to {server_name}!')
    else:
        await ctx.send('Authentication token not found or invalid.')

def is_valid_token(server_name, auth_token):
    try:
        cursor = db_connection.cursor()
        # Check if the auth_token exists for the provided server_name
        cursor.execute("SELECT * FROM auth_tokens WHERE server_name = %s AND auth_token = %s",
                       (server_name, auth_token))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"Error checking token validity: {e}")
        return False
    finally:
        cursor.close()


bot.run(token)
