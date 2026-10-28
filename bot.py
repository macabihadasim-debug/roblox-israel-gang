import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------------------------------------------------
# מחלקה לכפתור פתיחת טיקט אינטראקטיבי
# ------------------------------------------------------------------
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 פתח טיקט קבלה לגאנג", style=discord.ButtonStyle.green, custom_id="open_ticket_btn")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="🎫-טיקטים-לגאנג")
        
        # יצירת קטגוריה אם היא לא קיימת
        if not category:
            category = await guild.create_category("🎫-טיקטים-לגאנג")

        # הרשאות לחדר הפרטי
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        # יצירת ערוץ טקסט פרטי למועמד
        channel_name = f"ticket-{interaction.user.name}"
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        
        if existing_channel:
            await interaction.response.send_message(f"⚠️ כבר יש לך טיקט פתוח כאן: {existing_channel.mention}", ephemeral=True)
            return

        ticket_channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        
        await interaction.response.send_message(f"✅ הטיקט שלך נפתח בהצלחה! היכנס לכאן: {ticket_channel.mention}", ephemeral=True)
        
        # הודעה בתוך חדר הטיקט הפרטי
        embed = discord.Embed(
            title="⚔️ טיקט קבלה חדש – ROBLOX ISRAEL GANG",
            description=f"שלום {interaction.user.mention}! צוות הניהול יגיע אליך בקרוב.\n"
                        f"בינתיים, ספר לנו:\n1. בן כמה אתה?\n2. מה רמת ה-PVP שלך ברובלוקס?\n3. למה אתה רוצה להצטרף?",
            color=discord.Color.gold()
        )
        await ticket_channel.send(embed=embed)

# ------------------------------------------------------------------
# אירועים (EVENTS)
# ------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"🔥 הבוט האולטימטיבי {bot.user.name} מחובר ומוכן לפעולה!")
    activity = discord.Game(name="ROBLOX ISRAEL GANG ⚔️ | !help")
    bot.add_view(TicketView()) # טעינת הכפתורים למערכת

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="💬-צאט-כללי")
    if channel:
        embed = discord.Embed(
            title="👋 ברוך הבא למשפחה!",
            description=f"אהלן {member.mention}, הגעת לבית של **ROBLOX ISRAEL GANG**!\n📌 לך לקרוא את החוקים ותכין את הנשקים.",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)

# ------------------------------------------------------------------
# פקודות מידע
# ------------------------------------------------------------------
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="⚔️ תפריט פקודות הבוט", color=discord.Color.gold())
    embed.add_field(name="📜 !rules", value="חוקי השרת", inline=False)
    embed.add_field(name="👑 !roles", value="סולם הדרגות", inline=False)
    embed.add_field(name="🛒 !trade", value="מדריך מסחר", inline=False)
    embed.add_field(name="🎫 !panel", value="[למנהלים] שליחת לוח פתיחת טיקטים", inline=False)
    embed.add_field(name="🧹 !clear [כמות]", value="[למנהלים] מחיקת הודעות", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def rules(ctx):
    embed = discord.Embed(title="🚨 חוקי הברזל", description="1. כבוד הדדי\n2. משמעת בקרבות\n3. אין Combat Log\n4. סודיות מוחלטת", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command()
async def roles(ctx):
    embed = discord.Embed(title="👑 הדרגות בגאנג", description="Leader ➔ Underboss ➔ Capo ➔ Enforcer ➔ Gang Member ➔ Prospect", color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command()
async def trade(ctx):
    embed = discord.Embed(title="🛒 ערוץ המסחר", description="שלח הודעה בתבנית: [מוכר/קונה] | פריט | מחיר | תיוג", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def panel(ctx):
    """שולח את ההודעה עם הכפתור לפתיחת טיקטים לערוץ הנוכחי"""
    embed = discord.Embed(
        title="📥 רוצה להצטרף ל-ROBLOX ISRAEL GANG?",
        description="לחץ על הכפתור למטה כדי לפתוח טיקט קבלה פרטי מול הנהלת הגאנג!",
        color=discord.Color.blurple()
    )
    await ctx.send(embed=embed, view=TicketView())

# ------------------------------------------------------------------
# פקודות ניהול
# ------------------------------------------------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 נמחקו {amount} הודעות בהצלחה!")
    await msg.delete(delay=3)

# ⚠️ החלף את הטוקן בטוקן האמיתי שלך
TOKEN =MTU2NDk3NDYzNjU1NzQwMjEyMw.GJhg3S.DC4P2c0F6LpRHJlKgGzb_qcgrXY-elNcQGfBw4'
bot.run(TOKEN)