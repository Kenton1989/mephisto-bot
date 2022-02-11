from typing import *
import re

import pytesseract as ocr
from PIL import Image, ImageStat

import recruit_tag.recruit_data as db


def recognize_tags(img: Image.Image) -> List[str]:
    w, h = img.size
    if h > w:
        raise InvalidImgError(f'invalid image width/height ratio: {w/h}')

    if h < 500 or w < 500:
        raise InvalidImgError(f'resolution too low: {w}x{h}')

    tag_img_list = crop_tags(img)
    tag_img_batch = v_concat_tag_imgs(tag_img_list)

    stat = ImageStat.Stat(tag_img_batch)
    if stat.mean[0] < 210:
        raise InvalidImgError(
            f'average brightness of tag image batch is too low {stat.mean[0]}')

    tag_txt_list = recognize_tag_batch(tag_img_batch)

    return tag_txt_list

# concatenate tag images vertically


def v_concat_tag_imgs(tag_img_list: List[Image.Image]) -> Image.Image:
    w = min(img.size[0] for img in tag_img_list)
    h = sum(img.size[1] for img in tag_img_list)

    dst = Image.new('L', (w, h))
    y = 0
    for img in tag_img_list:
        dst.paste(img, (0, y))
        y += img.size[1]

    return dst


def crop_tags(img: Image.Image) -> List[Image.Image]:
    w, h = img.size
    vw, vh = w/100, h/100
    pos_list = get_tag_pos(vw, vh)

    return [crop_one_tag(img, pos) for pos in pos_list]


def crop_one_tag(img: Image.Image, tag_pos: Tuple[float]) -> List[Image.Image]:
    tag_img = img.crop(tag_pos)
    res = binarise_tag_img(tag_img)

    return res


def get_tag_pos(vw: float, vh: float) -> List[Tuple[float]]:
    '''
    vw: 1% of the width of view
    vh: 1% of the height of view
    '''
    return [
        (50*vw-36.481*vh, 50.185*vh, 50*vw-17.315*vh, 56.111*vh),
        (50*vw-13.241*vh, 50.185*vh, 50*vw+6.111*vh, 56.111*vh),
        (50*vw+10.000*vh, 50.185*vh, 50*vw+29.259*vh, 56.111*vh),
        (50*vw-36.481*vh, 60.278*vh, 50*vw-17.315*vh, 66.019*vh),
        (50*vw-13.241*vh, 60.278*vh, 50*vw+6.111*vh, 66.019*vh),
    ]


def binarise_tag_img(img: Image.Image) -> Image.Image:
    # assuming dark background and white text
    # convert to white background and black text
    res = img.convert('L').point(lambda m: 255 if m < 128 else 0, mode='1')
    stat = ImageStat.Stat(res)

    # if the lightness to low, means black ground is used, convert to white background
    if stat.mean[0] < 128:
        # ImageOps does not support inverting "L" format image
        # invert on my own
        res = res.point(lambda m: 255 - m, mode='1')

    return res


def recognize_one_tag(img: Image.Image) -> str:
    res = ocr.image_to_string(img, lang='chi_sim', config='--psm 11')
    res = res.replace(' ', '').strip()
    if res not in TAGS:
        raise UnknownTagError(res)
    return res


NOT_NEWLINE_AND_CHINESE = re.compile(r'[^\n\u4E00-\u9FFF]+')
REPEAT_NEWLINE = re.compile('\n+')


def recognize_tag_batch(img: Image.Image) -> List[str]:
    res = ocr.image_to_string(img, lang='chi_sim', config='--psm 11')

    # remove non-useful char
    res = re.sub(NOT_NEWLINE_AND_CHINESE, '', res).strip()
    # split with newline
    res_list = re.split(REPEAT_NEWLINE, res)
    # unique elements
    res_list = list(set(res_list))

    if len(res_list) != 5:
        raise InvalidImgError(f'cannot recognize all 5 tags, got {res_list}')

    for word in res_list:
        if word not in db.TAGS:
            raise UnknownTagError(word)
    return res_list


class UnknownTagError(Exception):
    pass


class InvalidImgError(Exception):
    pass
