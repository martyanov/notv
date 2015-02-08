"""
    tests.test_feed
    ===============

    Feed functionality related tests.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

import pytest
import responses

from notv.feed import FetchError, ParseError, _make_feed_url, fetch_show_data, \
    parse_show_data


TEST_XML_DOCUMENT_SHOW_ON_AIR = b"""<show id='25'>
    <name>Show name</name>
    <link>http://www.tvrage.com/Show_name</link>
    <ended></ended>
    <latestepisode>
        <number>04x02</number>
        <title>Episode title</title>
        <airdate>2015-02-02</airdate>
    </latestepisode>
    <nextepisode>
        <number>04x03</number>
        <title>Guilty</title>
        <airdate>2015-02-09</airdate>
    </nextepisode>
</show>
"""

TEST_XML_DOCUMENT_SHOW_ENDED = b"""<show id='25'>
    <name>Show name</name>
    <link>http://www.tvrage.com/Show_name</link>
    <ended>2015-02-02</ended>
    <latestepisode>
        <number>04x02</number>
        <title>Episode title</title>
        <airdate>2015-02-02</airdate>
    </latestepisode>
</show>
"""


def test_make_feed_url():
    assert _make_feed_url(25) == ("http://services.tvrage.com/feeds/"
                                  "episodeinfo.php?sid=25")


@responses.activate
def test_fetch_show_data_ok():
    feed_url = _make_feed_url(25)
    responses.add(responses.GET, feed_url,
                  body=b'ok', status=200,
                  match_querystring=True)

    r = fetch_show_data(25)

    assert r == b'ok'


@responses.activate
def test_fetch_show_data_error():
    feed_url = _make_feed_url(25)
    responses.add(responses.GET, feed_url,
                  status=500, match_querystring=True)

    with pytest.raises(FetchError):
        fetch_show_data(25)


def test_parse_show_data_with_invalid_input():
    with pytest.raises(ParseError):
        parse_show_data(None)

    with pytest.raises(ParseError):
        parse_show_data(5)

    with pytest.raises(ParseError):
        parse_show_data("bad data")


def test_parse_show_data_when_show_on_air():
    valid_keys = [
        'name',
        'link',
        'next_episode_number',
        'next_episode_title',
        'next_episode_date',
        'latest_episode_number',
        'latest_episode_title',
        'latest_episode_date',
    ]
    show = parse_show_data(TEST_XML_DOCUMENT_SHOW_ON_AIR)
    assert all([key in show for key in valid_keys])
    assert 'ended' not in show


def test_parse_show_data_when_show_ended():
    wrong_keys = [
        'next_episode_number',
        'next_episode_title',
        'next_episode_date'
    ]
    show = parse_show_data(TEST_XML_DOCUMENT_SHOW_ENDED)
    assert all([key not in show for key in wrong_keys])
    assert 'ended' in show
