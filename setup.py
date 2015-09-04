import setuptools
from slackNotifier.version import Version


setuptools.setup(name='slackNotifier',
                 version=Version('1.0.0').number,
                 description='Supervisord Slack Notifier',
                 long_description=open('README.md').read().strip(),
                 author='Wojciech Iskra',
                 author_email='wojciech.iskra@schibsted.pl',
                 url='https://github.com/Schibsted-Tech-Polska/supervisord-slack-notifier',
                 py_modules=['slack_notifier'],
                 install_requires=[
                     'supervisor',
                     'pyslack-real==0.5.3',
                 ],
                 tests_require=[
                     'pytest==2.7.1',
                     'pytest-cov==1.8.1',
                 ],
                 license='MIT License',
                 zip_safe=False,
                 keywords='supervisord slack listener notifications',
                 classifiers=['Slack', 'Supervisord'])
