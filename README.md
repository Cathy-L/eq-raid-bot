# Project 1999 Discord Raid Bot

## Fix for the Discord Bot command update is a WIP.

Invite: https://discord.com/api/oauth2/authorize?client_id=983582463643254814&permissions=1100585593920&scope=bot

### NOTE: In order for the bot to work properly, your server MUST include all the exact LOWERCASE emoji names listed in the `emojis` directory (minus the .png extension)

(Using the same .png file is not necessary, only the names must match.)


## Overview

This is a Discord bot whose sole purpose is to generate a raid signup message on command.

![image](https://user-images.githubusercontent.com/16923793/173730670-4c44d9ec-ab8d-4d88-98f5-1e6fa2e2a986.png)

Total *unique* registered players is displayed at the top. Each role has two numbers: the first is how many players have marked the role as their main class, the second is alternative(s).  Numbers next to class names counts both main and alternative players.

Users indicate participation in a raid by reacting to the appropriate class emoji under the raid message.
* The first reaction will be marked as the user's "main" or preferred character class in this raid.
* Subsequent reactions will be marked as alternative character classes that are available from this user.


## How to Use

Generate a new raid signup post with the `!raid` command.
* `--ROLENAME` will ping the given role in the post.
  * **NOTE:** only one-word role names are supported. Any spaces within the role will not work.
* Additional text not beginning with two dashes `--` will be used for the raid post title. (Replacing "Raid Signup" at the top of the screenshot above)

Examples:
* `!raid Vulak Raid` generates a new raid signup post titled "Vulak Raid"
* `!raid --raiders Vulak Raid` generates a new signup like the one above, and also pings the @raiders role.


## Contact

Email me: caffynated @ outlook dot com

Or: send me a PM on Discord @caffy#2808

This is my first Discord bot, made for my bf's raid guild. Please be gentle 🥲
