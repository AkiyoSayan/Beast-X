import os
import re
import urllib
from math import ceil
from re import findall
from urllib.parse import quote

import requests
from pornhub_api import PornhubApi
from search_engine_parser import GoogleSearch
from telethon import Button, custom, events, functions
from youtube_search import YoutubeSearch

from beastx import ALIVE_NAME, CMD_HELP, CMD_LIST, lang
from beastx.function import _deezer_dl, _ytdl
from beastx.modules import inlinestats

PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", None)
if PMPERMIT_PIC is None:
    WARN_PIC = "https://telegra.ph/file/3dd42b44d10528fa1f925.jpg"
else:
    WARN_PIC = PMPERMIT_PIC
LOG_CHAT = Config.PRIVATE_GROUP_ID
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Beast"

if lang == "si":

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query.startswith("Beast-X"):
            rev_text = query[::-1]
            buttons = paginate_help(0, CMD_HELP, "helpme")
            result = builder.article(
                "© Userbot Help",
                text="{}\nCurrently Loaded Plugins: {}".format(query, len(CMD_LIST)),
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result])
        elif event.query.user_id == bot.uid and query == "stats":
            result = builder.article(
                title="Stats",
                text=f"**Showing Stats For {DEFAULTUSER}'s Beast-XBot** \nNote --> Only Owner Can Check This \n(C) [Beast-X](https://github.com/msy1717/Beast-X)",
                buttons=[
                    [custom.Button.inline("Show Stats ?", data="terminator")],
                    [Button.url("Developed By", "https://github.com/msy1717")],
                    [Button.url("Support Chat❤️", "t.me/Botz_Officialsupport")],
                ],
            )
            await event.answer([result])
        elif event.query.user_id == bot.uid and query.startswith("**Hello"):
            result = builder.photo(
                file=WARN_PIC,
                text=query,
                buttons=[
                    [custom.Button.inline("Spamming", data="dontspamnigga")],
                    [
                        custom.Button.inline(
                            "Casual Talk",
                            data="whattalk",
                        )
                    ],
                    [custom.Button.inline("Requesting", data="askme")],
                ],
            )
            await event.answer([result])

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_next\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(current_page_number + 1, CMD_HELP, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_popp_up_alert = "ඔය මොකද කරන්නෙ, මේක ඔයාගෙ නෙමේ!"
            await event.answer(reply_popp_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_prev\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1, CMD_HELP, "helpme"  # pylint:disable=E0602
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "මොන පිස්සෙක්ද තෝ? උඹටම කියල බොටෙක් හදාගනිම්.!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"us_plugin_(.*)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if not event.query.user_id == bot.uid:
            sedok = "මොන පිස්සෙක්ද තෝ? උඹටම කියල බොටෙක් හදාගනිම්."
            await event.answer(sedok, cache_time=0, alert=True)
            return
        plugin_name = event.data_match.group(1).decode("UTF-8")
        if plugin_name in CMD_HELP:
            help_string = (
                f"**🦹‍♀️ PLUGIN NAME 🦹‍♀️ :** `{plugin_name}` \n{CMD_HELP[plugin_name]}"
            )
        reply_pop_up_alert = help_string
        reply_pop_up_alert += "\n\n**(C) Beast-X** ".format(plugin_name)
        if len(reply_pop_up_alert) >= 4096:
            crackexy = "`Pasting Your Help Menu.`"
            await event.answer(crackexy, cache_time=0, alert=True)
            out_file = reply_pop_up_alert
            url = "https://del.dog/documents"
            r = requests.post(url, data=out_file.encode("UTF-8")).json()
            url = f"https://del.dog/{r['key']}"
            await event.edit(
                f"Pasted {plugin_name} to {url}",
                link_preview=False,
                buttons=[[custom.Button.inline("Go Back", data="backme")]],
            )
        else:
            await event.edit(
                message=reply_pop_up_alert,
                buttons=[[custom.Button.inline("Go Back", data="backme")]],
            )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"terminator")))
    async def rip(event):
        if event.query.user_id == bot.uid:
            text = inlinestats
            await event.answer(text, alert=True)
        else:
            txt = "You Can't View My Boss Stats"
            await event.answer(txt, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"yt_dla_(.*)")))
    async def rip(event):
        yt_dl_data = event.data_match.group(1).decode("UTF-8")
        link_s = yt_dl_data
        if event.query.user_id != bot.uid:
            text = f"Sar Get Your Own Beast-X And Don't Waste My Resources"
            await event.answer(text, alert=True)
            return
        is_it = True
        await _ytdl(link_s, is_it, event, tgbot)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deezer_dl_(.*)")))
    async def rip(event):
        sun = event.data_match.group(1).decode("UTF-8")

        if event.query.user_id != bot.uid:
            text = f"Please Get Your Own Beast-X And Don't Waste My Resources"
            await event.answer(text, alert=True)
            return
        await _deezer_dl(sun, event, tgbot)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"yt_vid_(.*)")))
    async def rip(event):
        yt_dl_data = event.data_match.group(1).decode("UTF-8")
        link_s = yt_dl_data
        if event.query.user_id != bot.uid:
            text = f"Please Get Your Own Beast-X And Don't Waste My Resources"
            await event.answer(text, alert=True)
            return
        is_it = False
        await _ytdl(link_s, is_it, event, tgbot)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ph_dl_(.*)")))
    async def rip(event):
        link_s = event.pattern_match.group(1)
        if event.query.user_id != bot.uid:
            text = f"Please Get Your Own Beast-X And Don't Waste My Resources."
            await event.answer(text, alert=True)
            return
        await _phdl(link_s, event, tgbot)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"dontspamnigga")))
    async def rip(event):
        if event.query.user_id == bot.uid:
            sedok = "Boss, You Don't Need To Use This."
            await event.answer(sedok, cache_time=0, alert=True)
            return
        await event.get_chat()
        him_id = event.query.user_id
        text1 = "ඔයා ඇවිත් තියෙන්නෙ හොඳ දේකට නෙමේ.. ඔයා තෝරපු එක පිළිගන්න බෑ.. ඒක නිසා ඔයාව Block කරනවා"
        await event.edit("ඔයා තෝරපු එක පිළිගන්න බෑ ❌")
        await borg.send_message(event.query.user_id, text1)
        await borg(functions.contacts.BlockRequest(event.query.user_id))
        await borg.send_message(
            LOG_CHAT,
            f"ආයුබෝවන්, මෝඩ  [පකයා](tg://user?id={him_id}) තහන්ම් එකක් තෝරපු නිසා Block කරා",
        )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"backme")))
    async def sed(event):
        if event.query.user_id != bot.uid:
            sedok = "මොන පිස්සෙක්ද තෝ? උඹටම කියල බොටෙක් හදාගනිම්."
            await event.answer(sedok, cache_time=0, alert=True)
            return
        await event.answer("Back", cache_time=0, alert=False)
        # This Is Copy of Above Code. (C) @SpEcHiDe
        buttons = paginate_help(0, CMD_HELP, "helpme")
        sed = f"""Fire-X Modules Are Listed Here !\n
    For More Help or Support contact {DEFAULTUSER} \nCurrently Loaded Plugins: {len(CMD_LIST)}\nCurrently using Language - Sinhala (Sinhalese)"""
        await event.edit(message=sed, buttons=buttons)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"whattalk")))
    async def rip(event):
        if event.query.user_id == bot.uid:
            sedok = "Boss, You Don't Need To Use This."
            await event.answer(sedok, cache_time=0, alert=True)
            return
        await event.get_chat()
        him_id = event.query.user_id
        await event.edit("ඔයා තෝරපු එක මම පිළිගන්නවා ✔️")
        text2 = "හරි දැන් මගේ අයිතිකාරයා ඔයාට මැසේජ් එකක් දානකන් ටිකක් ඉවසල ඉන්න. \nගොඩාක් ස්තූතී මැසේජ් කරාට."
        await borg.send_message(event.query.user_id, text2)
        await borg.send_message(
            LOG_CHAT,
            message=f"Hello, [අලුත් පොරක්](tg://user?id={him_id}). ඔයා එක්ක කතා කරන්න ඉල්ලනවා.",
        )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"askme")))
    async def rip(event):
        if event.query.user_id == bot.uid:
            sedok = "මහත්තයෝ, ඔයා මේක පාවිච්චි කරන්න ඕන නෑ"
            await event.answer(sedok, cache_time=0, alert=True)
            return
        await event.get_chat()
        him_id = event.query.user_id
        await event.edit("ඔයා තෝරපු එක මම පිළිගන්නවා ✔️")
        text3 = "හරි දැන් මගේ අයිතිකාරයා ඔයාට මැසේජ් එකක් දානකන් ටිකක් ඉවසල ඉන්න. \nගොඩාක් ස්තූතී මැසේජ් කරාට."
        await borg.send_message(event.query.user_id, text3)
        await borg.send_message(
            LOG_CHAT,
            message=f"Hello, [අලුත් පොරකට](tg://user?id={him_id}). ඔයාගෙන් දෙයක් ඉල්ලන්න තියේලු.",
        )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            await event.edit("menu closed")
        else:
            reply_pop_up_alert = "මොන පිස්සෙක්ද තෝ? උඹටම කියල බොටෙක් හදාගනිම්. "
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    def paginate_help(page_number, loaded_modules, prefix):
        number_of_rows = 8
        number_of_cols = 2
        helpable_modules = []
        for p in loaded_modules:
            if not p.startswith("_"):
                helpable_modules.append(p)
        helpable_modules = sorted(helpable_modules)
        modules = [
            custom.Button.inline(
                "{} {} {}".format(
                    Config.EMOJI_TO_DISPLAY_IN_HELP, x, Config.EMOJI_TO_DISPLAY_IN_HELP
                ),
                data="us_plugin_{}".format(x),
            )
            for x in helpable_modules
        ]
        pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
        if len(modules) % number_of_cols == 1:
            pairs.append((modules[-1],))
        max_num_pages = ceil(len(pairs) / number_of_rows)
        modulo_page = page_number % max_num_pages
        if len(pairs) > number_of_rows:
            pairs = pairs[
                modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
            ] + [
                (
                    custom.Button.inline(
                        "⏪ Previous", data="{}_prev({})".format(prefix, modulo_page)
                    ),
                    custom.Button.inline("Close", data="close"),
                    custom.Button.inline(
                        "Next ⏩", data="{}_next({})".format(prefix, modulo_page)
                    ),
                )
            ]
        return pairs


else:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query.startswith("Beast-X"):
            rev_text = query[::-1]
            buttons = paginate_help(0, CMD_HELP, "helpme")
            result = builder.article(
                "© Userbot Help",
                text="{}\nCurrently Loaded Plugins: {}".format(query, len(CMD_LIST)),
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result])
        elif event.query.user_id == bot.uid and query == "stats":
            result = builder.article(
                title="Stats",
                text=f"**Showing Stats For {DEFAULTUSER}'s Fire-X** \nNote --> Only Owner Can Check This \n(C) Beast-X",
                buttons=[
                    [custom.Button.inline("Show Stats ?", data="terminator")],
                    [
                        Button.url(
                            "Repo Here", "https://github.com/msy1717/Beast-X"
                        )
                    ],
                    [Button.url("Join Channel ❤️", "t.me/https://t.me/Botz_Official")],
                ],
            )
            await event.answer([result])
        elif event.query.user_id == bot.uid and query.startswith("**Hello"):
            result = builder.photo(
                file=WARN_PIC,
                text=query,
                buttons=[
                    [custom.Button.inline("Spamming", data="dontspamnigga")],
                    [
                        custom.Button.inline(
                            "Casual Talk",
                            data="whattalk",
                        )
                    ],
                    [custom.Button.inline("Requesting", data="askme")],
                ],
            )
            await event.answer([result])

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_next\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(current_page_number + 1, CMD_HELP, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_popp_up_alert = "Please get your own Userbot, and don't use mine!"
            await event.answer(reply_popp_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_prev\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1, CMD_HELP, "helpme"  # pylint:disable=E0602
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own Userbot, and don't use mine!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"us_plugin_(.*)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if not event.query.user_id == bot.uid:
            sedok = "Who The Fuck Are You? Get Your Own Beast-X ."
            await event.answer(sedok, cache_time=0, alert=True)
            return
        plugin_name = event.data_match.group(1).decode("UTF-8")
        if plugin_name in CMD_HELP:
            help_string = (
                f"**🦹‍♀️ PLUGIN NAME 🦹‍♀️ :** `{plugin_name}` \n{CMD_HELP[plugin_name]}"
            )
        reply_pop_up_alert = help_string
        reply_pop_up_alert += "\n\n**(C) @BeastX_Userbot** ".format(plugin_name)
        if len(reply_pop_up_alert) >= 4096:
            crackexy = "`Pasting Your Help Menu.`"
            await event.answer(crackexy, cache_time=0, alert=True)
            out_file = reply_pop_up_alert
            url = "https://del.dog/documents"
            r = requests.post(url, data=out_file.encode("UTF-8")).json()
            url = f"https://del.dog/{r['key']}"
            await event.edit(
                f"Pasted {plugin_name} to {url}",
                link_preview=False,
                buttons=[[custom.Button.inline("Go Back", data="backme")]],
            )
        else:
            await event.edit(
                message=reply_pop_up_alert,
                buttons=[[custom.Button.inline("Go Back", data="backme")]],
            )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"terminator")))
    async def rip(event):
        if event.query.user_id == bot.uid:
            text = inlinestats
            await event.answer(text, alert=True)
        else:
            txt = "You Can't View My Masters Stats"
            await event.answer(txt, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"yt_dla_(.*)")))
    async def rip(event):
        yt_dl_data = event.data_match.group(1).decode("UTF-8")
        link_s = yt_dl_data
        if event.query.user_id != bot.uid:
            text = f"Please Get Your Own Beast-X And Don't Waste My Resources"
            await event.answer(text, alert=True)
            return
        is_it = True
        await _ytdl(link_s, is_it, event, tgbot)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deezer_dl_(.*)")))
    async def rip(event):
        sun = event.data_match.group(1).decode("UTF-8")

        if event.query.user_id != bot.uid:
            text = f"Please Get Your Own Beast-X And Don't Waste My Resources"
            await event.answer(text, alert=True)
            return
        await _deezer_dl(sun, event, tgbot)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"yt_vid_(.*)")))
    async def rip(event):
        yt_dl_data = event.data_match.group(1).decode("UTF-8")
        link_s = yt_dl_data
        if event.query.user_id != bot.uid:
            text = f"Please Get Your Own Beast-X And Don't Waste My Resources"
            await event.answer(text, alert=True)
            return
        is_it = False
        await _ytdl(link_s, is_it, event, tgbot)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ph_dl_(.*)")))
    async def rip(event):
        link_s = event.pattern_match.group(1)
        if event.query.user_id != bot.uid:
            text = f"Please Get Your Own Beast-X And Don't Waste My Resources."
            await event.answer(text, alert=True)
            return
        await _phdl(link_s, event, tgbot)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"dontspamnigga")))
    async def rip(event):
        if event.query.user_id == bot.uid:
            sedok = "Master, You Don't Need To Use This."
            await event.answer(sedok, cache_time=0, alert=True)
            return
        await event.get_chat()
        him_id = event.query.user_id
        text1 = "You Have Chosed A Probhited Option. Therefore, You Have Been Blocked"
        await event.edit("Choice Not Accepted ❌")
        await borg.send_message(event.query.user_id, text1)
        await borg(functions.contacts.BlockRequest(event.query.user_id))
        await borg.send_message(
            LOG_CHAT,
            f"Hello, A Noob [Nibba](tg://user?id={him_id}) Selected Probhited Option, Therefore Blocked.",
        )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"backme")))
    async def sed(event):
        if event.query.user_id != bot.uid:
            sedok = "Who The Fuck Are You? Get Your Own bot."
            await event.answer(sedok, cache_time=0, alert=True)
            return
        await event.answer("Back", cache_time=0, alert=False)
        # This Is Copy of Above Code. (C) @SpEcHiDe
        buttons = paginate_help(0, CMD_HELP, "helpme")
        sed = f"""Beast-X Userbot Modules Are Listed Here !\n
    For More Help or Support contact {DEFAULTUSER} \nCurrently Loaded Plugins: {len(CMD_LIST)}\nCurrently using Language - English (Standard)"""
        await event.edit(message=sed, buttons=buttons)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"whattalk")))
    async def rip(event):
        if event.query.user_id == bot.uid:
            sedok = "Master, You Don't Need To Use This."
            await event.answer(sedok, cache_time=0, alert=True)
            return
        await event.get_chat()
        him_id = event.query.user_id
        await event.edit("Your Choice Accepted ✔️")
        text2 = "Ok. Please Wait Until My Master will Approve you soon. Don't Spam Here Or Try Anything Stupid. \nThank You For Contacting Me."
        await borg.send_message(event.query.user_id, text2)
        await borg.send_message(
            LOG_CHAT,
            message=f"Hello, A [New User](tg://user?id={him_id}). Wants To Talk With You.",
        )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"askme")))
    async def rip(event):
        if event.query.user_id == bot.uid:
            sedok = "Master, You Don't Need To Use This."
            await event.answer(sedok, cache_time=0, alert=True)
            return
        await event.get_chat()
        him_id = event.query.user_id
        await event.edit("Your choice is Accepted ✔️")
        text3 = "Ok, Wait. My Master will reply you soon. Kindly, Wait."
        await borg.send_message(event.query.user_id, text3)
        await borg.send_message(
            LOG_CHAT,
            message=f"Hello, A [New User](tg://user?id={him_id}). Wants To Ask You Something.",
        )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            await event.edit("menu closed")
        else:
            reply_pop_up_alert = "WTF are you Doing.. "
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    def paginate_help(page_number, loaded_modules, prefix):
        number_of_rows = 8
        number_of_cols = 2
        helpable_modules = []
        for p in loaded_modules:
            if not p.startswith("_"):
                helpable_modules.append(p)
        helpable_modules = sorted(helpable_modules)
        modules = [
            custom.Button.inline(
                "{} {} {}".format(
                    Config.EMOJI_TO_DISPLAY_IN_HELP, x, Config.EMOJI_TO_DISPLAY_IN_HELP
                ),
                data="us_plugin_{}".format(x),
            )
            for x in helpable_modules
        ]
        pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
        if len(modules) % number_of_cols == 1:
            pairs.append((modules[-1],))
        max_num_pages = ceil(len(pairs) / number_of_rows)
        modulo_page = page_number % max_num_pages
        if len(pairs) > number_of_rows:
            pairs = pairs[
                modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
            ] + [
                (
                    custom.Button.inline(
                        "⏪ Previous", data="{}_prev({})".format(prefix, modulo_page)
                    ),
                    custom.Button.inline("Close", data="close"),
                    custom.Button.inline(
                        "Next ⏩", data="{}_next({})".format(prefix, modulo_page)
                    ),
                )
            ]
        return pairs


@tgbot.on(events.InlineQuery(pattern=r"torrent (.*)"))
async def inline_id_handler(event: events.InlineQuery.Event):
    builder = event.builder
    if event.query.user_id != bot.uid:
        resultm = builder.article(
            title="Not Allowded",
            text=f"You Can't Use This Bot. \nDeploy Beast-X To Get Your Own Assistant, Repo Link [Here](https://github.com/msy1717/Beast-X)",
        )
        await event.answer([resultm])
        return
    testinput = event.pattern_match.group(1)
    starkisnub = urllib.parse.quote_plus(testinput)
    results = []
    sedlyf = "https://api.sumanjay.cf/torrent/?query=" + starkisnub
    try:
        okpro = requests.get(url=sedlyf, timeout=10).json()
    except:
        pass
    sed = len(okpro)
    if sed == 0:
        resultm = builder.article(
            title="No Results Found.",
            description="Check Your Spelling / Keyword",
            text="**Please, Search Again With Correct Keyword, Thank you !**",
            buttons=[
                [
                    Button.switch_inline(
                        "Search Again", query="torrent ", same_peer=True
                    )
                ],
            ],
        )
        await event.answer([resultm])
        return
    if sed > 30:
        for i in range(30):
            seds = okpro[i]["age"]
            okpros = okpro[i]["leecher"]
            sadstark = okpro[i]["magnet"]
            okiknow = okpro[i]["name"]
            starksize = okpro[i]["size"]
            starky = okpro[i]["type"]
            seeders = okpro[i]["seeder"]
            okayz = f"**Title :** `{okiknow}` \n**Size :** `{starksize}` \n**Type :** `{starky}` \n**Seeder :** `{seeders}` \n**Leecher :** `{okpros}` \n**Magnet :** `{sadstark}` "
            sedme = f"Size : {starksize} Type : {starky} Age : {seds}"
            results.append(
                await event.builder.article(
                    title=okiknow,
                    description=sedme,
                    text=okayz,
                    buttons=Button.switch_inline(
                        "Search Again", query="torrent ", same_peer=True
                    ),
                )
            )
    else:
        for sedz in okpro:
            seds = sedz["age"]
            okpros = sedz["leecher"]
            sadstark = sedz["magnet"]
            okiknow = sedz["name"]
            starksize = sedz["size"]
            starky = sedz["type"]
            seeders = sedz["seeder"]
            okayz = f"**Title :** `{okiknow}` \n**Size :** `{starksize}` \n**Type :** `{starky}` \n**Seeder :** `{seeders}` \n**Leecher :** `{okpros}` \n**Magnet :** `{sadstark}` "
            sedme = f"Size : {starksize} Type : {starky} Age : {seds}"
            results.append(
                await event.builder.article(
                    title=okiknow,
                    description=sedme,
                    text=okayz,
                    buttons=[
                        Button.switch_inline(
                            "Search Again", query="torrent ", same_peer=True
                        )
                    ],
                )
            )
    await event.answer(results)


@tgbot.on(events.InlineQuery(pattern=r"yt (.*)"))
async def inline_id_handler(event: events.InlineQuery.Event):
    builder = event.builder
    if event.query.user_id != bot.uid:
        resultm = builder.article(
            title="Not Allowded",
            text=f"You Can't Use This Bot. \nDeploy Beast-X To Get Your Own Assistant, Repo Link [Here](https://github.com/msy1717/Beast-X)",
        )
        await event.answer([resultm])
        return
    testinput = event.pattern_match.group(1)
    urllib.parse.quote_plus(testinput)
    results = []
    moi = YoutubeSearch(testinput, max_results=9).to_dict()
    if not moi:
        resultm = builder.article(
            title="No Results Found.",
            description="Check Your Spelling / Keyword",
            text="**Please, Search Again With Correct Keyword, Thank you !**",
            buttons=[
                [Button.switch_inline("Search Again", query="yt ", same_peer=True)],
            ],
        )
        await event.answer([resultm])
        return
    for moon in moi:
        hmm = moon["id"]
        mo = f"https://www.youtube.com/watch?v={hmm}"
        kek = f"https://www.youtube.com/watch?v={hmm}"
        stark_name = moon["title"]
        stark_chnnl = moon["channel"]
        total_stark = moon["duration"]
        stark_views = moon["views"]
        moon["long_desc"]
        kekme = f"https://img.youtube.com/vi/{hmm}/hqdefault.jpg"
        okayz = f"**Title :** `{stark_name}` \n**Link :** `{kek}` \n**Channel :** `{stark_chnnl}` \n**Views :** `{stark_views}` \n**Duration :** `{total_stark}`"
        hmmkek = f"Video Name : {stark_name} \nChannel : {stark_chnnl} \nDuration : {total_stark} \nViews : {stark_views}"
        results.append(
            await event.builder.document(
                file=kekme,
                title=stark_name,
                description=hmmkek,
                text=okayz,
                include_media=True,
                buttons=[
                    [custom.Button.inline("Download Video - mp4", data=f"yt_vid_{mo}")],
                    [custom.Button.inline("Download Audio - mp3", data=f"yt_dla_{mo}")],
                    [Button.switch_inline("Search Again", query="yt ", same_peer=True)],
                ],
            )
        )
    await event.answer(results)


@tgbot.on(events.InlineQuery(pattern=r"jm (.*)"))
async def inline_id_handler(event: events.InlineQuery.Event):
    builder = event.builder
    if event.query.user_id != bot.uid:
        resultm = builder.article(
            title="Not Allowded",
            text=f"You Can't Use This Bot. \nDeploy Beast-X To Get Your Own Assistant, Repo Link [Here](https://github.com/msy1717/Beast-X)",
        )
        await event.answer([resultm])
        return
    testinput = event.pattern_match.group(1)
    starkisnub = urllib.parse.quote_plus(testinput)
    results = []
    search = f"http://starkmusic.herokuapp.com/result/?query={starkisnub}"
    seds = requests.get(url=search).json()
    for okz in seds:
        okz["album"]
        okmusic = okz["music"]
        hmmstar = okz["perma_url"]
        singer = okz["singers"]
        hmm = okz["duration"]
        langs = okz["language"]
        hidden_url = okz["media_url"]
        okayz = (
            f"**Song Name :** `{okmusic}` \n**Singer :** `{singer}` \n**Song Url :** `{hmmstar}`"
            f"\n**Language :** `{langs}` \n**Download Able Url :** `{hidden_url}`"
            f"\n**Duration :** `{hmm}`"
        )
        hmmkek = (
            f"Song : {okmusic} Singer : {singer} Duration : {hmm} \nLanguage : {langs}"
        )
        results.append(
            await event.builder.article(
                title=okmusic,
                description=hmmkek,
                text=okayz,
                buttons=Button.switch_inline(
                    "Search Again", query="jm ", same_peer=True
                ),
            )
        )
    await event.answer(results)


@tgbot.on(events.InlineQuery(pattern=r"google (.*)"))
async def inline_id_handler(event: events.InlineQuery.Event):
    builder = event.builder
    if event.query.user_id != bot.uid:
        resultm = builder.article(
            title="- Not Allowded -",
            text=f"You Can't Use This Bot. \nDeploy Beast-X  To Get Your Own Assistant, Repo Link [Here](https://github.com/msy1717/Beast-X)",
        )
        await event.answer([resultm])
        return
    results = []
    match = event.pattern_match.group(1)
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1

    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            okiknow = f"**GOOGLE - SEARCH** \n[{title}]({link})\n\n`{desc}`"
            results.append(
                await event.builder.article(
                    title=title,
                    description=desc,
                    text=okiknow,
                    buttons=[
                        Button.switch_inline(
                            "Search Again", query="google ", same_peer=True
                        )
                    ],
                )
            )
        except IndexError:
            break
    await event.answer(results)


@tgbot.on(events.InlineQuery(pattern=r"ph (.*)"))
async def inline_id_handler(event: events.InlineQuery.Event):
    builder = event.builder
    if event.query.user_id != bot.uid:
        resultm = builder.article(
            title="- Not Allowded -",
            text=f"You Can't Use This Bot. \nDeploy Beast-X To Get Your Own Assistant, Repo Link [Here](https://github.com/msy1717/Beast-X)",
        )
        await event.answer([resultm])
        return
    results = []
    input_str = event.pattern_match.group(1)
    api = PornhubApi()
    data = api.search.search(input_str, ordering="mostviewed")
    ok = 1
    for vid in data.videos:
        if ok <= 5:
            lul_m = f"**PORN-HUB SEARCH** \n**Video title :** `{vid.title}` \n**Video link :** `https://www.pornhub.com/view_video.php?viewkey={vid.video_id}`"
            results.append(
                await event.builder.article(
                    title=vid.title,
                    text=lul_m,
                    buttons=[
                        Button.switch_inline(
                            "Search Again", query="ph ", same_peer=True
                        )
                    ],
                )
            )
        else:
            pass
    await event.answer(results)


@tgbot.on(events.InlineQuery(pattern=r"xkcd (.*)"))
async def inline_id_handler(event: events.InlineQuery.Event):
    builder = event.builder
    if event.query.user_id != bot.uid:
        resultm = builder.article(
            title="- Not Allowded -",
            text=f"You Can't Use This Bot. \nDeploy Beast-X To Get Your Own Assistant, Repo Link [Here](https://github.com/msy1717/Beast-X)",
        )
        await event.answer([resultm])
        return
    input_str = event.pattern_match.group(1)
    xkcd_id = None
    if input_str:
        if input_str.isdigit():
            xkcd_id = input_str
        else:
            xkcd_search_url = "https://relevantxkcd.appspot.com/process?"
            queryresult = requests.get(
                xkcd_search_url, params={"action": "xkcd", "query": quote(input_str)}
            ).text
            xkcd_id = queryresult.split(" ")[2].lstrip("\n")
    if xkcd_id is None:
        xkcd_url = "https://xkcd.com/info.0.json"
    else:
        xkcd_url = "https://xkcd.com/{}/info.0.json".format(xkcd_id)
    r = requests.get(xkcd_url)
    if r.ok:
        data = r.json()
        year = data.get("year")
        month = data["month"].zfill(2)
        day = data["day"].zfill(2)
        xkcd_link = "https://xkcd.com/{}".format(data.get("num"))
        safe_title = data.get("safe_title")
        data.get("transcript")
        alt = data.get("alt")
        img = data.get("img")
        data.get("title")
        output_str = """
[XKCD]({})
Title: {}
Alt: {}
Day: {}
Month: {}
Year: {}""".format(
            xkcd_link, safe_title, alt, day, month, year
        )
        lul_k = builder.photo(file=img, text=output_str)
        await event.answer([lul_k])
    else:
        resultm = builder.article(title="- No Results :/ -", text=f"No Results Found !")
        await event.answer([resultm])


@tgbot.on(events.InlineQuery(pattern=r"deezer ?(.*)"))
async def inline_id_handler(event):
    builder = event.builder
    if event.query.user_id != bot.uid:
        resultm = builder.article(
            title="- Not Allowded -",
            text=f"You Can't Use This Bot. \nDeploy Beast-X To Get Your Own Assistant, Repo Link [Here](https://github.com/msy1717/Beast-X)",
        )
        await event.answer([resultm])
        return
    results = []
    input_str = event.pattern_match.group(1)
    link = f"https://api.deezer.com/search?q={input_str}&limit=7"
    dato = requests.get(url=link).json()
    # data_s = json.loads(data_s)
    for match in dato.get("data"):
        match.get("link")
        hmm_m = f"Title : {match['title']} \nLink : {match['link']} \nDuration : {match['duration']} seconds \nBy : {match['artist']['name']}"
        results.append(
            await event.builder.document(
                file=match["album"]["cover_medium"],
                title=match["title"],
                text=hmm_m,
                description=f"Artist: {match['artist']['name']}\nAlbum: {match['album']['title']}",
                buttons=[
                    [
                        custom.Button.inline(
                            "Download Audio - mp3", data=f"deezer_dl_{match['title']}"
                        )
                    ],
                    [
                        Button.switch_inline(
                            "Search Again", query="deezer ", same_peer=True
                        )
                    ],
                ],
            ),
        )
    if results:
        try:
            await event.answer(results)
        except TypeError:
            pass
