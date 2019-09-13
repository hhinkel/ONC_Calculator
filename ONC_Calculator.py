'''
Created on May 5, 2017

@author: Heidi Hinkel
'''
import wx
# import re
import math
from measurement.measures import Distance, Weight

ID_BUTTON_CALC = wx.NewId()
ID_MENU_UNITS = wx.NewId()
ID_MENU_SAE = wx.NewId()
ID_MENU_METRIC = wx.NewId()

class Window(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, title = title, size = size)
        
        self.weightLabel = "kg"
        self.heightLabel = "cm"
        
        self.InitMenuBar()
        self.InitPanel()
        
        self.Center()
        self.Show()
   
    def InitMenuBar(self):
        
        #setting up file menu
        fileMenu = wx.Menu()
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "End Program")
        
        #setting up Preferences Menu
        prefsMenu = wx.Menu()
         
        #setting up units menu
        unitsMenu = wx.Menu()
        self.menuSAE = unitsMenu.Append(wx.ID_ANY, "SAE(Imperial) Units", kind = wx.ITEM_RADIO)
        self.menuMetric = unitsMenu.Append(wx.ID_ANY, "Metric Units", kind = wx.ITEM_RADIO)
        
        unitsMenu.Check(self.menuMetric.GetId(), True)
        
        menuUnits = prefsMenu.AppendMenu(wx.ID_ANY, "&Units", unitsMenu)
        
        self.Bind(wx.EVT_MENU, self.SelectSAE, self.menuSAE)
        self.Bind(wx.EVT_MENU, self.SelectMetric, self.menuMetric)
        
        #setting up Help menu
        helpMenu = wx.Menu()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About", "About this program")
        
        #Creating Menu Bar
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(prefsMenu, "&Preferences")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        
        #Menu Bar Events
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
    
    def InitPanel(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(15, 15)
        
        self.firstRow(panel, sizer)
        self.Bind(wx.EVT_TEXT, self.OnTypeWeight, self.weight)
        
        self.secondRow(panel, sizer)      
        self.Bind(wx.EVT_TEXT, self.OnTypeHeight, self.height)
        
        self.thirdRow(panel, sizer)
        
        self.fourthRow(panel, sizer)
        
        self.calcButton.Disable()
        
        self.Bind(wx.EVT_BUTTON, self.OnCalculate, id = ID_BUTTON_CALC)
        
        sizer.AddGrowableCol(2)
        sizer.AddGrowableRow(3)
        panel.SetSizer(sizer)
    
    def firstRow(self, panel, sizer):
        #First Row
        self.weight = wx.TextCtrl(panel)
        self.weightUnitsText = wx.StaticText(panel, label = self.weightLabel)
        self.weightConvert = wx.StaticText(panel)
        
        sizer.Add(wx.StaticText(panel), pos = (0, 0))
        sizer.Add(wx.StaticText(panel, label = "Weight: "), pos = (0, 1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.weight, pos = (0, 2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.weightUnitsText, pos = (0, 3), flag = wx.ALIGN_LEFT)
        sizer.Add(self.weightConvert, pos = (0, 4))
        sizer.Add(wx.StaticText(panel, label = "lbs"), pos = (0,5))
        sizer.Add(wx.StaticText(panel), pos = (0, 6))
    
    def secondRow(self, panel, sizer):
        self.height = wx.TextCtrl(panel)
        self.heightUnitsText = wx.StaticText(panel, label = self.heightLabel)
        self.heightConvert = wx.StaticText(panel)
        
        sizer.Add(wx.StaticText(panel), pos = (1, 0))
        sizer.Add(wx.StaticText(panel, label = "Height: "), pos = (1, 1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.height, pos = (1, 2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.heightUnitsText, pos = (1, 3))
        sizer.Add(self.heightConvert, pos =(1,4))
        sizer.Add(wx.StaticText(panel, label = "inches"), pos = (1,5))
        sizer.Add(wx.StaticText(panel), pos = (1, 6))
        
    def thirdRow(self, panel, sizer):
        self.bmi = wx.StaticText(panel)
        
        sizer.Add(wx.StaticText(panel), pos = (2, 0))
        sizer.Add(wx.StaticText(panel, label = "BMI: "), pos = (2, 1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.bmi, pos = (2, 2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer.Add(wx.StaticText(panel, label = "kg/m2"), pos = (2, 3), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer.Add(wx.StaticText(panel), pos = (2, 4))
        sizer.Add(wx.StaticText(panel), pos = (2, 5))
        sizer.Add(wx.StaticText(panel), pos = (2, 6))
        
    def fourthRow(self, panel, sizer):
        self.calcButton = wx.Button(panel, ID_BUTTON_CALC, label = "Calculate")
        
        sizer.Add(wx.StaticText(panel), pos = (3, 0))
        sizer.Add(wx.StaticText(panel), pos = (3, 1))
        sizer.Add(wx.StaticText(panel), pos = (3, 2))
        sizer.Add(self.calcButton, pos = (3, 3), flag = wx.ALIGN_LEFT, border = 5)
        sizer.Add(wx.StaticText(panel), pos = (3, 4))
        sizer.Add(wx.StaticText(panel), pos = (3, 5))
        sizer.Add(wx.StaticText(panel), pos = (3, 6))
                       
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, " A Body Value Calculator \n in wxPython", "About ONC Calculator", wx.OK)
        dlg.ShowModal()
        dlg.Destroy() 
        
    def SelectSAE(self, event):
        self.weightUnitsText.SetLabel('lbs ozs')
        self.heightUnitsText.SetLabel('ft in')
        if (len(self.weightValue) > 0):
            w = Weight(kg = self.weightValue)
            self.weightValue = w.lb
            self.weight.SetValue(str(self.weightValue))
            
        if(len(self.heightValue) > 0):
            h = Distance(cm = self.heightValue)
            self.heightValue = h.ft
            self.height.SetValue(str(self.heightValue))
        
    def SelectMetric(self, event):
        self.weightUnitsText.SetLabel('kg')
        self.heightUnitsText.SetLabel('cm')
        
    def OnExit(self, event):
        self.Close(True)
    
    def OnTypeWeight(self, event):
        value = self.weight.GetValue()
        weight = Weight(kg = value)
        
        self.weightConvert.SetLabel(str(round(weight.lb,4)))
        self.weightValue = value
          
    def OnTypeHeight(self, event):
        value = self.height.GetValue()
        height = Distance(cm = value)
        
        self.heightConvert.SetLabel(str(round(height.inch,4)))
        self.heightValue = value
        
        if(len(self.heightValue) > 0):
            self.calcButton.Enable()
        else:
            self.calcButton.Disable()
                        
    def OnCalculate(self, event):
        if self.menuSAE.IsChecked():
            # ConvertValues()
            event.Skip()
        else:
            self.bmiValue = float(self.weightValue) / (math.pow((float(self.heightValue)/100), 2))
            self.bmi.SetLabel(str(round(self.bmiValue,4)))        
            
    #def ConvertValues(self):
        
            
app = wx.App(False)
mainWindow = Window(None, "ONC Body Value Calculator", (400, 200))
app.MainLoop() 