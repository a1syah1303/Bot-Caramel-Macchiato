import discord
from discord.ext import commands
from config import token

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

pelanggaran = []

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
        pelanggaran.append({
            "user_id": message.author.id,
            "username": str(message.author),
            "pesan": message.content,
            "waktu": message.created_at.isoformat()
        })

        try:
            await message.author.ban(reason="Mengirim tautan https://")
            await message.channel.send(
                f"{message.author} was banned for sending a link."
            )
        except discord.Forbidden:
            await message.channel.send(
                "The bot does not have permission to ban this user."
            )
        return

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        await channel.send(f'Selamat datang, {member.mention}!')

bot.run(token)