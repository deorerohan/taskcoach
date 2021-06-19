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

import test

class DateTest(test.TestCase):
    def testNoQuestionMarkInMetaDataDate(self):
        from taskcoachlib import meta
        self.failIf('?' in meta.date)

    def testNoQuestionMarkInChangeLog(self):
        import sys, os.path
        sys.path.insert(0, os.path.join(test.projectRoot, 'changes.in'))
        import changes # pylint: disable=F0401
        self.failIf('?' in changes.releases[0].date)
