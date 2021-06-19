#!/usr/bin/env python

'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2016 Task Coach developers <developers@taskcoach.org>

Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from distutils.core import setup
from taskcoachlib import meta
import platform
import os
import sys


def findPackages(base):
    if not os.path.exists(base):
        return list()

    result = [base.replace('/', '.')]

    for name in os.listdir(base):
        fname = os.path.join(base, name)
        if os.path.isdir(fname) and \
               os.path.exists(os.path.join(fname, '__init__.py')):
            result.extend(findPackages(fname))
    return result


def majorAndMinorPythonVersion():
    info = sys.version_info
    try:
        return info.major, info.minor
    except AttributeError:
        return info[0], info[1]
    

setupOptions = { 
    'name': meta.filename,
    'author': meta.author,
    'author_email': meta.author_email,
    'description': meta.description,
    'long_description': meta.long_description,
    'version': meta.version,
    'url': meta.url,
    'license': meta.license,
    'download_url': meta.download,
    'packages': findPackages('taskcoachlib') + findPackages('buildlib'),
    'scripts': ['taskcoach.py'],
    'classifiers': [\
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business']}

# Add available translations:
languages = sorted([name for name, (code, enabled) in meta.data.languages.items() if enabled])
for language in languages:
    setupOptions['classifiers'].append('Natural Language :: %s' % 'English' if languages == 'English (US)' else 'Natural Language :: %s' % language)

system = platform.system()
if system == 'Linux':
    # Add data files for Debian-based systems:
    current_dist = [dist.lower() for dist in platform.dist()]
    if 'debian' in current_dist or 'ubuntu' in current_dist:
        setupOptions['data_files'] = [('share/applications', ['build.in/linux_common/taskcoach.desktop']), 
                                      ('share/appdata', ['build.in/debian/taskcoach.appdata.xml']),
                                      ('share/pixmaps', ['icons.in/taskcoach.png'])]
elif system == 'Windows':
    setupOptions['scripts'].append('taskcoach.pyw')
    major, minor = majorAndMinorPythonVersion()
    sys.path.insert(0, os.path.join('taskcoachlib', 'bin.in', 'windows', 'py%d%d' % (major, minor)))
    import _pysyncml
    # ...
    # ModuleFinder can't handle runtime changes to __path__, but win32com uses them
    try:
        # py2exe 0.6.4 introduced a replacement modulefinder.
        # This means we have to add package paths there, not to the built-in
        # one.  If this new modulefinder gets integrated into Python, then
        # we might be able to revert this some day.
        # if this doesn't work, try import modulefinder
        try:
            import py2exe.mf as modulefinder
        except ImportError:
            import modulefinder
        import win32com, sys
        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", p)
        for extra in ["win32com.shell"]: #,"win32com.mapi"
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)
    except ImportError:
        # no build path setup, no worries.
        pass
elif system == 'Darwin':
    # When packaging for MacOS, choose the right binary depending on
    # the platform word size. Actually, we're always packaging on 32
    # bits.
    import struct
    wordSize = '32' if struct.calcsize('L') == 4 else '64'
    sys.path.insert(0, os.path.join('taskcoachlib', 'bin.in', 'macos', 'IA%s' % wordSize))
    sys.path.insert(0, os.path.join('extension', 'macos', 'bin-ia32'))
    # pylint: disable=F0401,W0611
    import _powermgt
    import _idle


if __name__ == '__main__':
    setup(**setupOptions)  # pylint: disable=W0142
