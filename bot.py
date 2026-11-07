import discord
from discord.ext import commands
from config import token  # Import the bot's token from configuration file

intents = discord.Intents.default()
intents.members = True  # Allows the bot to work with users and ban them
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def start(ctx):
    await ctx.send("Hi! I'm a chat manager bot!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("It is not possible to ban a user with equal or higher rank!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"User {member.name} was banned.")
    else:
        await ctx.send("This command should point to the user you want to ban. For example: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have sufficient permissions to execute this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.guild and "https://" in message.content:
        try:
            await message.author.ban(reason="Mengirim tautan https://")
            await message.channel.send(
                f"{message.author} dicekal karena mengirim tautan."
            )
        except discord.Forbidden:
            await message.channel.send("Bot tidak punya izin untuk mencekal anggota.")
        return

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        await channel.send(f"Selamat datang, {member.mention}!")

bot.run(token)
