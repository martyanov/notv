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


class ShowEnded(Exception):
    pass


class NextEpisodeNotFound(Exception):
    pass


def fetch_episode_data(show_id):
    episode_url = BASE_FEED_URL + "episodeinfo.php?sid=" + str(show_id)
    try:
        return requests.get(episode_url, timeout=(5, 5)).content
    except request.exception.RequestException as e:
        logger.exception(e)
        raise FetchError(e)


def parse_episode_data(episode_data):
    episode = {}

    try:
        parsed = ET.fromstring(episode_data)
    except (ValueError, TypeError, ET.ParseError):
        logger.exception(e)
        raise ParseError(e)

    if parsed.find('ended').text:
        raise ShowEnded()

    next_episode = parsed.find('nextepisode')
    if next_episode:
        episode['next_episode_number'] = next_episode.find('number').text
        episode['next_episode_title'] = next_episode.find('title').text
        episode['next_episode_date'] = next_episode.find('airdate').text
    else:
        raise NextEpisodeNotFound()

    latest_episode = parsed.find('latestepisode')
    episode['latest_episode_number'] = latest_episode.find('number').text
    episode['latest_episode_title'] = latest_episode.find('title').text
    episode['latest_episode_date'] = latest_episode.find('airdate').text

    logger.debug("Succesuflly parsed episode data: {}".format(episode))

    return episode
