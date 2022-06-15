import discord
import json
import logging
from datetime import datetime
import re
import data
from data import CLASSES, ROLE_CLASSES, ROLE_INDEX, get_embed_outline


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('./venv/config.json') as file:
    config = json.load(file)
TOKEN = config['token']

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content
    if content.startswith("!raid"):
        roles = message.guild.roles
        role_names = [role.name for role in roles]
        tags = []
        for cmd in content.split(" "):
            if cmd.startswith("--") and cmd[2:] in role_names:
                i = role_names.index(cmd[2:])
                tags.append(roles[i].mention)
                content = content.replace(cmd, "")

        title = content.replace("!raid", "").replace("--everyone", "").strip()
        if not title:
            embed = discord.Embed().from_dict(get_embed_outline(message))
        else:
            embed = discord.Embed().from_dict(get_embed_outline(message, title))

        embed.timestamp = datetime.utcnow()

        raid_msg = await message.channel.send(" ".join(tags), embed=embed)
        for emoji in client.emojis:
            if emoji.name in CLASSES:
                await raid_msg.add_reaction(emoji)


@client.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    if user != client.user and msg.author == client.user:
        is_primary = not any(user.display_name in field.value.split("\n") for field in msg.embeds[0].fields)
        await add_remove_user_role(msg, reaction.emoji.name, user, is_primary, True)


@client.event
async def on_reaction_remove(reaction, user):
    print("called remove rxn")
    msg = reaction.message
    if user != client.user and msg.author == client.user and reaction.emoji.name in CLASSES:
        # users = [u for field in msg.embeds[0].fields for u in field.value.split("\n")]
        users_for_rxn = msg.embeds[0].fields[ROLE_INDEX[reaction.emoji.name]].value
        if "*__Alternatives__*" not in users_for_rxn:
            is_primary = True
        else:
            users_for_rxn = users_for_rxn.replace(">>> *", "")[:-1].split("\n")
            is_primary = users_for_rxn.index(user.display_name) < users_for_rxn.index('*__Alternatives__*')
        # is_primary = True if "*__Secondary__*" not in users_for_rxn else users_for_rxn.index(user.display_name) < users_for_rxn.index('*__Secondary__*')
        await add_remove_user_role(msg, reaction.emoji.name, user, is_primary, False)


# --------- Actions ---------

async def add_remove_user_role(message, role, user, primary, adding):
    print("ROLE:", user, role, primary, "adding =",adding)
    if role in CLASSES:
        embed = message.embeds[0]
        index = ROLE_INDEX[role]
        role_value = embed.fields[index].value

        if data.secondary_txt in role_value:
            p_list, s_list = role_value.split(data.secondary_txt + ">>> *")
            s_list = s_list[:-1]
        else:
            p_list, s_list = role_value, "None"
        p_list = [] if p_list == "None" else p_list.split("\n")
        s_list = [] if s_list == "None" else s_list.split("\n")
        if primary:
            if adding:
                p_list.append(user.display_name)
            else:
                p_list.remove(user.display_name)
        else:
            if adding:
                s_list.append(user.display_name)
            else:
                s_list.remove(user.display_name)
        new_list = ("\n".join(p_list) if len(p_list) > 0 else "None") + ((data.secondary_txt + ">>> *" + "\n".join(s_list) + "*") if len(s_list) > 0 else "")

        embed.set_field_at(index,
                           name=f"{discord.utils.get(message.guild.emojis, name=role)} __{role.capitalize()}__ ({len(p_list) + len(s_list)})",
                           value=new_list,
                           inline=True)
        change_header_counts(embed, role, primary, 1 if adding else -1)

        await message.edit(embed=embed)


def change_header_counts(embed, role, primary, change_count=1):
    r = ''
    for k in ROLE_CLASSES.keys():
        r = k if role in ROLE_CLASSES[k] else r
    index = ROLE_INDEX[r]
    role_value = replace_nth_count(embed.fields[index].value, 1 if primary else 2, change_count)
    embed.set_field_at(index, name="\u200b", value=role_value, inline=False)

    if primary:
        total_value = embed.fields[0].value
        total_count = re.findall(r'\d+', total_value)[0]
        total_value = total_value.replace(total_count, str(int(total_count) + change_count))
        embed.set_field_at(0, name="\u200b", value=total_value, inline=False)


def replace_nth_count(value, n, change=1):
    match = re.search(r'`(\d+) \| (\d+)`', value)
    count = int(match.group(n))
    position = [match.start(n), match.end(n)]
    return value[:position[0]] + str(count + change) + value[position[1]:]


client.run(TOKEN)
