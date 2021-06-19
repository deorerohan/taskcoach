'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2016 Task Coach developers <developers@taskcoach.org>
Copyright (C) 2008 Rob McMullen <rob.mcmullen@gmail.com>
Copyright (C) 2008 Carl Zmola <zmola@acm.org>

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


# The native SpinCtrl on Windows has no TextCtrl API which means we cannot make
# the Delete key work (see uicommand.py::Delete). Our own SpinCtrl below 
# doesn't have this disadvantage.
    
class SpinCtrl(wx.Panel):
    maxRange = 2147483647 # 2^31
    
    def __init__(self, parent, wxId=wx.ID_ANY, value=0, pos=wx.DefaultPosition, size=wx.DefaultSize, 
                 style=0, name='wx.SpinCtrl', **kwargs): # pylint: disable=W0613
        super(SpinCtrl, self).__init__(parent, wxId, pos=pos, size=size, name=name)
        minValue = kwargs['min'] if 'min' in kwargs else -self.maxRange
        maxValue = kwargs['max'] if 'max' in kwargs else self.maxRange
        value = min(maxValue, max(int(value), minValue))
        self._textCtrl = wx.TextCtrl(self, value=str(value))
        self._spinButton = wx.SpinButton(self, size=(-1, self._textCtrl.GetSize()[1]), 
                                         style=wx.SP_VERTICAL|wx.SP_ARROW_KEYS)
        self._spinButton.SetRange(minValue, maxValue)
        self._spinButton.SetValue(value)
        self._textCtrl.SetMinSize((size[0]-self._spinButton.GetSize()[0], -1))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([self._textCtrl, self._spinButton])
        self.SetSizerAndFit(sizer)
        self._textCtrl.Bind(wx.EVT_TEXT, self.onText)
        self._textCtrl.Bind(wx.EVT_KEY_DOWN, self.onKey)
        self._textCtrl.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self._spinButton.Bind(wx.EVT_SPIN, self.onSpin)
        
    def onText(self, event):
        event.Skip()
        try:
            newValue = int(event.GetString()) 
            if newValue != self._spinButton.GetValue():
                self._spinButton.SetValue(newValue)
                self.__postEvent()
        except (ValueError, OverflowError):
            self._textCtrl.SetValue(str(self._spinButton.GetValue()))

    def onKey(self, event):
        deltaByKeyCode = {wx.WXK_UP: 1, wx.WXK_NUMPAD_UP: 1, 
                          wx.WXK_DOWN: -1, wx.WXK_NUMPAD_DOWN: -1,
                          wx.WXK_PAGEUP: 10, wx.WXK_NUMPAD_PAGEUP: 10,
                          wx.WXK_PAGEDOWN: -10, wx.WXK_NUMPAD_PAGEDOWN: -10}
        delta = 0 if event.HasModifiers() else deltaByKeyCode.get(event.GetKeyCode(), 0)
        if delta:
            self.SetValue(self.GetValue() + delta)
            self.__postEvent()
        else:
            event.Skip()
        
    def onSetFocus(self, event):
        self._textCtrl.SelectAll()
        event.Skip()
            
    def onSpin(self, event): # pylint: disable=W0613
        self._textCtrl.SetValue(str(self._spinButton.GetValue()))
        self.__postEvent()

    def GetValue(self):
        return self._spinButton.GetValue()
    
    def SetValue(self, value):
        self._spinButton.SetValue(value) 
        # Get the value from the spinButton because it is guaranteed to be
        # within the min/max range.
        self._textCtrl.SetValue(str(self.GetValue()))

    Value = property(GetValue, SetValue)
    
    def GetMax(self):
        return self._spinButton.GetMax()
    
    def GetMin(self):
        return self._spinButton.GetMin()
    
    def __postEvent(self):
        wx.PostEvent(self, wx.SpinEvent(wx.wxEVT_COMMAND_SPINCTRL_UPDATED, self.GetId()))
 
