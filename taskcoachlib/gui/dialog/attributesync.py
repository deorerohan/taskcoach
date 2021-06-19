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

from taskcoachlib import patterns
from taskcoachlib.thirdparty.pubsub import pub
from taskcoachlib.i18n import _
import wx


class AttributeSync(object):
    ''' Class used for keeping an attribute of a domain object synchronized with
        a control in a dialog. If the user edits the value using the control, 
        the domain object is changed, using the appropriate command. If the 
        attribute of the domain object is changed (e.g. in another dialog) the 
        value of the control is updated. '''
        
    def __init__(self, attributeGetterName, entry, currentValue, items, 
                 commandClass, editedEventType, changedEventType, callback=None, 
                 **kwargs):
        self._getter = attributeGetterName
        self._entry = entry
        self._currentValue = currentValue
        self._items = items
        self._commandClass = commandClass
        self.__commandKwArgs = kwargs
        self.__changedEventType = changedEventType
        self.__callback = callback
        entry.Bind(editedEventType, self.onAttributeEdited)
        if len(items) == 1:
            self.__start_observing_attribute(changedEventType, items[0])
        
    def onAttributeEdited(self, event):
        event.Skip()
        new_value = self.getValue()
        if new_value != self._currentValue:
            self._currentValue = new_value
            commandKwArgs = self.commandKwArgs(new_value)
            self._commandClass(None, self._items, **commandKwArgs).do()  # pylint: disable=W0142
            self.__invokeCallback(new_value)

    def onAttributeChanged_Deprecated(self, event):  # pylint: disable=W0613
        if self._entry: 
            new_value = getattr(self._items[0], self._getter)()
            if new_value != self._currentValue:
                self._currentValue = new_value
                self.setValue(new_value)
                self.__invokeCallback(new_value)
        else:
            self.__stop_observing_attribute()
            
    def onAttributeChanged(self, newValue, sender):
        if sender in self._items:
            if self._entry:
                if newValue != self._currentValue:
                    self._currentValue = newValue
                    self.setValue(newValue)
                    self.__invokeCallback(newValue)
            else:
                self.__stop_observing_attribute()
            
    def commandKwArgs(self, new_value):
        self.__commandKwArgs['newValue'] = new_value
        return self.__commandKwArgs
    
    def setValue(self, new_value):
        self._entry.SetValue(new_value)
            
    def getValue(self):
        return self._entry.GetValue()

    def __invokeCallback(self, value):
        if self.__callback is not None:
            try:
                self.__callback(value)
            except Exception, e:
                wx.MessageBox(unicode(e), _('Error'), wx.OK)

    def __start_observing_attribute(self, eventType, eventSource):
        if eventType.startswith('pubsub'):
            pub.subscribe(self.onAttributeChanged, eventType)
        else:
            patterns.Publisher().registerObserver(self.onAttributeChanged_Deprecated,
                                                  eventType=eventType,
                                                  eventSource=eventSource)
    
    def __stop_observing_attribute(self):
        try:
            pub.unsubscribe(self.onAttributeChanged, self.__changedEventType)
        except pub.TopicNameError:
            pass
        patterns.Publisher().removeObserver(self.onAttributeChanged_Deprecated)


class FontColorSync(AttributeSync):
    def setValue(self, newValue):
        self._entry.SetColor(newValue)

    def getValue(self):
        return self._entry.GetColor()
