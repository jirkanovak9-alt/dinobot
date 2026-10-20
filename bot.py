import asyncio
from datetime import datetime, timedelta, timezone
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Zkratky map a zkrácené klíče pro bossy (cyber_dino, cyber_leader)
MAPS_DATA = {
    "gf": {
        "map_name": "Goldfields",
        "bosses": {
            "cyber_dino": {"name": "Cyber Dino", "cooldown": 180},
            "cyber_leader": {"name": "Cyber Bandit Leader", "cooldown": 180},
        },
    },
    "mw": {
        "map_name": "Mokon Woods",
        "bosses": {
            "cyber_dino": {"name": "Cyber Dino", "cooldown": 180},
            "cyber_leader": {"name": "Cyber Bandit Leader", "cooldown": 180},
        },
    },
    "gv": {
        "map_name": "Green Vulcano",
        "bosses": {
            "cyber_dino": {"name": "Cyber Dino", "cooldown": 180},
            "cyber_leader": {"name": "Cyber Bandit Leader", "cooldown": 180},
        },
    },
    "ccv": {
        "map_name": "Coldclaw Valley",
        "bosses": {
            "cyber_dino": {"name": "Cyber Dino", "cooldown": 180},
            "cyber_leader": {"name": "Cyber Bandit Leader", "cooldown": 180},
        },
    },
    "mm": {
        "map_name": "Maujak Mountains",
        "bosses": {
            "cyber_dino": {"name": "Cyber Dino", "cooldown": 180},
            "cyber_leader": {"name": "Cyber Bandit Leader", "cooldown": 180},
        },
    },
}


@bot.event
async def on_ready():
    print(f"Dino Storm Live Tracker ({bot.user.name}) is online!")


@bot.command()
async def kill(ctx, map_key: str.lower, boss_key: str.lower):
    """Register a boss kill with LIVE relative countdown."""
    if map_key not in MAPS_DATA:
        await ctx.send(
            f"❌ Invalid map shortcut! Use: **gf, mw, gv, ccv, mm**"
        )
        return

    map_info = MAPS_DATA[map_key]

    if boss_key not in map_info["bosses"]:
        await ctx.send(f"❌ Invalid boss! Use: **cyber_dino** or **cyber_leader**")
        return

    boss_info = map_info["bosses"][boss_key]
    cooldown = boss_info["cooldown"]
    boss_name = boss_info["name"]
    map_name = map_info["map_name"]

    # Výpočet živého odpočtu pro Discord
    now_utc = datetime.now(timezone.utc)
    spawn_time_utc = now_utc + timedelta(minutes=cooldown)
    timestamp = int(spawn_time_utc.timestamp())

    embed = discord.Embed(
        title=f"⏳ COUNTDOWN: {boss_name}", color=discord.Color.orange()
    )
    embed.add_field(name="📍 Map", value=map_name, inline=True)
    embed.add_field(
        name="⏰ Exact Respawn Time", value=f"<t:{timestamp}:t>", inline=True
    )
    embed.add_field(
        name="⏳ Live Countdown", value=f"**<t:{timestamp}:R>**", inline=False
    )
    embed.set_footer(
        text="Status will change automatically when boss spawns."
    )

    countdown_msg = await ctx.send(embed=embed)

    # Čekání 3 hodiny (180 minut)
    await asyncio.sleep(cooldown * 60)

    # Změna zprávy po respawnu
    spawned_embed = discord.Embed(
        title=f"🚨 SPAWNED: {boss_name}", color=discord.Color.green()
    )
    spawned_embed.add_field(name="📍 Map", value=map_name, inline=True)
    spawned_embed.add_field(
        name="⚠️ Status",
        value="**BOSS IS ALIVE NOW! GO GET IT!**",
        inline=False,
    )

    await countdown_msg.edit(embed=spawned_embed)


@bot.command()
async def bosses(ctx):
    """Displays all maps, shortcuts, and instructions."""
    embed = discord.Embed(
        title="📜 Dino Storm Boss List & Guide", color=discord.Color.blue()
    )

    # Výpis map a jejich zkratek
    for map_key, map_data in MAPS_DATA.items():
        boss_list = ""
        for boss_key, boss_data in map_data["bosses"].items():
            boss_list += (
                f"• {boss_data['name']} (`!kill {map_key} {boss_key}`)\n"
            )

        embed.add_field(
            name=f"🗺️ {map_data['map_name']} (Shortcut: `{map_key}`)",
            value=boss_list,
            inline=False,
        )

    # Nápověda / Bot commands sekce dole v embedu
    embed.add_field(
        name="⚙️ How to use commands",
        value=(
            "To report a killed boss, use the shortcut format:\n"
            "`!kill [map_shortcut] [boss_name]`\n\n"
            "**Examples:**\n"
            "• `!kill gf cyber_dino`\n"
            "• `!kill mw cyber_leader`\n\n"
            "**Map Shortcuts:** `gf`, `mw`, `gv`, `ccv`, `mm`\n"
            "**Bosses:** `cyber_dino`, `cyber_leader`"
        ),
        inline=False,
    )

    await ctx.send(embed=embed)


import os

bot.run(os.getenv("DISCORD_TOKEN"))