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
from taskcoachlib import gui, config



class PrinterTest(test.TestCase):
    def setUp(self):
        super(PrinterTest, self).setUp()
        self.settings = config.Settings(load=False)
        self.margins = dict(top=1, left=2, bottom=3, right=4)
        self.printerSettings = gui.printer.PrinterSettings(self.settings)
        self.pageSetupData = wx.PageSetupDialogData()

    def tearDown(self):
        super(PrinterTest, self).tearDown()
        self.resetPrinterSettings()
        
    def resetPrinterSettings(self):
        gui.printer.PrinterSettings.deleteInstance() # pylint: disable=E1101
 
    def testInitialSettings(self):
        printerSettings = self.printerSettings
        self.assertEqual(wx.Point(0, 0), printerSettings.GetMarginTopLeft())
        self.assertEqual(0, printerSettings.GetPaperId())
        self.assertEqual(wx.PORTRAIT, printerSettings.GetOrientation())

    def testSetMargin(self):
        self.pageSetupData.SetMarginTopLeft(wx.Point(10, 1))
        self.printerSettings.updatePageSetupData(self.pageSetupData)
        self.assertEqual(wx.Point(10, 1), 
                         self.printerSettings.GetMarginTopLeft())

    def testDefaultMarginsFromSettings(self):
        settings = self.settings
        for margin in self.margins:
            self.assertEqual(0, settings.getint('printer', 'margin_'+margin))

    def testSetPaperId(self):
        self.pageSetupData.SetPaperId(1)
        self.printerSettings.updatePageSetupData(self.pageSetupData)
        self.assertEqual(1, self.printerSettings.GetPaperId())

    def testDefaultPaperIdFromSettings(self):
        self.assertEqual(0, self.settings.getint('printer', 'paper_id'))

    def testSetOrientation(self):
        self.pageSetupData.GetPrintData().SetOrientation(wx.LANDSCAPE)
        self.printerSettings.updatePageSetupData(self.pageSetupData)
        self.assertEqual(wx.LANDSCAPE, self.printerSettings.GetOrientation())

    def testDefaultOrientationFromSettings(self):
        self.assertEqual(wx.PORTRAIT, 
                         self.settings.getint('printer', 'orientation'))

    def testUpdateMarginsInPageSetupDataUpdatesSettings(self):
        self.pageSetupData.SetMarginTopLeft(wx.Point(self.margins['left'],
                                                     self.margins['top']))
        self.pageSetupData.SetMarginBottomRight(wx.Point(self.margins['right'], 
                                                         self.margins['bottom']))
        self.printerSettings.updatePageSetupData(self.pageSetupData)
        for margin in self.margins:
            self.assertEqual(self.margins[margin], 
                             self.settings.getint('printer', 'margin_'+margin))

    def testUpdatePaperIdInPageSetupDataUpdatesSettings(self):
        self.pageSetupData.SetPaperId(1)
        self.printerSettings.updatePageSetupData(self.pageSetupData)
        self.assertEqual(1, self.settings.getint('printer', 'paper_id'))

    def testUpdateOrientationInPageSetupDataUpdatesSettings(self):
        self.pageSetupData.GetPrintData().SetOrientation(wx.LANDSCAPE)
        self.printerSettings.updatePageSetupData(self.pageSetupData)
        self.assertEqual(wx.LANDSCAPE, 
                         self.settings.getint('printer', 'orientation'))

    def testMarginsInPageSetupDataAreUpdatedFromSettings(self):
        self.resetPrinterSettings()
        for margin in self.margins:
            self.settings.set('printer', 'margin_'+margin, 
                              str(self.margins[margin]))
        printerSettings = gui.printer.PrinterSettings(self.settings)
        self.assertEqual(wx.Point(2, 1), printerSettings.GetMarginTopLeft())
        self.assertEqual(wx.Point(4, 3), printerSettings.GetMarginBottomRight())
        
    def testPaperIdInPageSetupDataIsUpdatedFromSettings(self):
        self.resetPrinterSettings()
        self.settings.set('printer', 'paper_id', '1')
        printerSettings = gui.printer.PrinterSettings(self.settings)
        self.assertEqual(1, printerSettings.GetPaperId())

    def testOrientationInPageSetupDataIsUpdatedFromSettings(self):
        self.resetPrinterSettings()
        self.settings.set('printer', 'orientation', str(wx.LANDSCAPE))
        printerSettings = gui.printer.PrinterSettings(self.settings)
        self.assertEqual(wx.LANDSCAPE, printerSettings.GetOrientation())


class HTMLPrintoutTest(test.TestCase):
    def testCreate(self):
        gui.printer.HTMLPrintout('<html></html>', config.Settings(load=False))
        