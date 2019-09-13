'''
Created on Jun 12, 2017

@author: Heidi Hinkel
'''
import wx
from measurement.measures import Distance, Weight 
from patientData import PatientData

ID_BUTTON_CALC = wx.NewId()
ID_MENU_UNITS = wx.NewId()
ID_MENU_SAE = wx.NewId()
ID_MENU_METRIC = wx.NewId()
ID_RADIO_BUTTON_M = wx.NewId()
ID_RADIO_BUTTON_F = wx.NewId()

class Window(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, title = title, size = size)
        
        self.valuekg =  0
        self.valuecm = 0
        self.sexvalue = 'Male'
        self.patient = PatientData(self.valuecm, self.valuekg)
        
        self.InitMenuBar()
        self.InitMasterPanel()
        
        #Bindings
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChangeSex)
        
        self.Bind(wx.EVT_TEXT, self.OnTypeAge, self.ageValue)
        
        self.Bind(wx.EVT_TEXT, self.OnTypePlasmaCreat, self.plasmacreatvalue)
        
        self.Bind(wx.EVT_TEXT, self.OnTypeWeight, self.weightlb)
        self.Bind(wx.EVT_TEXT, self.OnTypeWeight, self.weightoz)
        
        self.Bind(wx.EVT_TEXT, self.OnTypeHeight, self.heightft)
        self.Bind(wx.EVT_TEXT, self.OnTypeHeight, self.heightin)
        
        self.Bind(wx.EVT_BUTTON, self.OnCalculate, id = ID_BUTTON_CALC)
        
        self.Center()
        self.Show()
        
    def InitMenuBar(self):
        
        #setting up file menu
        fileMenu = wx.Menu()
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "End Program")
        
        #setting up Help menu
        helpMenu = wx.Menu()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About", "About this program")
        
        #Creating Menu Bar
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        
        #Menu Bar Events
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
    
    def InitMasterPanel(self):
        self.masterPanel = wx.Panel(self)
        masterSizer = wx.BoxSizer(wx.VERTICAL)

        self.dataPanel()
        self.calcPanel()
        
        masterSizer.Add(self.panel, 0, wx.EXPAND | wx.ALL, 20, 20)
        masterSizer.Add(self.calcPanel, 1, wx.EXPAND | wx.ALL, 20, 20)
        self.masterPanel.SetSizer(masterSizer)
        
    def dataPanel(self):
        
        self.panel = wx.Panel(self.masterPanel, style = wx.BORDER_SUNKEN)
        self.panel.SetBackgroundColour('#ededed')
        dataSizer = wx.GridBagSizer(7, 6)
        
        row = 0
        self.sexRow(row, dataSizer)
        
        row = row + 1
        self.ageRow(row, dataSizer)
        
        row = row + 1
        self.serumCreatRow(row, dataSizer)
        
        row = row + 1
        self.weightRow(row, dataSizer)
        
        row = row + 1        
        self.heightRow(row, dataSizer)      
        
        self.panel.SetSizer(dataSizer)
        
    
    def calcPanel(self):
        self.calcPanel = wx.Panel(self.masterPanel, style = wx.BORDER_DOUBLE)
        self.calcPanel.SetBackgroundColour('#ededed')
        calcSizer = wx.GridBagSizer(7, 6)
        
        row = 0
        self.bmiRow(row, calcSizer)
        
        row = row + 1
        self.bsaRow(row, calcSizer)
        
        row = row + 1
        self.creatClearRow(row, calcSizer)
        
        row = row + 1
        self.creatClearModRow(row, calcSizer)
        
        row = row + 1
        self.calculateRow(row, calcSizer)
        
        self.calcButton.Disable()
        
        self.calcPanel.SetSizer(calcSizer)
        
        return row
        
    def sexRow(self, row, sizer):
        sizer.Add(wx.StaticText(self.panel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.panel, label = "Sex: "), pos = (row,1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(wx.RadioButton(self.panel, id = ID_RADIO_BUTTON_M, label = "Male", style = wx.RB_GROUP), pos = (row, 2))
        sizer.Add(wx.RadioButton(self.panel, id = ID_RADIO_BUTTON_F, label = "Female"), pos = (row, 3))
    
    def ageRow(self, row, sizer):
        self.ageValue = wx.TextCtrl(self.panel)
        
        sizer.Add(wx.StaticText(self.panel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.panel, label = "Age: "), pos = (row,1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.ageValue, pos = (row, 2))
        sizer.Add(wx.StaticText(self.panel, label = "years"), pos = (row, 3))
        
    def serumCreatRow(self, row, sizer):
        self.plasmacreatvalue = wx.TextCtrl(self.panel)
        
        sizer.Add(wx.StaticText(self.panel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.panel, label = "Serum Creatinine Level: "), pos = (row, 1))
        sizer.Add(self.plasmacreatvalue, pos = (row, 2))
        sizer.Add(wx.StaticText(self.panel, label = "mg/dl"), pos = (row, 3))
    
    def weightRow(self, row, sizer):
        self.weightlb = wx.TextCtrl(self.panel)
        self.weightoz = wx.TextCtrl(self.panel)
        self.weightConvert = wx.StaticText(self.panel)
        self.weightlb.SetValue('0.0')
        self.weightoz.SetValue('0.0')
        
        sizer.Add(wx.StaticText(self.panel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.panel, label = "Weight: "), pos = (row, 1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.weightlb, pos = (row, 2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(wx.StaticText(self.panel, label = 'lb'), pos = (row, 3))
        sizer.Add(self.weightoz, pos = (row, 4), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(wx.StaticText(self.panel, label = 'oz'), pos = (row, 5))
            
    def heightRow(self, row, sizer):
        self.heightft = wx.TextCtrl(self.panel)
        self.heightin = wx.TextCtrl(self.panel)
        self.heightConvert = wx.StaticText(self.panel)
        self.heightft.SetValue('0.0')
        self.heightin.SetValue('0.0')
        
        sizer.Add(wx.StaticText(self.panel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.panel, label = "Height: "), pos = (row, 1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.heightft, pos = (row, 2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(wx.StaticText(self.panel, label = 'ft'), pos = (row, 3))
        sizer.Add(self.heightin, pos = (row, 4), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(wx.StaticText(self.panel, label = 'in'), pos = (row, 5))
        
    def bmiRow(self, row, sizer):
        self.bmi = wx.StaticText(self.calcPanel)
        
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.calcPanel, label = "BMI: "), pos = (row, 1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.bmi, pos = (row, 2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 3))
        
    def bsaRow(self, row, sizer):
        self.bsa = wx.StaticText(self.calcPanel)
        
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.calcPanel, label = "BSA: "), pos = (row, 1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.bsa, pos = (row, 2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 3))
        
    def creatClearRow(self, row, sizer):
        self.creatclear = wx.StaticText(self.calcPanel)
        
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.calcPanel, label = "Creatinine Clearance: "), pos = (row, 1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.creatclear, pos = (row, 2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 3))
        
    def creatClearModRow(self, row, sizer):
        self.creatclearmod = wx.StaticText(self.calcPanel)
        
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.calcPanel, label = "Creatinine Clearance (Mod): "), pos = (row, 1), flag = wx.ALIGN_CENTER_VERTICAL, border = 10)
        sizer.Add(self.creatclearmod, pos = (row, 2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 3))
           
    
    def calculateRow(self, row, sizer):
        self.calcButton = wx.Button(self.calcPanel, ID_BUTTON_CALC, label = "Calculate")
        
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 0))
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 1))
        sizer.Add(wx.StaticText(self.calcPanel), pos = (row, 2))
        sizer.Add(self.calcButton, pos = (row, 3), flag = wx.ALIGN_LEFT, border = 5)
                       
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, " A Body Value Calculator \n in wxPython", "About ONC Calculator", wx.OK)
        dlg.ShowModal()
        dlg.Destroy() 
        
    def OnExit(self, event):
        self.Close(True)
        
    def OnChangeSex(self, event):
        radioButton = event.GetEventObject()
        self.sexvalue = radioButton.GetLabel()
        self.patient.setSex(self.sexvalue) 
        
    def OnTypeAge(self, event):
        self.patient.setAge(self.ageValue.GetValue())
        
    def OnTypePlasmaCreat(self, event):
        self.patient.setPlasmaCreatinine(self.plasmacreatvalue.GetValue())
    
    def OnTypeWeight(self, event):
        valuelb = self.weightlb.GetValue()
        valueoz = self.weightoz.GetValue()
        self.valuekg = float((Weight(lb = valuelb) + Weight(oz = valueoz)).kg)
    
    def OnTypeHeight(self, event):
        valueft = self.heightft.GetValue()
        valuein = self.heightin.GetValue()
        self.valuecm = float((Distance(ft = valueft) + Distance(inch = valuein)).cm)
        self.calcButton.Enable()
    
    def OnCalculate(self, event):
        self.patient.setWeight(self.valuekg)
        self.patient.setHeight(self.valuecm)
        self.bmi.SetLabel(str(round(self.patient.determineBMI(),4)) + " kg/m2")
        self.bsa.SetLabel(str(round(self.patient.determineBSA(),4)) + " m2")
        self.creatclear.SetLabel(str(round(self.patient.determineCrclCockroftGault(),4)) + " ml/min")
        self.creatclearmod.SetLabel(str(round(self.patient.determineCrClCockroftGaultMod(),4)) + " ml/min")
    
            
app = wx.App(False)
mainWindow = Window(None, "ONC Body Value Calculator", (600, 400))
app.MainLoop() 