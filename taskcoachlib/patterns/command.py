"""
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
"""

import taskcoachlib.patterns.singleton as patterns


class Command(object):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__()  # object.__init__ takes no arguments

    def do(self):
        CommandHistory().append(self)

    def undo(self):
        pass

    def redo(self):
        pass

    def __str__(self):
        return "command"


class CommandHistory(object):
    __metaclass__ = patterns.Singleton

    def __init__(self):
        self.__history = []
        self.__future = []

    def append(self, command):
        self.__history.append(command)
        del self.__future[:]

    def undo(self):
        if self.__history:
            command = self.__history.pop()
            command.undo()
            self.__future.append(command)

    def redo(self):
        if self.__future:
            command = self.__future.pop()
            command.redo()
            self.__history.append(command)

    def clear(self):
        del self.__history[:]
        del self.__future[:]

    def hasHistory(self):
        return self.__history

    def getHistory(self):
        return self.__history

    def hasFuture(self):
        return self.__future

    def getFuture(self):
        return self.__future

    def _extendLabel(self, label, commandList):
        if commandList:
            commandName = u" %s" % commandList[-1]
            label += commandName.lower()
        return label

    def undostr(self, label="Undo"):
        return self._extendLabel(label, self.__history)

    def redostr(self, label="Redo"):
        return self._extendLabel(label, self.__future)
