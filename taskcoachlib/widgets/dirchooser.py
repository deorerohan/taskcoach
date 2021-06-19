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
from taskcoachlib.i18n import _


class DirectoryChooser(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(DirectoryChooser, self).__init__(*args, **kwargs)

        self.chooser = wx.DirPickerCtrl(self, wx.ID_ANY, u'')
        self.checkbx = wx.CheckBox(self, wx.ID_ANY, _('None'))

        sz = wx.BoxSizer(wx.VERTICAL)
        sz.Add(self.chooser, 1, wx.EXPAND)
        sz.Add(self.checkbx, 1)

        self.SetSizer(sz)
        self.Fit()

        wx.EVT_CHECKBOX(self.checkbx, wx.ID_ANY, self.OnCheck)

    def SetPath(self, pth):
        if pth:
            self.checkbx.SetValue(False)
            self.chooser.Enable(True)
            self.chooser.SetPath(pth)
        else:
            self.checkbx.SetValue(True)
            self.chooser.SetPath(u'')
            self.chooser.Enable(False)

    def GetPath(self):
        if not self.checkbx.GetValue():
            return self.chooser.GetPath()
        return u''

    def OnCheck(self, evt):
        self.chooser.Enable(not evt.IsChecked())
        self.chooser.SetPath('/') # Workaround for a wx bug
