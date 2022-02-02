import os
import logging
import asyncio
from PIL import Image
from urllib.request import urlopen
from threading import Lock

from nonebot import on_command, CommandSession

import recruit_tag.tag_ocr as ocr
import recruit_tag.analysis as analysis

# param keys
IMG_CNT = 'img_cnt'
IMG_URL = 'img_url'

cmd_mux = Lock()
log = logging.getLogger('recruit_tag')

@on_command('recruit', aliases=('公招'), only_to_me=False)
async def recruit(session: CommandSession):
    if not cmd_mux.acquire(blocking=False):
        session.finish('\n👴日理万机，你待会再来', at_sender=True)
    try:
        await recruit_main(session)
    finally:
        cmd_mux.release()


async def recruit_main(session: CommandSession):
    reply = ''

    img_url_future = session.aget(IMG_URL, prompt='\n来张截图', at_sender=True)
    try:
        img_url: str = (await asyncio.wait_for(img_url_future, 30))
    except asyncio.TimeoutError:
        session.finish('\n不给图拉倒，我不等了', at_sender=True)

    img_cnt = session.state[IMG_CNT]
    if img_cnt < 1:
        session.finish('\n不给图拉倒', at_sender=True)

    try:
        img = download_img(img_url)
    except Exception as e:
        log.error('image download error: %s', e)
        session.finish('\n我图读不出来，sb🐧', at_sender=True)
    
    if img_cnt > 1:
        session.send('\n我只管第一张图', at_sender=True)
    else:
        session.send('\n稍等一下', at_sender=True)

    w, h = img.size
    if h < 400 or w < 400:
        session.finish('\n画质好渣', at_sender=True)


    try:
        tag_list = ocr.recognize_tags(img)
    except ocr.UnknownTagError as e:
        log.warn('unknown tag: %s', e)
        if h < 720 or w < 720:
            session.finish('\n画质好渣', at_sender=True)
        session.finish('\n看不懂的tag：\n' + str(e), at_sender=True)
    except ocr.InvalidImgError as e:
        log.warn('invalid image: %s', e)
        if h < 720 or w < 720:
            session.finish('\n画质好渣', at_sender=True)
        session.finish('\n你发的是个什么玩意？', at_sender=True)

    tags = ocr.recognize_tags(img)

    try:
        res = analysis.rank6_analysis(tags)
    except analysis.NoRank6Error:
        session.finish('\n没高资也好意思叫我？', at_sender=True)

    res_str = ''.join('\n\n' + str(r) for r in res)

    await session.send(res_str, at_sender=True)


@recruit.args_parser
async def extract_img(session: CommandSession):
    images = session.current_arg_images
    img_cnt = len(images)
    session.state[IMG_CNT] = img_cnt

    if img_cnt > 0:
        url = images[0]
        session.state[IMG_URL] = url


def download_img(url: str) -> Image.Image:
    stream = urlopen(url)
    return Image.open(stream)
