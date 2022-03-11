# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/fnixdev/KannaBot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import os
import time
from urllib.request import urlretrieve

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from youtube_dl import YoutubeDL
from youtubesearchpython.__future__ import VideosSearch

from .. import udB
from .all import dler, uploader

# search youtube


async def get_yt_link(query):
    vid_ser = VideosSearch(query, limit=1)
    res = await vid_ser.next()
    results = res["result"]
    for i in results:
        link = i["link"]
    return link


async def download_yt(xx, event, link, ytd):
    st = time.time()
    info = await dler(xx, link)
    try:
        YoutubeDL(ytd).download([link])
    except Exception as ex:
        return await xx.edit(str(ex))
    title = info["title"]
    urlretrieve(f"https://i.ytimg.com/vi/{info['id']}/hqdefault.jpg", f"{title}.jpg")
    thumb = f"{title}.jpg"
    dir = os.listdir()
    if f"{info['id']}.mp3" in dir:
        tm = f"{info['id']}.mp3"
        os.rename(tm, f"{title}.mp3")
        kk = f"{title}.mp3"
        caption = f"`{title}`\n`Do YouTubeMusic`"
    elif f"{info['id']}.mp4" in dir:
        os.rename(f"{info['id']}.mp4", f"{title}.mkv")
        kk = f"{title}.mkv"
        tm = f"{info['id']}"
        caption = f"`{title}`\n\n`Do YouTube Official`"
    else:
        return
    res = await uploader(kk, kk, st, xx, "Enviando...")
    metadata = extractMetadata(createParser(res.name))
    wi = metadata.get("width") if metadata.has("width") else 512
    hi = metadata.get("height") if metadata.has("height") else 512
    duration = metadata.get("duration").seconds if metadata.has("duration") else 0
    try:
        author = info["artist"]
    except KeyError:
        author = info["uploader"]
    if kk.endswith(".mkv"):
        im = Image.open(thumb)
        ok = im.resize((int(wi), int(hi)))
        ok.save(thumb, format="PNG", optimize=True)
        await event.client.send_file(
            event.chat_id,
            file=res,
            caption=caption,
            attributes=[
                DocumentAttributeVideo(
                    duration=duration,
                    w=wi,
                    h=hi,
                    supports_streaming=True,
                )
            ],
            thumb=thumb,
        )
    else:
        await event.client.send_file(
            event.chat_id,
            file=res,
            caption=caption,
            supports_streaming=True,
            thumb=thumb,
            attributes=[
                DocumentAttributeAudio(
                    duration=duration,
                    title=title,
                    performer=author,
                )
            ],
        )
    os.remove(kk)
    os.remove(thumb)
    await xx.delete()
