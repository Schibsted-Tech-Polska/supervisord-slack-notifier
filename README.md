supervisord-slack-notifier
==========================

[![Build Status](https://travis-ci.org/Schibsted-Tech-Polska/supervisord-slack-notifier.svg)](https://travis-ci.org/Schibsted-Tech-Polska/supervisord-slack-notifier)

Event listener for Supervisord that sends notifications to Slack via Web API

## Package

Basic structure of package is

```
--- slackNotifier
  \ slackNotifier.py
  \ version.py
--- tests
  \ tests_helper.py
  --- unit    # Unit Tests
  --- helpers # Test Helpers
\ requirements.txt
\ setup.py
```

## Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

## Tests

Testing is set up using [pytest](http://pytest.org) and coverage is handled
with the pytest-cov plugin.

Run your tests with ```py.test``` in the root directory.

Coverage is ran by default and is set in the ```pytest.ini``` file.
To see an html output of coverage open ```htmlcov/index.html``` after running the tests.

## Travis CI

There is a ```.travis.yml``` file that is set up to run your tests for python 2.7
and python 3.2, should you choose to use it.

## License

Released under the MIT License: http://www.opensource.org/licenses/mit-license.php
