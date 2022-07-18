import discord
import json
import logging
from datetime import datetime
import re
import data
from data import CLASSES, ROLE_CLASSES, ROLE_INDEX, STATUSES, STATUS_HEADERS, get_embed_outline
import userfn

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

        sorted_emojis = []
        for emoji in message.guild.emojis:
            if emoji.name in CLASSES:
                sorted_emojis.append(emoji)

        sorted_emojis.sort(key=lambda e: e.name)
        for emoji in sorted_emojis:
            await raid_msg.add_reaction(emoji)

        for status in STATUSES:
            await raid_msg.add_reaction(status)


@client.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    if user != client.user and msg.author == client.user:
        if reaction.emoji in STATUSES:
            await change_status(msg, reaction.emoji, user)
        else:
            # is_primary = not any(user.display_name in field.value.split("\n") for field in msg.embeds[0].fields)
            is_primary = True
            for field in msg.embeds[0].fields:
                flist = field.value.split("\n")
                if userfn.user_index_in_list(user.display_name, flist) != -1:
                    is_primary = False
                    break
            await add_remove_user_role(msg, reaction.emoji.name, user, is_primary, True)


@client.event
async def on_reaction_remove(reaction, user):
    msg = reaction.message
    if user != client.user and msg.author == client.user:
        if reaction.emoji in STATUSES:
            await change_status(msg, reaction.emoji, user)
        elif reaction.emoji.name in CLASSES:
            # users = [u for field in msg.embeds[0].fields for u in field.value.split("\n")]
            users_for_rxn = msg.embeds[0].fields[ROLE_INDEX[reaction.emoji.name]].value
            if "*__Alternatives__*" not in users_for_rxn:
                is_primary = True
            else:
                users_for_rxn = users_for_rxn.replace(">>> *", "")[:-1].split("\n")
                user_index = userfn.user_index_in_list(user.display_name, users_for_rxn)
                is_primary = user_index < users_for_rxn.index('*__Alternatives__*')
            await add_remove_user_role(msg, reaction.emoji.name, user, is_primary, False)


# --------- Actions ---------

async def add_remove_user_role(message, role, user, primary, adding):
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
        statuses = embed.fields[-1].value.split("\n")
        if primary:
            og_len = len(p_list)
            if adding:
                userfn.add_user_to_list(user.display_name, p_list, statuses)
                # p_list.append(user.display_name)
            else:
                userfn.remove_user_from_list(user.display_name, p_list)
                # p_list.remove(user.display_name)
            if og_len == len(p_list):
                return
        else:
            og_len = len(s_list)
            if adding:
                userfn.add_user_to_list(user.display_name, s_list, statuses)
                # s_list.append(user.display_name)
            else:
                userfn.remove_user_from_list(user.display_name, s_list)
                # s_list.remove(user.display_name)
            if og_len == len(s_list):
                return
        new_list = ("\n".join(p_list) if len(p_list) > 0 else "None") + (
            (data.secondary_txt + ">>> *" + "\n".join(s_list) + "*") if len(s_list) > 0 else "")

        embed.set_field_at(index,
                           name=f"{discord.utils.get(message.guild.emojis, name=role)} __{role.capitalize()}__ ({len(p_list)} | {len(s_list)})",
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


# ------ STATUS FUNCTIONS ------

async def change_status(msg, emoji, user):
    embed = msg.embeds[0]
    statusIndex = STATUSES.index(emoji)
    statuses = embed.fields[-1].value.split("\n")
    users = statuses[statusIndex]
    users = users.replace(STATUS_HEADERS[statusIndex], "")
    users = users.split(", ")
    users = list(filter(lambda u: u != '', users))
    # Trim leading space for "LATE" status in first person
    if statusIndex == 2 and len(users) > 0:
        users[0] = users[0][1:]

    # Check if user exists in list users and add/remove
    if user.display_name in users:
        users.remove(user.display_name)
    else:
        users.append(user.display_name)

    new_statuses = get_new_statuses(statusIndex, statuses, users)

    embed.set_field_at(
        len(embed.fields) - 1,
        name="\u200b",
        value=new_statuses,
        inline=False
    )

    await msg.edit(embed=embed)

    await update_existing_user_status(new_statuses.split("\n"), user, msg, statusIndex)


def get_new_statuses(index, statuses, users):
    result = ""
    if index == 0:
        result = STATUS_HEADERS[0] + ", ".join(users) + "\n" + "\n".join(statuses[1:])
    elif index == 1:
        result = statuses[0] + "\n" + STATUS_HEADERS[1] + ", ".join(users) + "\n" + statuses[2]
    elif index == 2:
        result = "\n".join(statuses[:2]) + "\n" + STATUS_HEADERS[2] + " " + ", ".join(users)
    return result


# Takes status_index and updates existing user instances in registration with status emote
async def update_existing_user_status(statuses, user, msg, statusIndex):
    embed = msg.embeds[0]
    for field_i in range(len(embed.fields)):
        field = embed.fields[field_i]
        users = field.value.split("\n")

        first_alt, last_alt = -1, -1
        if "*__Alternatives__*" in users:
            first_alt = users.index("*__Alternatives__*") + 1
            last_alt = len(users) - 1
            users[first_alt] = users[first_alt][5:]
            users[last_alt] = users[last_alt][:-1]

        i = userfn.user_index_in_list(user.display_name, users)
        if i != -1:
            if statusIndex == 0:
                role = list(ROLE_INDEX.keys())[list(ROLE_INDEX.values()).index(field_i)]
                await add_remove_user_role(msg, role, user, first_alt == -1, False)
                continue
            else:
                users = userfn.add_user_to_list(user.display_name, users, statuses, i)
            # users[i] = userfn.add_status_emote(user, statusIndex)

            if first_alt != -1:
                users[first_alt] = ">>> *" + users[first_alt]
            if last_alt != -1:
                users[last_alt] += "*"

            embed.set_field_at(
                field_i,
                name=field.name,
                value="\n".join(users),
                inline=field.inline
            )

            await msg.edit(embed=embed)

client.run(TOKEN)
