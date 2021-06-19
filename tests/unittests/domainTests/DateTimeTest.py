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
from taskcoachlib.domain import date


class PyDateTimeTest(test.TestCase):
    def testReplaceCannotBeEasilyUsedToFindTheLastDayofTheMonth(self):
        testDate = datetime.date(2004, 4, 1) # April 1st, 2004
        try:
            lastDayOfApril = testDate.replace(day=31)
            self.fail('Surprise! datetime.date.replace works as we want!') # pragma: no cover
            self.assertEqual(datetime.date(2004, 4, 30), lastDayOfApril) # pragma: no cover
        except ValueError:
            pass


class DateTimeTest(test.TestCase):
    def testWeekNumber(self):
        self.assertEqual(53, date.DateTime(2005,1,1).weeknumber())
        self.assertEqual(1, date.DateTime(2005,1,3).weeknumber())   
        
    def testStartOfDay(self):
        startOfDay = date.DateTime(2005,1,1,0,0,0,0)
        noonish = date.DateTime(2005,1,1,12,30,15,400)
        self.assertEqual(startOfDay, noonish.startOfDay())
        
    def testEndOfDay(self):
        endOfDay = date.DateTime(2005,1,1,23,59,59,999999)
        noonish = date.DateTime(2005,1,1,12,30,15,400)
        self.assertEqual(endOfDay, noonish.endOfDay())
        
    def testStartOfWorkWeekOnWednesday(self):
        startOfWorkWeek = date.DateTime(2011,7,25,0,0,0,0)
        wednesday = date.DateTime(2011,7,27,8,39,10)
        self.assertEqual(startOfWorkWeek, wednesday.startOfWorkWeek())
        
    def testStartOfWorkWeekOnMonday(self):
        startOfWorkWeek = date.DateTime(2011,7,25,0,0,0,0)
        monday = date.DateTime(2011,7,25,8,39,10)
        self.assertEqual(startOfWorkWeek, monday.startOfWorkWeek())

    def testStartOfWorkWeekOnSunday(self):
        startOfWorkWeek = date.DateTime(2011,7,18,0,0,0,0)
        sunday = date.DateTime(2011,7,24,8,39,10)
        self.assertEqual(startOfWorkWeek, sunday.startOfWorkWeek())
        
    def testEndOfWorkWeek(self):
        endOfWorkWeek = date.DateTime(2010,5,7,23,59,59,999999)
        midweek = date.DateTime(2010,5,5,12,30,15,200000)
        self.assertEqual(endOfWorkWeek, midweek.endOfWorkWeek())

    def testEndOfWorkWeek_OnSaturday(self):
        endOfWorkWeek = date.DateTime(2010,5,7,23,59,59,999999)
        midweek = date.DateTime(2010,5,1,12,30,15,200000)
        self.assertEqual(endOfWorkWeek, midweek.endOfWorkWeek())
        
    def testLastDayOfCurrentMonth_InFebruary2004(self):
        expected = date.DateTime(2004, 2, 29)
        actual = date.LastDayOfCurrentMonth(localtime=lambda: (2004, 2, 1))
        self.assertEqual(expected, actual)

    def testLastDayOfCurrentMonth_InDecember(self):
        expected = date.DateTime(2003, 12, 31)
        actual = date.LastDayOfCurrentMonth(localtime=lambda: (2003, 12, 1))
        self.assertEqual(expected, actual)

    def testFormat1900(self):
        self.assertEqual(date.DateTime(2, 5, 19, 0, 0, 0).strftime('%Y%m%d'), '20519')
