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
import test
from taskcoachlib import gui, config, persistence, operating_system
from taskcoachlib.domain import category, attachment


class DummyEvent(object):
    def Skip(self): # pragma: no cover
        pass
    

class CategoryEditorTest(test.wxTestCase):
    def setUp(self):
        super(CategoryEditorTest, self).setUp()
        self.settings = config.Settings(load=False)
        self.taskFile = persistence.TaskFile()
        self.categories = self.taskFile.categories()
        self.categories.extend(self.createCategories())
        self.editor = gui.dialog.editor.CategoryEditor(self.frame, 
            list(self.categories), self.settings, self.categories, 
            self.taskFile)

    def tearDown(self):
        # CategoryEditor uses CallAfter for setting the focus, make sure those 
        # calls are dealt with, otherwise they'll turn up in other tests
        if operating_system.isGTK():
            wx.Yield() # pragma: no cover 
        super(CategoryEditorTest, self).tearDown()
        self.taskFile.close()
        self.taskFile.stop()

    # pylint: disable=E1101,E1103,W0212
    
    def createCategories(self):
        # pylint: disable=W0201
        self.category = category.Category('Category to edit')
        self.attachment = attachment.FileAttachment('some attachment')
        self.category.addAttachments(self.attachment)
        return [self.category]

    def setSubject(self, newSubject):
        page = self.editor._interior[0]
        page._subjectEntry.SetFocus()
        page._subjectEntry.SetValue(newSubject)
        if operating_system.isGTK(): # pragma: no cover 
            page._subjectSync.onAttributeEdited(DummyEvent())
        else: # pragma: no cover 
            page._descriptionEntry.SetFocus()

    def setDescription(self, newDescription):
        page = self.editor._interior[0]
        page._descriptionEntry.SetFocus()
        page._descriptionEntry.SetValue(newDescription)
        if operating_system.isGTK(): # pragma: no cover 
            page._descriptionSync.onAttributeEdited(DummyEvent())
        else:  # pragma: no cover
            page._subjectEntry.SetFocus()
        
    def testCreate(self):
        self.assertEqual('Category to edit', self.editor._interior[0]._subjectEntry.GetValue())
    
    def testEditSubject(self):
        self.setSubject('Done')
        self.assertEqual('Done', self.category.subject())

    def testEditDescription(self):
        self.setDescription('Description')
        self.assertEqual('Description', self.category.description())        

    def testAddAttachment(self):
        self.editor._interior[2].viewer.onDropFiles(self.category, ['filename'])
        self.failUnless('filename' in [att.location() for att in self.category.attachments()])
        self.failUnless('filename' in [att.subject() for att in self.category.attachments()])
        
    def testRemoveAttachment(self):
        self.editor._interior[2].viewer.select(self.category.attachments())
        self.editor._interior[2].viewer.deleteItemCommand().do()
        self.assertEqual([], self.category.attachments())

    def testEditMutualExclusiveSubcategories(self):
        self.editor._interior[0]._exclusiveSubcategoriesCheckBox.SetValue(True)
        self.editor._interior[0]._exclusiveSubcategoriesSync.onAttributeEdited(DummyEvent())
        self.failUnless(self.category.hasExclusiveSubcategories())
        
    def testAddNote(self):
        viewer = self.editor._interior[1].viewer
        viewer.newItemCommand(viewer.presentation()).do() 
        self.assertEqual(1, len(self.category.notes()))
