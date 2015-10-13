#!/usr/bin/env python
##############################################################################
#
# Copyright (c) 2007 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

# A event listener meant to be subscribed to PROCESS_STATE_CHANGE
# events.  It will send notification when processes that are children of
# supervisord transition unexpectedly to the EXITED state.

# A supervisor config snippet that tells supervisor to use this script
# as a listener is below.
#
# [eventlistener:slack_notifier]
# command =
#     ./slack_notifier
#         -t=token
#         -c=channel
# events=PROCESS_STATE

doc = """\
slack_notifier.py [-p processname] [-a] [-c channel] -t token

Options:

-p -- specify a supervisor process_name. Notify when the process goes to any of the 'followed' states.
    If this process is part of a group, it can be specified using the
      'process_name:group_name' syntax.

-a -- Notify about ALL processes.  Overrides any -p
    parameters passed in the same crashmail process invocation.

-e -- follow only transitions to these events. This overrides event list in config.py

-c -- Channel to send notifications to. Can be either:
    '#public_channel',
    '@private_group',
    'CHANNEL_ID',

-t -- Web API auth token

The -p and -e options may be specified more than once, allowing for
specification of multiple processes and events.  Specifying -a overrides any
selection of -p.

A sample invocation:

slack_notifier.py -p=program1 -p=group1:program2 -t=dckjhgvfuhvdf -c='#general'

"""

import config
import os
import sys
import socket
import json
import datetime

from pprint import pprint
from pyslack import SlackClient
from supervisor import childutils


def usage():
    print(doc)
    sys.exit(255)


class SlackNotifier:

    def __init__(self, slackClient, programs, any, events, channel):

        self.slackClient = slackClient
        self.programs = programs
        self.events = events
        self.any = any
        self.channel = channel
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def runforever(self, test=False):
        while 1:
            # we explicitly use self.stdin, self.stderr, and self.stderr
            # instead of sys.* so we can unit test this code
            headers, payload = childutils.listener.wait(
                self.stdin, self.stdout)

            pheaders, pdata = childutils.eventdata(payload+'\n')

            if not headers['eventname'] in self.events:
                # do nothing with non-TICK events
                childutils.listener.ok(self.stdout)
                if test:
                    self.stderr.write(pheaders['from_state'] + ' --> ' + headers['eventname'] + ': non-exited event\n')
                    self.stderr.flush()
                    break
                continue

            if not self.any and not pheaders['processname'] in self.programs:
                childutils.listener.ok(self.stdout)
                if test:
                    self.stderr.write('not followed program event\n')
                    self.stderr.flush()
                    break
                continue

            msg = 'Process *' +\
                pheaders['groupname'] + ':' + pheaders['processname'] +\
                '* went from *' + pheaders['from_state'] +\
                '* to *' + headers['eventname'] + '*'

            self.send(headers['eventname'], msg)

            childutils.listener.ok(self.stdout)
            if test:
                break

    def send(self, eventName, msg):
        attachments = [{
            'text': msg + ' ' + config.events[eventName]['emoji'],
            'color': config.events[eventName]['color'],
            'mrkdwn_in': ['text'],
            'fields': [
                {
                    'title': 'Server',
                    'value': socket.gethostname(),
                    'short': True
                },
                {
                    'title': 'Date',
                    'value': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
                    'short': True
                }
            ],
        }]

        self.slackClient.chat_post_message(
            self.channel,
            '',
            username='Supervisord',
            icon_emoji=':doge:',
            attachments=json.dumps(attachments)
            )


def main(argv=sys.argv):
    import getopt
    short_args = "hp:e:at:c:"
    long_args = [
        "help",
        "program=",
        "event=",
        "any",
        "token="
        "channel=",
        ]
    arguments = argv[1:]
    try:
        opts, args = getopt.getopt(arguments, short_args, long_args)
    except:
        usage()

    programs = []
    events = []
    any = False
    channel = ''
    token = ''

    for option, value in opts:

        if option in ('-h', '--help'):
            usage()

        if option in ('-p', '--program'):
            programs.append(value)

        if option in ('-e', '--event'):
            events.append(value)

        if option in ('-a', '--any'):
            any = True

        if option in ('-t', '--token'):
            token = value

        if option in ('-c', '--channel'):
            channel = value

    if not events:
        events = config.events.keys()

    if 'SUPERVISOR_SERVER_URL' not in os.environ:
        sys.stderr.write('slack must be run as a supervisor event '
                         'listener\n')
        sys.stderr.flush()
        return

    sys.stderr.flush()
    slackClient = SlackClient(token)

    prog = SlackNotifier(slackClient, programs, any, events, channel)
    prog.runforever()


if __name__ == '__main__':
    main()
