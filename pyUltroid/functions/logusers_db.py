# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/fnixdev/KannaBot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from .. import udB


def str_to_list(text):  # Returns List
    return text.split(" ")


def list_to_str(list):  # Returns String
    str = "".join(f"{x} " for x in list)
    return str.strip()


def get_logger():  # Returns List
    pmperm = udB.get("LOGUSERS")
    return [""] if pmperm is None or pmperm == "" else str_to_list(pmperm)


def is_logger(id):  # Take int or str with numbers only , Returns Boolean
    if not str(id).isdigit():
        return False
    pmperm = get_logger()
    return str(id) in pmperm


def log_user(id):  # Take int or str with numbers only , Returns Boolean
    id = str(id)
    if not id.isdigit():
        return False
    try:
        pmperm = get_logger()
        pmperm.append(id)
        udB.set("LOGUSERS", list_to_str(pmperm))
        return True
    except Exception as e:
        print(f"KannaBot LOG : // functions/logusers_db/log_user : {e}")
        return False


def nolog_user(id):  # Take int or str with numbers only , Returns Boolean
    id = str(id)
    if not id.isdigit():
        return False
    try:
        pmperm = get_logger()
        pmperm.remove(id)
        udB.set("LOGUSERS", list_to_str(pmperm))
        return True
    except Exception as e:
        print(f"KannaBot LOG : // functions/loguser_db/nolog_user : {e}")
        return False
