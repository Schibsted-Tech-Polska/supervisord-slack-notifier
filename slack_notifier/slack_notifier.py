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

-p -- specify a supervisor process_name.  Send mail when this process
      transitions to the EXITED state unexpectedly. If this process is
      part of a group, it can be specified using the
      'process_name:group_name' syntax.

-a -- Send mail when any child of the supervisord transitions
    unexpectedly to the EXITED state unexpectedly.  Overrides any -p
    parameters passed in the same crashmail process invocation.


-c -- Channel to send notifications to

-t -- Web API auth token

The -p option may be specified more than once, allowing for
specification of multiple processes.  Specifying -a overrides any
selection of -p.

A sample invocation:

slack_notifier.py -p=program1 -p=group1:program2 -t=dckjhgvfuhvdf -c='#general'

"""

import os
import sys
import socket

from pyslack import SlackClient
from supervisor import childutils


def usage():
    print(doc)
    sys.exit(255)


class SlackNotifier:

    def __init__(self, slackClient, programs, any, channel):

        self.slackClient = slackClient
        self.programs = programs
        self.any = any
        self.channel = channel
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def runforever(self, test=False):
        while 1:
            # we explicitly use self.stdin, self.stdout, and self.stderr
            # instead of sys.* so we can unit test this code
            headers, payload = childutils.listener.wait(
                self.stdin, self.stdout)

            pheaders, pdata = childutils.eventdata(payload+'\n')

            msg = socket.gethostname() + ': process *' + pheaders['groupname'] + ':' + pheaders['processname'] + '* changed status from *' + pheaders['from_state'] + '* to *' + headers['eventname'] +'*'

            self.stderr.write('unexpected exit, sending notification\n')
            self.stderr.flush()

            self.send(msg)

            childutils.listener.ok(self.stdout)
            if test:
                break

    def send(self, msg):
        self.slackClient.chat_post_message(self.channel, '', username='Supervisord', icon_emoji=':doge:', attachments='[{"text": "' + msg +'", "color": "warning", "mrkdwn_in": ["text"]}]')

def main(argv=sys.argv):
    import getopt
    short_args = "hp:at:c:"
    long_args = [
        "help",
        "program=",
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
    any = True
    channel = '#vg-platform-team'
    token = ''

    for option, value in opts:

        if option in ('-h', '--help'):
            usage()

        if option in ('-p', '--program'):
            programs.append(value)

        if option in ('-a', '--any'):
            any = True

        if option in ('-t', '--token'):
            token = value

        if option in ('-c', '--channel'):
            channel = value

    if not 'SUPERVISOR_SERVER_URL' in os.environ:
        sys.stderr.write('slack must be run as a supervisor event '
                         'listener\n')
        sys.stderr.flush()
        return

    sys.stderr.flush()
    slackClient = SlackClient(token)

    prog = SlackNotifier(slackClient, programs, any, channel)
    prog.runforever()


if __name__ == '__main__':
    main()
