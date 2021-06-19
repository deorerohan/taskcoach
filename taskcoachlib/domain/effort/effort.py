'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2016 Task Coach developers <developers@taskcoach.org>
Copyright (C) 2008 Thomas Sonne Olesen <tpo@sonnet.dk>

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
from taskcoachlib.domain import date, base, task
from taskcoachlib.thirdparty.pubsub import pub
import base as baseeffort
import weakref


class Effort(baseeffort.BaseEffort, base.Object):
    def __init__(self, task=None, start=None, stop=None, *args, **kwargs):
        super(Effort, self).__init__(task, start or date.DateTime.now(), stop, 
            *args, **kwargs)
        self.__updateDurationCache()
        
    def setTask(self, task):
        if self._task is None: 
            # We haven't been fully initialised yet, so allow setting of the
            # task, without notifying observers. Also, don't call addEffort()
            # on the new task, because we assume setTask was invoked by the
            # new task itself.
            self._task = None if task is None else weakref.ref(task)
            return
        if task in (self.task(), None): 
            # command.PasteCommand may try to set the parent to None
            return
        event = patterns.Event()  # Change monitor needs one event to detect task change
        self._task().removeEffort(self)
        self._task = weakref.ref(task)
        self._task().addEffort(self)
        event.send()
        pub.sendMessage(self.taskChangedEventType(), newValue=task, sender=self)
        
    setParent = setTask  # FIXME: should we create a common superclass for Effort and Task?

    @classmethod
    def monitoredAttributes(class_):
        return base.Object.monitoredAttributes() + ['start', 'stop']

    def task(self):
        return None if self._task is None else self._task()

    @classmethod
    def taskChangedEventType(class_):
        return 'pubsub.effort.task'
    
    def __str__(self):
        return 'Effort(%s, %s, %s)' % (self.task(), self._start, self._stop)
    
    __repr__ = __str__
        
    def __getstate__(self):
        state = super(Effort, self).__getstate__()
        state.update(dict(task=self.task(), start=self._start, stop=self._stop))
        return state

    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super(Effort, self).__setstate__(state, event=event)
        self.setTask(state['task'])
        self.setStart(state['start'])
        self.setStop(state['stop'])

    def __getcopystate__(self):
        state = super(Effort, self).__getcopystate__()
        state.update(dict(task=self.task(), start=self._start, stop=self._stop))
        return state
   
    def duration(self, now=date.DateTime.now):
        return now() - self._start if self.__cachedDuration is None else self.__cachedDuration
     
    def setStart(self, startDateTime):
        if startDateTime == self._start:
            return
        self._start = startDateTime
        self.__updateDurationCache()
        pub.sendMessage(self.startChangedEventType(), newValue=startDateTime,
                        sender=self)
        self.task().sendTimeSpentChangedMessage()
        self.sendDurationChangedMessage()
        if self.task().hourlyFee():
            self.sendRevenueChangedMessage()

    @classmethod
    def startChangedEventType(class_):
        return 'pubsub.effort.start'

    def setStop(self, newStop=None):
        if newStop is None:
            newStop = date.DateTime.now()
        elif newStop == date.DateTime.max:
            newStop = None
        if newStop == self._stop:
            return
        previousStop = self._stop
        self._stop = newStop
        self.__updateDurationCache()
        if newStop == None:
            pub.sendMessage(self.trackingChangedEventType(), newValue=True, 
                            sender=self)
            self.task().sendTrackingChangedMessage(tracking=True)
        elif previousStop == None:
            pub.sendMessage(self.trackingChangedEventType(), newValue=False,
                            sender=self)
            self.task().sendTrackingChangedMessage(tracking=False)
        self.task().sendTimeSpentChangedMessage()
        pub.sendMessage(self.stopChangedEventType(), newValue=self._stop,
                           sender=self)
        self.sendDurationChangedMessage()
        if self.task().hourlyFee():
            self.sendRevenueChangedMessage()
            
    @classmethod
    def stopChangedEventType(class_):
        return 'pubsub.effort.stop'
        
    def __updateDurationCache(self):
        self.__cachedDuration = self._stop - self._start if self._stop else None
        
    def isBeingTracked(self, recursive=False):  # pylint: disable=W0613
        return self._stop is None

    def revenue(self):
        return self.duration().hours() * self.task().hourlyFee()

    @staticmethod
    def periodSortFunction(**kwargs):
        # Sort by start of effort first, then make sure the Total entry comes
        # first and finally sort by task subject:
        return lambda effort: (effort.getStart(), effort.isTotal(),
                               effort.task().subject(recursive=True))
    
    @classmethod
    def periodSortEventTypes(class_):
        ''' The event types that influence the effort sort order. '''
        return (class_.startChangedEventType(), class_.taskChangedEventType(),
                task.Task.subjectChangedEventType())
            
    @classmethod    
    def modificationEventTypes(class_):
        eventTypes = super(Effort, class_).modificationEventTypes()
        return eventTypes + [class_.taskChangedEventType(), 
                             class_.startChangedEventType(), 
                             class_.stopChangedEventType()]
