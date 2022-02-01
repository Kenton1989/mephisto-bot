import os
import logging
from PIL import Image
from urllib.request import urlopen
from threading import Lock

from nonebot import on_command, CommandSession, logger

import tag_ocr as ocr

# param keys
IMG_CNT = 'img_cnt'
IMG_URL = 'img_url'
IMG = 'img'

cmd_mux = Lock()


@on_command('recruit', aliases=('公招'), only_to_me=False)
async def recruit(session: CommandSession):
    if not cmd_mux.acquire(blocking=False):
        session.finish('👴日理万机，你待会再来', at_sender=True)
    try:
        await recruit_main(session)
    finally:
        cmd_mux.release()


async def recruit_main(session: CommandSession):
    reply = ''

    img: Image.Image = session.aget(IMG, prompt='来张截图', at_sender=True)

    img_cnt = session.state[IMG_CNT]
    if img_cnt > 1:
        reply += '\n我只看第一张图'
    elif img_cnt < 1:
        session.finish('不给图拉倒', at_sender=True)

    try:
        tag_list = ocr.recognize_tags(img)
    except ocr.UnknownTagError as e:
        reply += '\n看不懂的tag：' + str(e)
        session.finish(reply, at_sender=True)
    
    tags = ocr.recognize_tags(img)
    reply += '\ntag：\n- ' + '\n- '.join(tags)

    await session.send(reply, at_sender=True)


@recruit.args_parser
async def extract_img(session: CommandSession):
    images = session.current_arg_images
    img_cnt = len(images)
    session.state[IMG_CNT] = img_cnt

    if img_cnt > 0:
        url = images[0]
        session.state[IMG_URL] = url
        try:
            session.state[IMG] = download_img(url)
        except Exception as e:
            logger.error('image download error: %s', e)
            session.finish('我图读不出来，sb🐧', at_sender=True)


def download_img(url: str) -> Image.Image:
    stream = urlopen(url)
    return Image.open(stream)
