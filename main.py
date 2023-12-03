import discord
import sqlite3
import random
import time

conn = sqlite3.connect("most_useful.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user TEXT,
    lolis BIGINT,
    last_time_command_used INTEGER
)
""")
conn.commit()

intents = discord.Intents.default()
intents.message_content = True

with open("loli_gifs.txt", "r") as f:
    gifs = [el[:-1] for el in f.readlines()]

client = discord.Client(intents=intents)


def epic_random():
    out_of_bounds_chance = 0.2
    if random.random() <= out_of_bounds_chance:
        num = random.randint(-10, 15)
    else:
        num = random.randint(-5, 7)
    if num == 0:
        return 1
    else:
        return num


@client.event
async def on_ready():
    print(f'logged in as {client.user}')


@client.event
async def on_message(message):
    match message.content.split(" ")[0]:
        case '!help':
            await message.channel.send("Welcome to the loli bot! Here's the list of commands:\n\n`!loli` - get new lolis (every 12 hours)\n\n`!my_lolis` - see how many lolis you have\n\n`!top` - see the top 10 users with most lolis\n\nIdea by: Valpik; Bot by: cat dev")
        case '!loli':
            now = int(time.time())
            amount_delta = epic_random()
            check = cur.execute("SELECT * FROM users WHERE user=?", (message.author.name,)).fetchone()
            if check is None:
                old_amount = 0
                time_delta = 43200
                cur.execute("INSERT INTO users VALUES (?,?,?)", (message.author.name, 0, int(time.time())))
            else:
                time_delta = now - check[2]
                old_amount = check[1]
            if time_delta >= 43200:
                cur.execute("UPDATE users SET lolis=? WHERE user=?", (int(old_amount + amount_delta), message.author.name))
                conn.commit()
                await message.channel.send(f'{message.author.mention}, you got {amount_delta} new lolis!')
            else:
                await message.channel.send(f"{message.author.mention}, you can't get new lolis yet!")
            await message.channel.send(random.choice(gifs))
        case '!my_lolis':
            check = cur.execute("SELECT * FROM users WHERE user=?", (message.author.name,)).fetchone()
            if check is None:
                amount = 0
                cur.execute("INSERT INTO users VALUES (?,?,?)", (message.author.name, 0, 0))
            else:
                amount = check[1]
            await message.channel.send(f"{message.author.mention}, you've got {amount} lolis!")
        case '!top':
            top = cur.execute("SELECT * FROM users ORDER BY lolis DESC").fetchall()
            embed = discord.Embed(title='Top 10 users with most lolis:', colour=discord.Colour.from_rgb(30, 230, 30))
            if len(top) <= 10:
                lim = len(top)
            else:
                lim = 10
            for i in range(lim):
                embed.add_field(name=f'{i + 1}. {top[i][0]}: {top[i][1]} lolis', value='', inline=False)
            await message.channel.send(embed=embed)

client.run('idi nahuy')
