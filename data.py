from discord.utils import get

CLASSES = ['warrior', 'paladin', 'shadowknight', 'rogue', 'ranger', 'monk', 'enchanter', 'magician', 'necromancer',
           'wizard', 'druid', 'shaman', 'bard', 'cleric']

ROLE_CLASSES = {
    'tank': ['warrior', 'paladin', 'shadowknight'],
    'melee': ['rogue', 'ranger', 'monk'],
    'caster': ['enchanter', 'magician', 'necromancer', 'wizard'],
    'support': ['druid', 'shaman', 'bard'],
    'healer': ['cleric']
}

ROLE_INDEX = {
    'tank': 1,
    'melee': 5,
    'caster': 9,
    'support': 16,
    'healer': 20,
    'warrior': 2,
    'paladin': 3,
    'shadowknight': 4,
    'rogue': 6,
    'ranger': 7,
    'monk': 8,
    'enchanter': 10,
    'magician': 11,
    'necromancer': 13,
    'wizard': 14,
    'druid': 17,
    'shaman': 18,
    'bard': 19,
    'cleric': 21
}

secondary_txt = "\n\n*__Alternatives__*\n"

def get_embed_outline(msg, title="Raid Signup"):
    return {
        "title": title,
        "footer": {"text": f"""Started by {msg.author}"""},
        "fields": [
            {"name": "\u200b",
             "value": "**__Total Players__: `0`**",
             # "value": "**0** Tanks　　**0** Melee　　**0** Casters　　**0** Support　　**0** Healers"
             },

            {"name": "\u200b",
             "value": "--------------------------🛡️ TANKS `0 | 0` 🛡️--------------------------"},

            {"name": f"{get(msg.guild.emojis, name='warrior')} __Warrior__ (0)",
             "value": "None",
             "inline": True},
            {"name": f"{get(msg.guild.emojis, name='paladin')} __Paladin__ (0)",
             "value": "None",
             "inline": True},
            {"name": f"{get(msg.guild.emojis, name='shadowknight')} __Shadowknight__ (0)",
             "value": "None",
             "inline": True},

            {"name": "\u200b",
             "value": "--------------------------⚔️ MELEE `0 | 0` ⚔️--------------------------"},

            {"name": f"{get(msg.guild.emojis, name='rogue')} __Rogue__ (0)",
             "value": "None",
             "inline": True},
            {"name": f"{get(msg.guild.emojis, name='ranger')} __Ranger__ (0)",
             "value": "None",
             "inline": True},
            {"name": f"{get(msg.guild.emojis, name='monk')} __Monk__ (0)",
             "value": "None",
             "inline": True},

            {"name": "\u200b",
             "value": "--------------------------🪄 CASTERS `0 | 0` 🪄--------------------------"},

            {"name": f"{get(msg.guild.emojis, name='enchanter')} __Enchanter__ (0)",
             "value": "None",
             "inline": True},
            {"name": f"{get(msg.guild.emojis, name='magician')} __Magician__ (0)",
             "value": "None",
             "inline": True},
            {"name": "\u200b",
             "value": "\u200b",
             "inline": True},
            {"name": f"{get(msg.guild.emojis, name='necromancer')} __Necromancer__ (0)",
             "value": "None",
             "inline": True},
            {"name": f"{get(msg.guild.emojis, name='wizard')} __Wizard__ (0)",
             "value": "None",
             "inline": True},
            {"name": "\u200b",
             "value": "\u200b",
             "inline": True},

            {"name": "\u200b",
             "value": "--------------------------💪 SUPPORT `0 | 0` 💪--------------------------"},

            {"name": f"{get(msg.guild.emojis, name='druid')} __Druid__ (0)",
             "value": "None",
             "inline": True},
            {"name": f"{get(msg.guild.emojis, name='shaman')} __Shaman__ (0)",
             "value": "None",
             "inline": True},
            {"name": f"{get(msg.guild.emojis, name='bard')} __Bard__ (0)",
             "value": "None",
             "inline": True},

            {"name": "\u200b",
             "value": "--------------------------❤️ HEALERS `0 | 0` ❤️--------------------------"},

            {"name": f"{get(msg.guild.emojis, name='cleric')} __Cleric__ (0)",
             "value": "None"},
        ]
    }