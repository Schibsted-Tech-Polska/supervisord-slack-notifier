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

## Configuration
Add to supervisord.conf the following:
```
[eventlistener:slackNotifier]
command=/usr/bin/slackNotifier -t=%AUTH_TOKEN% -c=%CHANNEL_NAME%
events=PROCESS_STATE
```

## License

Released under the MIT License: http://www.opensource.org/licenses/mit-license.php
