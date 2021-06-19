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

import wx, os
from taskcoachlib.persistence import BackupManifest
from taskcoachlib.i18n import _
from taskcoachlib import render


class BackupManagerDialog(wx.Dialog):
    def __init__(self, parent, settings, selectedFile=None):
        super(BackupManagerDialog, self).__init__(parent, wx.ID_ANY, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        container = wx.Panel(self)
        self.__files = wx.ListCtrl(container, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.__files.InsertColumn(0, _('File'))
        self.__files.InsertColumn(1, _('Full path'))
        self.__backups = wx.ListCtrl(container, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.__backups.InsertColumn(0, _('Date'))
        self.__backups.Enable(False)
        self.__btnRestore = wx.Button(container, wx.ID_ANY, _('Restore'))
        self.__btnRestore.Enable(False)
        self.__filename = selectedFile
        self.__selection = (None, None)

        vsz = wx.BoxSizer(wx.VERTICAL)
        hsz = wx.BoxSizer(wx.HORIZONTAL)
        hsz.Add(self.__files, 1, wx.EXPAND|wx.ALL, 3)
        hsz.Add(self.__backups, 1, wx.EXPAND|wx.ALL, 3)
        hsz.Add(self.__btnRestore, 0, wx.ALIGN_TOP|wx.ALL, 3)
        vsz.Add(hsz, 1, wx.EXPAND)

        container.SetSizer(vsz)

        vsz = wx.BoxSizer(wx.VERTICAL)
        vsz.Add(container, 1, wx.EXPAND)
        btn = wx.Button(self, wx.ID_ANY, _('Close'))
        vsz.Add(btn, 0, wx.ALL|wx.ALIGN_RIGHT, 3)
        self.SetSizer(vsz)

        self.__manifest = BackupManifest(settings)
        self.__filenames = self.__manifest.listFiles()
        selection = None
        for filename in self.__filenames:
            item = self.__files.InsertStringItem(self.__files.GetItemCount(), os.path.split(filename)[-1])
            self.__files.SetStringItem(item, 1, filename)
            if filename == selectedFile:
                selection = item

        self.SetSize(wx.Size(600, 400))
        self.CentreOnParent()

        wx.EVT_BUTTON(btn, wx.ID_ANY, self.DoClose)
        wx.EVT_LIST_ITEM_SELECTED(self.__files, wx.ID_ANY, self._OnSelectFile)
        wx.EVT_LIST_ITEM_DESELECTED(self.__files, wx.ID_ANY, self._OnDeselectFile)
        wx.EVT_LIST_ITEM_SELECTED(self.__backups, wx.ID_ANY, self._OnSelectBackup)
        wx.EVT_LIST_ITEM_DESELECTED(self.__backups, wx.ID_ANY, self._OnDeselectBackup)
        wx.EVT_BUTTON(self.__btnRestore, wx.ID_ANY, self._OnRestore)

        if selection is not None:
            self.__files.SetItemState(selection, wx.LIST_STATE_FOCUSED|wx.LIST_STATE_SELECTED, wx.LIST_STATE_FOCUSED|wx.LIST_STATE_SELECTED)
        self.__files.SetColumnWidth(0, -1)
        self.__files.SetColumnWidth(1, -1)

    def restoredFilename(self):
        return self.__filename

    def DoClose(self, event):
        self.EndModal(wx.ID_CANCEL)

    def _OnSelectFile(self, event):
        self.__backups.DeleteAllItems()
        for index, dateTime in enumerate(self.__manifest.listBackups(self.__filenames[event.GetIndex()])):
            self.__backups.InsertStringItem(index, render.dateTime(dateTime, humanReadable=True))
        self.__backups.SetColumnWidth(0, -1)
        self.__backups.Enable(True)
        self.__selection = (self.__filenames[event.GetIndex()], None)

    def _OnDeselectFile(self, event):
        self.__btnRestore.Enable(False)
        self.__backups.DeleteAllItems()
        self.__backups.Enable(False)
        self.__selection = (None, None)

    def _OnSelectBackup(self, event):
        self.__btnRestore.Enable(True)
        filename = self.__selection[0]
        self.__selection = (filename, self.__manifest.listBackups(filename)[event.GetIndex()])

    def _OnDeselectBackup(self, event):
        self.__btnRestore.Enable(False)
        self.__selection = (self.__selection[0], None)

    def _OnRestore(self, event):
        filename, dateTime = self.__selection
        dlg = wx.FileDialog(self, _('Choose the restoration destination'),
                            defaultDir=os.path.dirname(filename),
                            defaultFile=os.path.split(filename)[-1],
                            wildcard='*.tsk', style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.__filename = dlg.GetPath()
                self.__manifest.restoreFile(filename, dateTime, self.__filename)
                self.EndModal(wx.ID_OK)
        finally:
            dlg.Destroy()
