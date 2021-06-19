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

import test, datetime
from taskcoachlib import meta


class VersionNumberTest(test.TestCase):
    def testVersionHasMajorMinorAndPatchLevel(self):
        expectedParts = 4 if meta.data.revision else 3
        self.assertEqual(expectedParts, len(meta.data.version.split('.')))
        
    def testVersionComponentsAreIntegers(self):
        for component in meta.data.version.split('.'):
            self.assertEqual(component, str(int(component)))
            
    def testTskVersionIsInteger(self):
        self.assertEqual(int, type(meta.data.tskversion))
        
    def testReleaseStatus(self):
        self.failUnless(meta.data.release_status in ['alpha', 'beta', 'stable'])
        
    def testReleaseDate(self):
        datetime.date(int(meta.data.release_year), 
                      meta.data.months.index(meta.data.release_month)+1, 
                      int(meta.data.release_day))
