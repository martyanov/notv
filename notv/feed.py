"""
    notv.feed
    =========

    Feed machinery based on TVRage API.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

import logging
import xml.etree.ElementTree as ET

import requests


logger = logging.getLogger(__name__)

BASE_FEED_URL = "http://services.tvrage.com/feeds/"


class FetchError(Exception):
    pass


class ParseError(Exception):
    pass


def _make_feed_url(show_id):
    return BASE_FEED_URL + "episodeinfo.php?sid=" + str(show_id)


def fetch_show_data(show_id):
    feed_url = _make_feed_url(show_id)
    try:
        return requests.get(feed_url, timeout=(30, 30)).content
    except requests.exceptions.RequestException as e:
        logger.exception(e)
        raise FetchError(e)


def parse_show_data(show_data):
    show = {}

    try:
        parsed = ET.fromstring(show_data)
    except (ValueError, TypeError, ET.ParseError) as e:
        logger.exception(e)
        raise ParseError(e)

    show['name'] = parsed.find('name').text
    show['link'] = parsed.find('link').text

    ended = parsed.find('ended').text
    if ended:
        show['ended'] = ended

    next_episode = parsed.find('nextepisode')
    if next_episode:
        show['next_episode_number'] = next_episode.find('number').text
        show['next_episode_title'] = next_episode.find('title').text
        show['next_episode_date'] = next_episode.find('airdate').text

    latest_episode = parsed.find('latestepisode')
    if latest_episode:
        show['latest_episode_number'] = latest_episode.find('number').text
        show['latest_episode_title'] = latest_episode.find('title').text
        show['latest_episode_date'] = latest_episode.find('airdate').text

    logger.debug("Successfully parsed episode data: {}".format(show))

    return show
