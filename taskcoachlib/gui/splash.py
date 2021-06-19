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

import wx
from taskcoachlib import i18n
try:
    import icons
except ImportError: # pragma: no cover   
    print "ERROR: couldn't import icons.py."
    print 'You need to generate the icons file.'
    print 'Run "make prepare" in the Task Coach root folder.'
    import sys
    sys.exit(1)


class SplashScreen(wx.SplashScreen):
    def __init__(self):
        splash = icons.catalog['splash']
        if i18n.currentLanguageIsRightToLeft():
            # RTL languages cause the bitmap to be mirrored too, but because
            # the splash image is not internationalized, we have to mirror it
            # (back). Unfortunately using SetLayoutDirection() on the 
            # SplashWindow doesn't work.
            bitmap = wx.BitmapFromImage(splash.getImage().Mirror())
        else:
            bitmap = splash.getBitmap()
        super(SplashScreen, self).__init__(bitmap,
            wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT, 4000, None, -1)

