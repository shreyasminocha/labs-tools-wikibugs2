# encoding: utf-8
from pathlib import Path

import pytest

import configfetcher
import unittest
import requests
import wikibugs

root = Path(__file__).parent.parent


class TestWikibugs(unittest.TestCase):
    def setUp(self):
        self.bugs = wikibugs.Wikibugs2(
            configfetcher.ConfigFetcher(str(root / "config.json.example"))
        )

    def test_offline_scrape(self):
        content = (root / "tests" / "data" / "T87834").open(encoding="utf-8").read()

        tags = self.bugs.get_tags(content)

        assert {
            'Wikimedia-Fundraising',
            'Fundraising Tech Backlog',
            'Wikimedia-Fundraising-CiviCRM',
            '§ Fundraising Sprint Devo',
            'Fr-tech-archived-from-FY-2014/15',
        } == tags.keys()

        assert {'shade', 'disabled', 'uri', 'tagtype'} == tags['§ Fundraising Sprint Devo'].keys()
        assert tags['§ Fundraising Sprint Devo']['shade'] == 'blue'
        assert tags['§ Fundraising Sprint Devo']['disabled']
        assert tags['§ Fundraising Sprint Devo']['uri'] == '/tag/§_fundraising_sprint_devo/'
        assert tags['§ Fundraising Sprint Devo']['tagtype'] == 'calendar'

    @pytest.mark.xfail(reason="'disabled' is no longer processed correctly")
    def test_online_scrape(self):
        content = requests.get('https://phabricator.wikimedia.org/T87834').text

        tags = self.bugs.get_tags(content)

        assert len(tags) > 0

        n_disabled = 0
        n_briefcase = 0
        n_calendar = 0

        for tag, props in tags.items():
            if props['disabled']:
                n_disabled += 1
            if props['tagtype'] == 'briefcase':
                n_briefcase += 1
            if props['tagtype'] == 'calendar':
                n_calendar += 1

        assert n_disabled > 0
        assert n_briefcase > 0
