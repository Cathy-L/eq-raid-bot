MAX_USERNAME_LEN = 20


# Return index of user in given list, otherwise -1
def user_index_in_list(user, ulist):
    for i in range(len(ulist)):
        # Check user is marked tentative/late
        u = ulist[i]
        if u.endswith("..."):
            u = u[:-3]
        while u.startswith(("❔", "🕒")):
            u = u[2:]

        # Get user index in list
        if u != '' and user.startswith(u):
            return i
    return -1


# Return given list with user replacing index, or appended to end
# Handles when user is marked tentative/late/absent
def add_user_to_list(user, ulist, statuses, index=-1):
    short_user = user
    display = short_user
    for s_i in range(len(statuses)):
        if short_user in statuses[s_i]:
            if s_i == 0:
                return ulist
            else:
                display = add_status_emote(display, s_i)

    if len(display) > MAX_USERNAME_LEN:
        display = display[:MAX_USERNAME_LEN] + "..."

    if index > -1:
        ulist[index] = display
    else:
        ulist.append(display)
    return ulist


def remove_user_from_list(user, ulist):
    for u in ulist:
        short_user = u
        if short_user.endswith("..."):
            short_user = short_user[:-3]
        # Check user is marked tentative/late
        while short_user.startswith(("❔", "🕒")):
            short_user = short_user[2:]
        # Remove user if match
        if user.startswith(short_user):
            ulist.remove(u)
    return ulist


def add_status_emote(user, i):
    if i == 1:
        return "❔ " + user
    if i == 2:
        return "🕒 " + user
