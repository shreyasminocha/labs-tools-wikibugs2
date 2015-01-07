#!/usr/bin/env python

import channelfilter

chanfilter = channelfilter.ChannelFilter()
# An exception would have been raised if that wasn't the case
print('channels.yaml has valid syntax')


def assertEquals(expected, actual):
    assert expected == actual, "\nExpected: %s\nActual:   %s" % (expected, actual)

assertEquals(
    {'#mediawiki-feed', '#wikimedia-qa', '#wikimedia-releng'},
    chanfilter.channels_for(['Continuous-Integration']))

assertEquals(
    {'#mediawiki-feed', '#wikimedia-devtools', '#wikimedia-releng'},
    chanfilter.channels_for(['Phabricator']))

print('Acceptance tests passed')
