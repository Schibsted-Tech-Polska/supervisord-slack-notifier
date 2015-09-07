supervisord-slack-notifier
==========================

[![Build Status](https://travis-ci.org/Schibsted-Tech-Polska/supervisord-slack-notifier.svg)](https://travis-ci.org/Schibsted-Tech-Polska/supervisord-slack-notifier)

Event listener for Supervisord that sends notifications to Slack via Web API

# Installation

### Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

### Tests

Testing is set up using [pytest](http://pytest.org) and coverage is handled
with the pytest-cov plugin.

Run your tests with ```py.test``` in the root directory.

Coverage is ran by default and is set in the ```pytest.ini``` file.
To see an html output of coverage open ```htmlcov/index.html``` after running the tests.

### Travis CI

There is a ```.travis.yml``` file that is set up to run your tests for python 2.7
and python 3.2, should you choose to use it.

## Set up
To get the package up and running run

```
./setup.py install
```

Add to supervisord.conf the following:
```
[eventlistener:slack_notifier]
command=/path/to/slack_notifier -t=%AUTH_TOKEN% -c=%CHANNEL_NAME% -a
events=PROCESS_STATE
```

##Options

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


## License

Released under the MIT License: http://www.opensource.org/licenses/mit-license.php
