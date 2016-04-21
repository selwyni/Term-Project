# -*- coding: utf-8 -*-

import numpy as np
import math
from mayavi import mlab
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, SceneEditor
from scipy.misc import derivative
###########################
# Pyside GUI 
###########################
import sys
from PySide import QtGui, QtCore

app = QtGui.QApplication.instance()

    
class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.setGeometry(200, 200, 600, 200)
        self.setWindowTitle('Material Science Utilities')
        self.setWindowIcon(QtGui.QIcon('exit.png'))
        self.createMenuBar()
        self.setCentralWidget(Opening())
        self.show()
        
    def createMenuBar(self):
        #Wrapper for MenuBar
        self.statusBar()
        menubar = self.menuBar()
        self.createFileMenu(menubar)
        self.createCalcMenu(menubar)
        self.createModelMenu(menubar)
        self.createMiscMenu(menubar)
        
    def createFileMenu(self, menubar):
        #Save, Exit
        fileMenu= menubar.addMenu('&File')
        
        saveAction = QtGui.QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip("Save Current Window's Data")
        #saveAction.triggered.connect()
        
        mainAction = QtGui.QAction('Main Menu', self)
        mainAction.setShortcut('Ctrl+M')
        mainAction.setStatusTip('Return to the Main Menu')
        mainAction.triggered.connect(lambda: self.setWidget(Opening()))
        
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(lambda: QtGui.qApp.closeAllWindows())
        
        fileMenu.addAction(saveAction)
        fileMenu.addAction(mainAction)
        fileMenu.addAction(exitAction)
        
    def createCalcMenu(self, menubar):
        #Stress/Strain Calculator, Theoretical Density
        calcMenu = menubar.addMenu('&Calculators')
        
        ssCalcAct = QtGui.QAction('&Stress and Strain Calculator', self)
        ssCalcAct.setShortcut('Ctrl+1')
        ssCalcAct.triggered.connect(lambda: self.setWidget(SSCalc()))
            
        diffCalcAct = QtGui.QAction('Diffusion Calculator', self)
        diffCalcAct.setShortcut('Ctrl+2')
        diffCalcAct.triggered.connect(lambda: self.setWidget(DiffCalc()))
        
        TheoCalcAct = QtGui.QAction('Theoretical Density Calculator', self)
        TheoCalcAct.setShortcut('Ctrl+3')
        TheoCalcAct.triggered.connect(lambda: self.setWidget(TheoDenCalc()))
                                                
        calcMenu.addAction(ssCalcAct)
        calcMenu.addAction(diffCalcAct)
        calcMenu.addAction(TheoCalcAct)
        #ssCalc.triggered.connect()
        
        
    def createModelMenu(self, menubar):
        modelMenu = menubar.addMenu('&Modeling')
        
        mayaviModelAct = QtGui.QAction('Crystal Structure Modeling', self)
        mayaviModelAct.setShortcut('Ctrl+4')
        mayaviModelAct.triggered.connect(lambda: self.setWidget(MayaviModel()))

        modelMenu.addAction(mayaviModelAct)
        
    def createMiscMenu(self, menubar):
        miscMenu = menubar.addMenu('&Miscellaneous')
        
        unitConvAct = QtGui.QAction('Unit Conversions', self)
        unitConvAct.setShortcut('Ctrl+5')
        unitConvAct.triggered.connect(lambda: self.setWidget(UnitConv()))
        miscMenu.addAction(unitConvAct)
    
    def setWidget(self, window=None):
        win = window
        self.setCentralWidget(win)

class Opening(QtGui.QWidget):
    def __init__(self):
        super(Opening, self).__init__()
        self.initUI()

        
    def initUI(self):
        #Buttons
        ssCalcBtn = QtGui.QPushButton("Stress and Strain \n Calculator")
        ssCalcBtn.setStatusTip("Calculate different types of stress and strain")
        ssCalcBtn.clicked.connect(lambda: self.parent().setWidget(SSCalc()))
        
        ssModelingBtn = QtGui.QPushButton('Crystal Structure\n Modeling')
        modelString = "Model basic one or two element crystal structures"
        ssModelingBtn.setStatusTip(modelString)
        ssModelingBtn.clicked.connect(
        lambda: self.parent().setWidget(MayaviModel()))

        diffCalcBtn = QtGui.QPushButton('Diffusion Calculator')
        diffString = "Calculate diffusion rates based on Fick's Laws"
        diffCalcBtn.setStatusTip(diffString)
        diffCalcBtn.clicked.connect(
        lambda: self.parent().setWidget(DiffCalc()))
        
        unitConvBtn = QtGui.QPushButton('Unit Conversions')
        unitConvString = "Convert mass, length, angles, pressure, and volume"
        unitConvBtn.setStatusTip(unitConvString)
        unitConvBtn.clicked.connect(
        lambda: self.parent().setWidget(UnitConv()))
        
        theoDensiBtn = QtGui.QPushButton('Theoretical Density Calculator')
        theoDensiString = "Calculate theoretical density of a structure"
        theoDensiBtn.setStatusTip(theoDensiString)
        theoDensiBtn.clicked.connect(
        lambda: self.parent().setWidget(TheoDenCalc()))
        
        #Labels
        CalcLbl = QtGui.QLabel('Calculators')
        CalcLbl.setAlignment(QtCore.Qt.AlignCenter)
        ModelLbl = QtGui.QLabel('Modeling')
        ModelLbl.setAlignment(QtCore.Qt.AlignCenter)
        MiscLbl = QtGui.QLabel('Miscellaneous')
        MiscLbl.setAlignment(QtCore.Qt.AlignCenter)
        
        grid = QtGui.QGridLayout()
            
        grid.setSpacing(5)  
        
        grid.addWidget(CalcLbl, 0, 0)
        grid.addWidget(ssCalcBtn, 1, 0)
        grid.addWidget(diffCalcBtn, 2, 0)
        grid.addWidget(theoDensiBtn, 3, 0)
        
        grid.addWidget(ModelLbl, 0, 1)
        grid.addWidget(ssModelingBtn, 1,1)
        
        grid.addWidget(MiscLbl, 2, 1)
        grid.addWidget(unitConvBtn, 3, 1)
        
        self.setLayout(grid) 
        self.show()   

class MayaviModel(QtGui.QWidget):
    def __init__(self):
        super(MayaviModel, self).__init__()
        self.initUI()
        
    def initUI(self):
        #Buttons
        calculateBtn = QtGui.QPushButton('Model')
        calculateBtn.clicked.connect(lambda: self.createPlotData())
        
        #Labels
        ionRadLbl = QtGui.QLabel('Ionic Radius')
        ALbl = QtGui.QLabel('Oxidation State')
        BLbl = QtGui.QLabel('PlaceHolder B')
        elemALbl = QtGui.QLabel('Element 1')
        elemALbl.setAlignment(QtCore.Qt.AlignCenter)
        elemBLbl = QtGui.QLabel('Element 2')
        elemBLbl.setAlignment(QtCore.Qt.AlignCenter)

        #TextEdits
        self.ionRadATextEdit = QtGui.QLineEdit()
        self.ionRadBTextEdit = QtGui.QLineEdit()
        self.elecChargeATextEdit = QtGui.QLineEdit()
        self.elecChargeBTextEdit = QtGui.QLineEdit()
        self.PlceHoldATextEdit = QtGui.QLineEdit()
        self.PlceHoldBTextEdit = QtGui.QLineEdit()
        
        #ComboBoxes
        ionRadABox = QtGui.QComboBox(self)
        ionRadBBox = QtGui.QComboBox(self)
        
        elecABox = QtGui.QComboBox(self)
        elecBBox = QtGui.QComboBox(self)
        
        placeCBox = QtGui.QComboBox(self)
        placeDBox = QtGui.QComboBox(self)
        
        ionRadABox.addItem('pm')
        ionRadABox.addItem('Angstroms')
        #ionRadABox.activated[str].connect(self.onActivated)
        ionRadBBox.addItem('pm')
        ionRadBBox.addItem('Angstroms')
        
        elecABox.addItem('+')
        elecABox.addItem('-')
        elecBBox.addItem('-')
        elecBBox.addItem('+')
        
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(5)
        
        grid.addWidget(elemALbl, 0, 1)
        grid.addWidget(elemBLbl, 0, 3)
        
        grid.addWidget(ionRadLbl, 2, 0)
        grid.addWidget(self.ionRadATextEdit, 2, 1)
        grid.addWidget(ionRadABox, 2,2)
        grid.addWidget(self.ionRadBTextEdit, 2, 3)
        grid.addWidget(ionRadBBox, 2,4)
        
        grid.addWidget(ALbl, 3, 0)
        grid.addWidget(self.elecChargeATextEdit, 3,1)
        grid.addWidget(elecABox, 3, 2)
        grid.addWidget(self.elecChargeBTextEdit, 3,3)
        grid.addWidget(elecBBox, 3, 4)
        
        grid.addWidget(BLbl, 4,0)
        grid.addWidget(self.PlceHoldATextEdit, 4,1)
        grid.addWidget(placeCBox, 4, 2)
        grid.addWidget(self.PlceHoldBTextEdit, 4,3)
        grid.addWidget(placeDBox, 4, 4)
        
        grid.addWidget(calculateBtn, 5,3, 1, 2)
        self.setLayout(grid)
        self.show()
        
    def onActivated(self,text):
        pass
        
    def createPlotData(self):
        ionRadAText = self.ionRadATextEdit.text()
        ionRadBText = self.ionRadBTextEdit.text()
        elecChargeAText = self.elecChargeATextEdit.text()
        elecChargeBText = self.elecChargeBTextEdit.text()
        #c = SimpleUnitCell()
        #plotSimple3D(c.red_x, c.red_y, c.red_z, c.white_x, c.white_y, c.white_z)
        
class DiffCalc(QtGui.QWidget):
    def __init__(self):
        super(DiffCalc, self).__init__()
        self.result = 0
        self.unit = 'mol / m^2 s'
        self.initUI()
        
    def initUI(self):
        #Buttons
        calcBtn = QtGui.QPushButton('Calculate')
        calcBtn.clicked.connect(lambda: self.calculateDiff())
        
        #Labels
        self.resultLbl = QtGui.QLabel('J = %d %s' %(self.result, self.unit))
        self.resultLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLbl.setFont(QtGui.QFont('Helvetica', 20))
        self.diffCoeffLbl = QtGui.QLabel('Diffusion Coefficient')
        self.concOneLbl = QtGui.QLabel('Concentration 1')
        self.concTwoLbl = QtGui.QLabel('Concentration 2')
        
        #TextEdits
        self.diffCoeff = QtGui.QLineEdit()
        self.concOne = QtGui.QLineEdit()
        self.concTwo = QtGui.QLineEdit()
        
        #ComboBoxes
        self.diffCoeffUnit = QtGui.QComboBox(self)
        self.concOneUnit = QtGui.QComboBox(self)
        self.concTwoUnit = QtGui.QComboBox(self)
        
        self.diffCoeffUnit.addItem('m^2 / 2')
        self.diffCoeffUnit.addItem('cm^2 / 2')
        
        self.concOneUnit.addItem('mol / m^3')
        self.concOneUnit.addItem('mol / mm^3')

        self.concTwoUnit.addItem('mol / m^3')
        self.concTwoUnit.addItem('mol / mm^3')
        
        #Grid
        grid = QtGui.QGridLayout()
        grid.setSpacing(5)
        
        grid.addWidget(self.diffCoeffLbl, 0,0)
        grid.addWidget(self.concOneLbl, 1, 0)
        grid.addWidget(self.concTwoLbl, 2, 0)
        grid.addWidget(self.resultLbl, 3, 0, 2, 0)
        
        grid.addWidget(self.diffCoeff, 0, 1)
        grid.addWidget(self.concOne, 1, 1)
        grid.addWidget(self.concTwo, 2, 1)
        
        grid.addWidget(self.diffCoeffUnit, 0, 2)
        grid.addWidget(self.concOneUnit, 1, 2)
        grid.addWidget(self.concTwoUnit, 2, 2)
        grid.addWidget(calcBtn, 3, 2)
        
        self.setLayout(grid)
        self.show()
        
    def calculateDiff(self):
        diffCoeff = self.diffCoeff.text()
        diffCoeffUnit = self.diffCoeffUnit.currentText()
        concOneVal = self.concOne.text()
        concTwoVal = self.concTwo.text()
        concOneUnit = self.concOneUnit.currentText()
        concTwoUnit = self.concTwoUnit.currentText()
    
class TheoDenCalc(QtGui.QWidget):
    def __init__(self):
        super(TheoDenCalc, self).__init__()
        self.val = 0
        self.unit = 'g/cm^3'
        self.initUI()
        
    def initUI(self):
        #Buttons
        calcBtn = QtGui.QPushButton('Calculate')
        calcBtn.clicked.connect(lambda: self.calculateDensity())
        
        oneElemBtn = QtGui.QCheckBox('Single Element', self)
        oneElemBtn.toggle()
        
        #TextEdits
        self.ionRadiiOne = QtGui.QLineEdit()
        self.ionRadiiTwo = QtGui.QLineEdit()
        self.atomWeightOne = QtGui.QLineEdit()
        self.atomWeightTwo = QtGui.QLineEdit()
        
        #ComboBoxes
        self.crysStruct = QtGui.QComboBox(self)
        self.lengthUnitOne = QtGui.QComboBox(self)
        self.lengthUnitTwo = QtGui.QComboBox(self)
        self.massOne = QtGui.QComboBox(self)
        self.massTwo = QtGui.QComboBox(self)
        
        self.crysStruct.addItem('Simple')
        self.crysStruct.addItem('FCC')
        self.crysStruct.addItem('BCC')
        self.crysStruct.addItem('Hexagonal')
        
        self.lengthUnitOne.addItem('Angstrom')
        self.lengthUnitOne.addItem('pm')
        self.lengthUnitOne.addItem('nm')
        
        self.lengthUnitTwo.addItem('Angstrom')
        self.lengthUnitTwo.addItem('pm')
        self.lengthUnitTwo.addItem('nm')
        
        self.massOne.addItem('g/mol')
        
        self.massTwo.addItem('g/mol')
        
        #Labels
        self.resultLbl = QtGui.QLabel('Density = %d %s' %(self.val, self.unit))
        self.resultLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLbl.setFont(QtGui.QFont('Helvetica', 20))
        self.elemOneLbl = QtGui.QLabel('Element One')
        self.elemTwoLbl = QtGui.QLabel('Element Two')
        
        #Grid
        grid = QtGui.QGridLayout()
        grid.setSpacing(5)
        
        grid.addWidget(self.elemOneLbl, 0, 1)
        grid.addWidget(self.elemTwoLbl, 0, 3)
        
        grid.addWidget(self.crysStruct, 1, 0)
        grid.addWidget(self.ionRadiiOne, 1, 1)
        grid.addWidget(self.ionRadiiTwo, 1, 3)
        grid.addWidget(self.lengthUnitOne, 1, 2)
        grid.addWidget(self.lengthUnitTwo, 1, 4)
        
        grid.addWidget(self.atomWeightOne, 2, 1)
        grid.addWidget(self.atomWeightTwo, 2, 3)
        grid.addWidget(self.massOne, 2, 2)
        grid.addWidget(self.massTwo, 2, 4)
        
        grid.addWidget(calcBtn, 3, 4)
        grid.addWidget(self.resultLbl, 3,1, 1, 3)
        grid.addWidget(oneElemBtn, 3, 0)
        
        self.setLayout(grid)
        self.show()
        
    def calculateDensity(self):
        pass
                        
class SSCalc(QtGui.QWidget):
    def __init__(self):
        super(SSCalc, self).__init__()
        self.stressVal = 0
        self.strainVal = 0
        self.modVal = 0
        self.stressUnit = 'Pa'
        self.modUnit = 'Pa'
        self.initUI()
        
    def initUI(self):
        #Buttons
        calcBtn = QtGui.QPushButton('Calculate')
        calcBtn.clicked.connect(lambda: self.calculateSS())
    
        #TextEdits
        self.force = QtGui.QLineEdit()
        self.area = QtGui.QLineEdit()
        self.initLength = QtGui.QLineEdit()
        self.finalLength = QtGui.QLineEdit()
        self.stressInput = QtGui.QLineEdit()
        self.strainInput = QtGui.QLineEdit()
        
        
        #ComboBoxes
        self.forceUnit = QtGui.QComboBox(self)
        self.areaUnit = QtGui.QComboBox(self)
        self.initLengthUnit = QtGui.QComboBox(self)
        self.finalLengthUnit = QtGui.QComboBox(self)
        
        self.stressUnitBox = QtGui.QComboBox(self)
        self.strainUnit = QtGui.QComboBox(self)
        
        self.forceUnit.addItem('Newton')
        
        self.areaUnit.addItem('m^2')
        self.areaUnit.addItem('cm^2')
        self.areaUnit.addItem('mm^2')
        self.areaUnit.addItem(u'\u00B5m^2')
        self.areaUnit.addItem('nm^2')
        
        self.initLengthUnit.addItem('m')
        self.initLengthUnit.addItem('cm')
        self.initLengthUnit.addItem('mm')
        self.initLengthUnit.addItem(u'\u00B5m')
        self.initLengthUnit.addItem('nm')
        
        self.finalLengthUnit.addItem('m')
        self.finalLengthUnit.addItem('cm')
        self.finalLengthUnit.addItem('mm')
        self.finalLengthUnit.addItem(u'\u00B5m')
        self.finalLengthUnit.addItem('nm')
        
        self.stressUnitBox.addItem('Pa')
        self.stressUnitBox.addItem('MPa')
        self.stressUnitBox.addItem('GPa')
        
        #Labels
        self.stressLbl = QtGui.QLabel('Stress = %d %s'
                    %(self.stressVal, self.stressUnit))
        self.stressLbl.setFont(QtGui.QFont('Helvetica', 16))
        
        self.strainLbl = QtGui.QLabel('Strain = %d' 
                    %(self.strainVal))
        self.strainLbl.setFont(QtGui.QFont('Helvetica', 16))
        self.strainLbl.setAlignment(QtCore.Qt.AlignCenter)
        
        self.modulusLbl = QtGui.QLabel("Young's Modulus = %d %s"
                    %(self.modVal, self.modUnit))
        self.modulusLbl.setFont(QtGui.QFont('Helvetica', 16))
        
        self.forceLbl = QtGui.QLabel('Force')
        self.areaLbl = QtGui.QLabel('Area')
        self.initLengthLbl = QtGui.QLabel('Initial Length')
        self.finalLengthLbl = QtGui.QLabel('Final Length')
        
        self.stressInputLbl = QtGui.QLabel('Stress')
        self.strainInputLbl = QtGui.QLabel('Strain')
        
        #Grid
        grid = QtGui.QGridLayout()
        grid.setSpacing(5)
        
        grid.addWidget(self.forceLbl, 0, 0)
        grid.addWidget(self.force, 0, 1)
        grid.addWidget(self.forceUnit, 0, 2)
        
        grid.addWidget(self.initLengthLbl, 0, 3)
        grid.addWidget(self.initLength, 0, 4)
        grid.addWidget(self.initLengthUnit, 0, 5)
        
        grid.addWidget(self.areaLbl, 1, 0)
        grid.addWidget(self.area, 1, 1)
        grid.addWidget(self.areaUnit, 1, 2)
        
        grid.addWidget(self.finalLengthLbl, 1, 3)
        grid.addWidget(self.finalLength, 1, 4)
        grid.addWidget(self.finalLengthUnit, 1, 5)
        
        grid.addWidget(self.stressInputLbl, 2, 0)
        grid.addWidget(self.stressInput, 2, 1)
        grid.addWidget(self.stressUnitBox, 2, 2)
        grid.addWidget(self.strainInputLbl, 2, 3)
        grid.addWidget(self.strainInput, 2, 4)
        grid.addWidget(self.strainUnit, 2, 5)
        
        grid.addWidget(self.stressLbl, 3, 0, 1, 1)
        grid.addWidget(self.strainLbl, 3, 1, 1, 2)
        grid.addWidget(self.modulusLbl, 3, 3, 1, 2)
        grid.addWidget(calcBtn, 3, 5)
        
        self.setLayout(grid)
        self.show()
        
    def calculateSS(self):
        pass        
        
class UnitConv(QtGui.QWidget):
    def __init__(self):
        super(UnitConv,self).__init__()
        self.unit='Pa'
        self.val = 0
        self.initUI()

    def initUI(self):
        #Buttons
        calcBtn = QtGui.QPushButton('Calculate')
        calcBtn.clicked.connect(lambda: self.calculateUnits())
        calcBtn.setAutoDefault(True)
                
        #TextEdits
        self.valOne = QtGui.QLineEdit()

        #Labels
        self.resultLbl = QtGui.QLabel('%d %s' %(self.val, self.unit))
        self.resultLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLbl.setFont(QtGui.QFont('Helvetica',20))
        
        #ComboBoxes
        self.propertyBox = QtGui.QComboBox(self)
        self.unitOne = QtGui.QComboBox(self)
        self.unitTwo = QtGui.QComboBox(self)
                
        self.propertyBox.addItem('Pressure')
        self.propertyBox.addItem('Length')
        self.propertyBox.addItem('Mass')
        self.propertyBox.addItem('Temperature')
        self.propertyBox.activated.connect(lambda: self.changeUnits())
        self.propertyBox.activated.connect(lambda: self.updateLabel())
        self.changeUnits()
        
        self.unitTwo.activated.connect(lambda: self.updateLabel())

        #Grid
        grid = QtGui.QGridLayout()
        grid.setSpacing(5)
        
        grid.addWidget(self.propertyBox, 0, 0, 1, 1)
        grid.addWidget(self.valOne, 1,0)
        grid.addWidget(self.unitOne,1,1, 1,2)
        grid.addWidget(self.unitTwo,2,1,1,2)
        grid.addWidget(self.resultLbl, 3,0, 1,2)
        grid.addWidget(calcBtn, 3,1, 1, 2)
        
        self.setLayout(grid)
        self.show()
    
    def updateLabel(self):
        self.unit = self.unitTwo.currentText()
        self.resultLbl.setText('%6f %s' %(self.val, self.unit))
    
    def changeUnits(self):
        self.unitOne.clear()
        self.unitTwo.clear()
        self.pressureUnits = ['Pa', 'MPa', 'GPa', 'atm', 'torr', 'mmHg', 'psi']
        self.lengthUnits = ['m','cm','mm', 'ft', u'\u00B5m', 'nm', 'Angstroms']
        self.massUnits = ['g','kg','mg', u'\u00B5g','ng','amu','lbs']
        self.tempUnits = [u'\u00B0T', u'\u00B0C', 'K']
        if (self.propertyBox.currentText() == 'Pressure'):
            for elem in self.pressureUnits:
                self.unitOne.addItem(elem)
                self.unitTwo.addItem(elem)          
        elif (self.propertyBox.currentText() == 'Length'):
            for elem in self.lengthUnits:
                self.unitOne.addItem(elem)
                self.unitTwo.addItem(elem)
        elif (self.propertyBox.currentText() == 'Mass'):
            for elem in self.massUnits:
                self.unitOne.addItem(elem)
                self.unitTwo.addItem(elem)
        elif (self.propertyBox.currentText() == 'Temperature'):
            for elem in self.tempUnits:
                self.unitOne.addItem(elem)
                self.unitTwo.addItem(elem)
            
    def calculateUnits(self):
        if (self.propertyBox.currentText() == 'Pressure'):
            return self.convertPressure()
        elif (self.propertyBox.currentText() == 'Length'):
            return self.convertLength()
        elif (self.propertyBox.currentText() == 'Mass'):
            return self.convertMass()
        elif (self.propertyBox.currentText() == 'Temperature'):
            return self.convertTemp()
            
    def convertPressure(self):
        givenUnit = self.unitOne.currentText()
        goalUnit = self.unitTwo.currentText()
            
        try:    
            givenVal = float(self.valOne.text())
        except:
            pass
        torrToPa = long(101325/760)
        PaToTorr = long(760/101325)
        PaToAtm = long(1/101325)
        toPaIndex = self.pressureUnits.index(givenUnit)
        fromPaIndex = self.pressureUnits.index(goalUnit)
        scaleToPa = [1, 10**6, 10**9, 101325, torrToPa, 1, 1.933*10**-2]
        scaleFromPa = [1, 10**-6, 10**-9, PaToAtm,  PaToTorr, 1,
                                1/(1.933*10**-2)]
        print(1/101325)
        print(toPaIndex, fromPaIndex)
        print(givenVal, scaleToPa[toPaIndex], scaleFromPa[fromPaIndex])
        self.val = givenVal * scaleToPa[toPaIndex] * scaleFromPa[fromPaIndex]
        self.updateLabel()

    def convertMass(self):
        givenUnit = self.unitOne.currentText()
        goalUnit = self.unitTwo.currentText()
        
        try:    
            givenVal = float(self.valOne.text())
        except:
            pass
        toKgIndex = self.massUnits.index(givenUnit)
        fromKgIndex = self.massUnits.index(goalUnit)
        scaleToKg = [10**-3, 1, 10**-6, 10**-9, 10**-12, 1.660539040*10**-27,
                        0.453592]
        scaleFromKg = [10**3, 1, 10**6, 10**9, 10**12, (1/1.660539040)*10**27,
                        2.20462]
        print(1/(1.6605*10**-27))
        self.val = givenVal * scaleToKg[toKgIndex] * scaleFromKg[fromKgIndex]
        self.updateLabel()
        
    def convertLength(self):
        givenUnit = self.unitOne.currentText()
        goalUnit = self.unitTwo.currentText()
        try: 
            givenVal = float(self.valOne.text())
        except: 
            pass
        toMIndex = self.lengthUnits.index(givenUnit)
        fromMIndex = self.lengthUnits.index(goalUnit)
        self.lengthUnits = ['m','cm','mm', 'ft', u'\u00B5m', 'nm', 'Angstroms']

        scaleToM = [1, 10**-2, 10**-3, 0.3048, 10**-6, 10**-9, 10**-10]
        scaleFromM = [1, 10**2, 10**3, 3.28084, 10**6, 10**9, 10**10]
        
        if (givenUnit == goalUnit):
            self.val = givenVal
        else:
            self.val = givenVal * scaleToM[toMIndex] * scaleFromM[fromMIndex]
        self.updateLabel()
        
        
    def convertTemp(self):
        givenUnit = self.unitOne.currentText()
        goalUnit = self.unitTwo.currentText()
        try: givenVal = float(self.valOne.text())
        except: pass
        if (givenUnit == goalUnit):
            self.val = givenVal
        elif (givenUnit == u'\u00B0T'):
            if (goalUnit == u'\u00B0C'):
                self.val = (givenVal - 32)*5.0 / 9.0
            elif (goalUnit == 'K'):
                self.val = (givenVal + 459.67)*5.0/9.0
        elif (givenUnit == u'\u00B0C'):
            if (goalUnit == u'\u00B0T'):
                self.val = givenVal*9.0/5.0 + 32
            elif (goalUnit == 'K'):
                self.val = givenVal + 273.15
        elif (givenUnit == 'K'):
            if (goalUnit == u'\u00B0T'):
                self.val = givenVal*9.0/5.0 - 459.67
            elif (goalUnit == u'\u00B0C'):
                self.val = givenVal - 273.15
        self.updateLabel()

    
###########################
# Crystal plot3d (Tubes)
###########################

###########################
# Plotting Function
###########################


#Repurposed Mayavi Sample plot (Modified inputs and scale)
def plotSimple3D(red_x, red_y, red_z, white_x, white_y, white_z):
    mlab.figure(1, bgcolor=(0.0,0.0,0.0), size=(600, 600))
    mlab.clf()
    # The position of the atoms    
    mlab.points3d(red_x, red_y, red_z, scale_factor=1,
                resolution=20,
                color=(1, 0, 0),
                scale_mode='none')
    mlab.points3d(white_x, white_y, white_z, scale_factor=1.25,
                resolution=20,
                color=(1, 1, 1),
                scale_mode='none')
    mlab.view()
    mlab.show()
    
#Self-written specifically for one certain crystal structure.
def plotBodyCenteredCubic(red_x, red_y, red_z, white_x, white_y, white_z):
    mlab.figure(1, bgcolor=(0.0, 0.0, 0.0), size = (600, 600))
    mlab.clf()
    
    mlab.points3d(red_x, red_y, red_z, scale_factor = 0.5,
                    resolution = 20,
                    color = (1, 1, 1),
                    scale_mode='none')
    mlab.points3d(white_x, white_y, white_z, scale_factor = 1,
                    resolution = 20,
                    color = (1,0,0),
                    scale_mode='none')
    mlab.view()
    mlab.show()

def plotFCC(one_x, one_y, one_z, two_x, two_y, two_z):
    mlab.figure(1, bgcolor=(0.0, 0.0, 0.0), size = (600, 600))
    mlab.clf()
                    
    mlab.points3d(one_x, one_y, one_z, scale_factor =0.2,
                    resolution = 20,
                    color = (1, 1, 1),
                    scale_mode='none')
                
    mlab.points3d(two_x, two_y, two_z, scale_factor = 0.2,
                    resolution = 20,
                    color = (1, 0, 0),
                    scale_mode='none')
                    
    mlab.view()
    mlab.show()

def plot3D(coords):
    mlab.figure(1, bgcolor=(0.0, 0.0, 0.0), size = (600, 600))
    mlab.clf()
                    
    mlab.points3d(coords[0], coords[1], coords[2], scale_factor = 0.2,
                    resolution = 20,
                    color = (1, 1, 1),
                    scale_mode='none')
                
    mlab.points3d(coords[3], coords[4], coords[5], scale_factor = 0.2,
                    resolution = 20,
                    color = (1, 0, 0),
                    scale_mode='none')
                    
    mlab.view()
    mlab.show()
##########################################
# CrystalStructure Helpers
##########################################

def CCPTupleList(UnitCell, n=4, xFactor=1, yFactor=1, zFactor=1):
    (one_x, one_y, one_z) = ([], [], [])
    (two_x, two_y, two_z) = ([], [], [])
    (oneX, oneY, oneZ) = (UnitCell[0], UnitCell[1], UnitCell[2])
    (twoX, twoY, twoZ) = (UnitCell[3], UnitCell[4], UnitCell[5])
    for zOffsetInt in range(n):
        zOffset = zOffsetInt*zFactor
        for yOffsetInt in range(n):
            yOffset = yOffset*yFactor
            for xOffsetInt in range(n):
                xOffset = xOffset*xFactor
                for elem in oneX:
                    one_x.append(elem + xOffset)
                for elem in oneY:
                    one_y.append(elem + yOffset)
                for elem in oneZ:
                    one_z.append(elem + zOffset)
                for elem in twoX:
                    two_x.append(elem + xOffset)
                for elem in twoY:
                    two_y.append(elem + yOffset)
                for elem in twoZ:
                    two_z.append(elem + zOffset) 
    return [one_x, one_y, one_z, two_x, two_y, two_z]
    
def HCPTupleList(UnitCell, n=4, xFactor=0.5, yFactor=(3**0.5 /2), zFactor=1):
    (one_x, one_y, one_z) = ([], [], [])
    (two_x, two_y, two_z) = ([], [], [])
    (oneX, oneY, oneZ) = (UnitCell[0], UnitCell[1], UnitCell[2])
    (twoX, twoY, twoZ) = (UnitCell[3], UnitCell[4], UnitCell[5])
    for zOffsetInt in range(n):
        zOffset = zOffsetInt*zFactor
        for yOffsetInt in range(n):
            yOffset = yOffsetInt*yFactor
            for xOffsetInt in range(n):
                xOffset = xOffsetInt + yOffsetInt*xFactor
                for elem in oneX:
                    one_x.append(elem + xOffset)
                for elem in oneY:
                    one_y.append(elem + yOffset)
                for elem in oneZ:
                    one_z.append(elem + zOffset)
                for elem in twoX:
                    two_x.append(elem + xOffset)
                for elem in twoY:
                    two_y.append(elem + yOffset)
                for elem in twoZ:
                    two_z.append(elem + zOffset) 
    return [one_x, one_y, one_z, two_x, two_y, two_z]
    

def removeRepeats(Cells):
    (oneX, oneY, oneZ) = (Cells[0], Cells[1], Cells[2])
    (twoX, twoY, twoZ) = (Cells[3], Cells[4], Cells[5])
    oneTupleList = []
    twoTupleList = []
    for index in range(len(oneX)):
        point = (oneX[index], oneY[index], oneZ[index])
        if point in oneTupleList:
            continue
        else:
            oneTupleList.append(point)
    for index in range(len(twoX)):
        point = (twoX[index], twoY[index],twoZ[index])
        if point in twoTupleList:
            continue
        else:
            twoTupleList.append(point) 
    return [oneTupleList, twoTupleList]
    
def createCoordinates(TupleLists):
    (one_x, one_y, one_z) = ([],[],[])
    (two_x, two_y, two_z) = ([],[],[])
    for elem in TupleLists[0]:
        one_x.append(elem[0])
        one_y.append(elem[1])
        one_z.append(elem[2])
    for elem in TupleLists[1]:
        two_x.append(elem[0])
        two_y.append(elem[1])
        two_z.append(elem[2])
    return [one_x, one_y, one_z, two_x, two_y, two_z]
    
##########################################
# Single Element Crystal Structures
##########################################   

class SCC(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.TupleList = CCPTupleList(self.UnitCell)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):
        self.one_xUnit = [0]*4 + [1]*4
        self.one_yUnit = ([0]*2 + [1]*2)*2
        self.one_zUnit = [0,1]*4
        
        self.two_xUnit = []
        self.two_yUnit = []
        self.two_zUnit = []
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]
    
        
class BCC(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.TupleList = CCPTupleList(self.UnitCell)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):
        self.one_xUnit = [0]*4 + [0.5] + [1]*4
        self.one_yUnit = [0]*2 + [1]*2 + [0.5] + [0]*2 + [1]*2
        self.one_zUnit = [0,1]*2 + [0.5] + [0,1]*2

        self.two_xUnit = []
        self.two_yUnit = []
        self.two_zUnit = []
        
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit,
                            self.two_xUnit, self.two_yUnit, self.two_zUnit]

class FCC(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.TupleList = CCPTupleList(self.UnitCell)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):
        #Create the basic unit coordinates to the FCC crystal
        self.one_xUnit = [0]*4 + [1]*4
        self.one_yUnit = [0]*2 + [1]*2 + [0]*2 + [1]*2
        self.one_zUnit = [0,1]*4
        self.two_xUnit = [0] + [0.5]*4 + [1]
        self.two_yUnit = [0.5]*2 + [0] + [1] + [0.5]*2
        self.two_zUnit = [0.5] + [0] + [0.5]*2 + [1] + [0.5]
        
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit,
                            self.two_xUnit, self.two_yUnit, self.two_zUnit]
        
class HCP(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.TupleList = HCPTupleList(self.UnitCell, 1)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):
        r3 = 3**0.5 * 0.5
        
        #Top and Bottom Layers
        self.one_xUnit = ([0] + [0.5]*2 + [1] + [1.5]*2 + [2])*2
        self.one_yUnit = (([r3] + [0] + [r3*2])*2 + [r3])*2
        self.one_zUnit = [0]*7 + [(2* 2**0.5)/(3**0.5)]*7
        #Middle Layer
        self.two_xUnit = [0.5] + [1] + [1.5]
        self.two_yUnit = [r3*2/3] + [r3 + r3*2/3] + [r3*2/3]
        self.two_zUnit = [2**0.5 / 3**0.5]*3

        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit,
                            self.two_xUnit, self.two_yUnit, self.two_zUnit]
        
        
##########################################
# AB Crystal Structures
########################################## 

class NaCl(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.r3 = 3**0.5 / 3
        self.createUnitCell()
        self.TupleList = CCPTupleList(self.UnitCell)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):
        self.one_xUnit = [0]*5 + [0.5]*4 + [1]*5
        self.one_yUnit = [0,0,0.5,1,1] + [0, 0.5, 0.5, 1] + [0,0,0.5,1,1]
        self.one_zUnit = [0,1,0.5,0,1] + [0.5,0,1,0.5] + [0,1,0.5,0,1]
        
        self.two_xUnit = [0]*4 + [0.5]*5 + [1]*4
        self.two_yUnit = [0,0.5,0.5,1] + [0,0,0.5,1,1] + [0,0.5,0.5,1]
        self.two_zUnit = [0.5,0,1,0.5] + [0,1,0.5,0,1] + [0.5,0,1,0.5]
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]
                    
class NiAs(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.r3 = 3**0.5 / 3
        self.createUnitCell()
        self.TupleList = HCPTupleList(self.UnitCell, 1)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):        
        self.one_xUnit = [0]*3 + [0.5]*3 + [1]*3 + [1.5]*3
        self.one_yUnit = [0]*3 + [0.5*3**0.5]*3 + [0]*3 + [0.5*3**0.5]*3
        self.one_zUnit = [0, 0.5, 1]*4

        self.two_xUnit = [0.5, 1]
        self.two_yUnit = [self.r3/2] + [self.r3]
        self.two_zUnit = [0.25] + [0.75]
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]

                
class ZincBlende(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.TupleList = CCPTupleList(self.UnitCell)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):
        self.one_xUnit = [0]*5 + [0.5]*4 + [1]*5
        self.one_yUnit = [0,0,0.5,1,1] + [0,0.5,0.5,1] + [0,0,0.5,1,1]
        self.one_zUnit = [0,1,0.5,0,1] + [0.5,0,1,0.5] + [0,1,0.5,0,1]
        
        self.two_xUnit = [0.25]*2 + [0.75]*2
        self.two_yUnit = [0.25, 0.75]*2
        self.two_zUnit = [0.75] + [0.25]*2 + [0.75]
    
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]
                    
   
class Wurtzite(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.r3 = 3**0.5
        self.createUnitCell()
        self.TupleList = HCPTupleList(self.UnitCell)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
                
    def createUnitCell(self):
        self.one_xUnit = [0]*2 + [0.5]*3 + [1]*2 + [1.5]*2
        self.one_yUnit = [0]*2 + [self.r3/6] + \
                        [self.r3/2]*2 + [0]*2 + [self.r3/2]*2
        self.one_zUnit = [0,1] + [0.5, 0, 1] + [0,1]*2
        
        self.two_xUnit = [0, 0.5, 0.5, 1, 1.5]
        self.two_yUnit = [0, self.r3/6, self.r3/2, 0, self.r3/2]
        self.two_zUnit = [0.675, 0.125] + [0.675]*3
        
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]
      
                                    
##########################################
# AB2 Crystal Structure
########################################## 

class Fluorite(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.TupleList = CCPTupleList(self.UnitCell)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):
        self.one_xUnit = [0]*5 + [0.5]*4 + [1]*5
        self.one_yUnit = [0,0,0.5,1,1] + [0,0.5,0.5,1] + [0,0,0.5,1,1]
        self.one_zUnit = [0, 1, 0.5, 0, 1] + \
                            [0.5, 0, 1, 0.5] + [0, 1, 0.5, 0, 1]
    
        self.two_xUnit = [0.25]*4 + [0.75]*4
        self.two_yUnit = [0.25]*2 + [0.75]*2 + [0.25]*2 + [0.75]*2
        self.two_zUnit = [0.25, 0.75]*4
        
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]
              
##########################################
# AB3 Crystal Structure
########################################## 

class YCl3(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.s69 = math.sin(math.radians(69))
        self.c69 = math.cos(math.radians(69))
        self.createUnitCell()
        self.TupleList = HCPTupleList(self.UnitCell, 1, self.c69,self.s69)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
                
    def createUnitCell(self):
        self.one_xUnit = [0]*2 + [self.c69]*2 + [0.5]*2 + [0.5+self.c69]*2 + \
                            [1]*2 + [1+self.c69]*2
        self.one_yUnit = ([0]*2 + [1]*2)*3
        self.one_zUnit = [1.0/3.0, 5.0/3.0]*2 + [2.0/3.0, 4.0/3.0]*2 + \
                            [1.0/3.0, 5.0/3.0]*2
        
        self.two_xUnit = []
        self.two_yUnit = []
        self.two_zUnit = []
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]
        
c = YCl3()
        
class BiI3(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.createTuplePointList()
        self.removeRepeats()
        self.createCoords()
                
    def createUnitCell(self):
        pass
            
##########################################
# A2B Crystal Structure
########################################## 
class CdI2(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.TupleList = HCPTupleList(self.UnitCell, 1)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):
        self.one_xUnit = []
        self.one_yUnit = [0]*2 + [1]*2 + [0.5] + [0]*2 + [1]*2
        self.one_zUnit = [0,1]*2 + [0.5] + [0,1]*2
        
        self.two_xUnit = [0.25] + [0.3]*2 + [0.7]*2 + [0.75]
        self.two_yUnit = [0.25] + [0.7]*2 + [0.3]*2 + [0.75]
        self.two_zUnit = [0.5] + [0,1]*2 + [0.5]
    
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]
     


class Rutile(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.TupleList = CCPTupleList(self.UnitCell, 1)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
        
    def createUnitCell(self):
        self.one_xUnit = [0]*4 + [0.5] + [1]*4
        self.one_yUnit = [0]*2 + [1]*2 + [0.5] + [0]*2 + [1]*2
        self.one_zUnit = [0,1]*2 + [0.5] + [0,1]*2
        
        self.two_xUnit = [0.25] + [0.3]*2 + [0.7]*2 + [0.75]
        self.two_yUnit = [0.25] + [0.7]*2 + [0.3]*2 + [0.75]
        self.two_zUnit = [0.5] + [0,1]*2 + [0.5]
    
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]
     


##########################################
# A3B Crystal Structures
##########################################        
class Li3Bi(object):
    def __init__(self):
        (self.one_x, self.one_y, self.one_z) = ([],[],[])
        (self.two_x, self.two_y, self.two_z) = ([],[],[])
        self.createUnitCell()
        self.TupleList = CCPTupleList(self.UnitCell, 3)
        self.Cell = removeRepeats(self.TupleList)
        self.coordinates = createCoordinates(self.Cell)
        plot3D(self.coordinates)
    
    def createUnitCell(self):
        self.one_xUnit = [0]*5 + [0.5]*4 + [1]*5
        self.one_yUnit = [0]*2 + [0.5] + [1]*2 + [0] + \
                        [0.5]*2 + [1] + [0]*2 + [0.5] + [1]*2
        self.one_zUnit = [0,1,0.5,0, 1] + [0.5, 0, 1, 0.5] + [0,1,0.5,0, 1]
        self.two_xUnit = [0]*4 + [0.25]*4 + [0.5]*5 + [0.75]*4 + [1]*4
        self.two_yUnit = [0,0.5,0.5,1] + [0.25]*2 + [0.75]*2 + \
                            [0,0,0.5,1,1] + [0.25]*2 + [0.75]*2 + [0,0.5,0.5,1]
        self.two_zUnit = [0.5, 0, 1, 0.5] + [0.25, 0.75]*2 + [0, 1, 0.5, 0, 1]\
                        + [0.25, 0.75]*2 + [0.5, 0, 1, 0.5]
        self.UnitCell = [self.one_xUnit, self.one_yUnit, self.one_zUnit, 
                    self.two_xUnit, self.two_yUnit, self.two_zUnit]
                    
def printArrays(x, y, z):
    for index in range(len(x)):
        print((x[index], y[index], z[index]))


#######################################
# TP2 Update Test Functions
#######################################

#c = SCC()
#d = FCC()
#e = BCC()
#f = HCP()
#g = NaCl()
#h = NiAs()
#i = ZincBlende()
#j = Wurtzite()
#k = Fluorite()
#l = Rutile()
#m = Li3Bi()

############################
# Run Function
############################

def main():
    run = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
