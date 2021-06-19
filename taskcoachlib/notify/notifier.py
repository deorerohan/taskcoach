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

from taskcoachlib import operating_system


class AbstractNotifier(object):
    """
    Abstract base class for interfacing with notification systems
    (Growl, Snarl...).
    """

    notifiers = {}
    _enabled = True

    def getName(self):
        raise NotImplementedError

    def isAvailable(self):
        raise NotImplementedError

    def notify(self, title, summary, bitmap, **kwargs):
        raise NotImplementedError

    @classmethod
    def register(klass, notifier):
        if notifier.isAvailable():
            klass.notifiers[notifier.getName()] = notifier

    @classmethod
    def get(klass, name):
        return klass.notifiers.get(name, None)

    @classmethod
    def getSimple(klass):
        """
        Returns a notifier suitable for simple notifications. This
        defaults to Growl/Snarl/libnotify depending on their
        availability.
        """

        if klass._enabled:
            if operating_system.isMac():
                return klass.get('Growl') or klass.get('Task Coach')
            elif operating_system.isWindows():
                return klass.get('Snarl') or klass.get('Task Coach')
            else:
                return klass.get('libnotify') or klass.get('Task Coach')
        else:
            class DummyNotifier(AbstractNotifier):
                def getName(self):
                    return u'Dummy'
                def isAvailable(self):
                    return True
                def notify(self, title, summary, bitmap, **kwargs):
                    pass
            return DummyNotifier()

    @classmethod
    def disableNotifications(klass):
        klass._enabled = False

    @classmethod
    def names(klass):
        names = klass.notifiers.keys()
        names.sort()
        return names
