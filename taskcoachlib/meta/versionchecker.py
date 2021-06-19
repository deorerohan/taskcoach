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

import taskcoachlib.meta.data
import threading
import urllib3
import sys
import traceback


class VersionChecker(threading.Thread):
    def __init__(self, settings, verbose=False):
        self.settings = settings
        self.verbose = verbose
        super(VersionChecker, self).__init__()

    def _set_daemon(self):
        return True  # Don't block application exit

    def run(self):
        from taskcoachlib.gui.dialog import version

        try:
            latestVersionString = self.getLatestVersion()
            latestVersion = self.tupleVersion(latestVersionString)
            lastVersionNotified = self.tupleVersion(self.getLastVersionNotified())
            currentVersion = self.tupleVersion(data.version)
        except:
            if self.verbose:
                self.notifyUser(
                    version.NoVersionDialog,
                    message="".join(
                        traceback.format_exception_only(sys.exc_type, sys.exc_value)
                    ),
                )
        else:
            if latestVersion < currentVersion and self.verbose:
                self.notifyUser(version.PrereleaseVersionDialog, latestVersionString)
            elif latestVersion == currentVersion and self.verbose:
                self.notifyUser(version.VersionUpToDateDialog, latestVersionString)
            elif latestVersion > currentVersion and (
                self.verbose or latestVersion > lastVersionNotified
            ):
                self.setLastVersionNotified(latestVersionString)
                self.notifyUser(version.NewVersionDialog, latestVersionString)

    def getLatestVersion(self):
        versionText = self.parseVersionFile(self.retrieveVersionFile())
        return versionText.strip()

    def notifyUser(self, dialog, latestVersion="", message=""):
        # Must use CallAfter because this is a non-GUI thread
        # Import wx here so it isn't a build dependency
        import wx

        wx.CallAfter(self.showDialog, dialog, latestVersion, message)

    def showDialog(self, VersionDialog, latestVersion, message=""):
        import wx

        dialog = VersionDialog(
            wx.GetApp().GetTopWindow(),
            version=latestVersion,
            message=message,
            settings=self.settings,
        )
        dialog.Show()
        return dialog

    def getLastVersionNotified(self):
        return self.settings.get("version", "notified")

    def setLastVersionNotified(self, lastVersionNotifiedString):
        self.settings.set("version", "notified", lastVersionNotifiedString)

    @staticmethod
    def parseVersionFile(versionFile):
        return versionFile.readline()

    @staticmethod
    def retrieveVersionFile():
        return urllib2.urlopen(data.version_url)

    @staticmethod
    def tupleVersion(versionString):
        return tuple(int(i) for i in versionString.split("."))
