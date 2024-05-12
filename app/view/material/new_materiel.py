from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QPoint
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, ComboBox, BodyLabel,\
    StrongBodyLabel, CompactSpinBox, DateEdit, PrimaryPushButton, FluentIcon, RoundMenu,\
        Action, MenuAnimationType
from ...components.table_view import TableView

class editWithLabel(QVBoxLayout):
    def __init__(self, label:str,parent=None, **kwargs):
        super().__init__(None)
        self.parent = parent
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(5)
        self.label = BodyLabel(parent)
        self.label.setText(label)
        self.addWidget(self.label)
        self.args = kwargs
        self.lineEdits = []
        self.LineEdit()

    def LineEdit(self):
        self.hBoxLayout = QHBoxLayout()
        self.lineEdits.clear()
        if "placeholders" in self.args.keys():
            placeholders = self.args.get("placeholders")
            for placeholder in placeholders:
                lineEdit = LineEdit(self.parent)
                lineEdit.setClearButtonEnabled(True)
                lineEdit.setPlaceholderText(placeholder)
                self.hBoxLayout.addWidget(lineEdit)
                self.lineEdits.append(lineEdit)
                
        if "combox" in self.args.keys():
            self.combox = ComboBox(self.parent)
            self.combox.setMinimumWidth(200)
            self.combox.addItems(self.args.get("combox"))
            self.hBoxLayout.addWidget(self.combox)
            
        if "spinbox" in self.args.keys():
            self.compactSpinBox = CompactSpinBox(self.parent)
            self.hBoxLayout.addWidget(self.compactSpinBox)
            
        if "date" in self.args.keys():
            self.date = DateEdit(self.parent)
            self.hBoxLayout.addWidget(self.date)
            
        self.addLayout(self.hBoxLayout)
        
    
    def getValue(self) -> int:
        return self.compactSpinBox.value()
            
    def value(self):
        return self.combox.text()
    
    def text(self, pos:int):
        return self.lineEdits[pos].text()
    
    def lineEdit(self, pos:int) -> LineEdit:
        return self.lineEdits[pos]
        


class NewMaterielDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Matériels entrants', self)
        self.accessory = []
        self.parent = parent
        self.row = QHBoxLayout()
        self.dateEdit = editWithLabel("Date", self, date="date")
        self.nameEdit = editWithLabel("Rubrique", self, placeholders=["Rubrique"])
        self.nameEdit.lineEdit(0).textChanged.connect(self.__isValid)
        self.typeEdit = editWithLabel("Types", self, placeholders=["Types"])
        self.typeEdit.lineEdit(0).textChanged.connect(self.__isValid)
        self.row.addLayout(self.dateEdit)
        self.row.addLayout(self.nameEdit)
        self.row.addLayout(self.typeEdit)
        
        self.row_2 = QHBoxLayout()
        self.brandEdit = editWithLabel("Marque", self, placeholders=["Marque"])
        self.modelEdit = editWithLabel("Model", self, placeholders=["Model"])
        
        self.countSpinBox = editWithLabel("Nombre", self, spinbox="Nombre")
        self.countSpinBox.compactSpinBox.textChanged.connect(self.__isValid)
        self.row_2.addLayout(self.brandEdit)
        self.row_2.addLayout(self.modelEdit)
        self.row_2.addLayout(self.countSpinBox)
        
        self.accTitle = StrongBodyLabel("Accessoires")
        self.accTable = TableView(parent)
        self.accTable.contextMenuEvent = lambda event: self.mouseRightClick(event)
        self.accTable.setHorizontalHeaderLabels(['Nombres', 'Rubriques'])
        
        self.row_3 = QHBoxLayout()
        self.accCountSpinBox = editWithLabel("Nombre", self, spinbox="Nombre")
        self.accCountSpinBox.compactSpinBox.textChanged.connect(self.__isAccValid)
        self.accessoryEdit = editWithLabel("Rubrique accessoire", self, placeholders=["Accessoire"])
        self.accessoryEdit.lineEdit(0).textChanged.connect(self.__isAccValid)
        self.btnAddAccessory = PrimaryPushButton(FluentIcon.ACCEPT, 'Ajouter', parent)
        self.btnAddAccessory.setEnabled(False)
        self.btnAddAccessory.clicked.connect(lambda: self.addAccessory())
        self.row_3.addLayout(self.accCountSpinBox)
        self.row_3.addLayout(self.accessoryEdit)
        self.row_3.addWidget(self.btnAddAccessory, alignment=Qt.AlignBottom)
        
        self.row_4 = QHBoxLayout()
        self.stateEdit = editWithLabel("Etat", self, placeholders=["Etat"])
        self.fonctionalityEdit = editWithLabel("Fonctionnalité", self, placeholders=["Fonctionnalité"])
        self.row_4.addLayout(self.stateEdit)
        self.row_4.addLayout(self.fonctionalityEdit)
        
        self.row_5 = QHBoxLayout()
        self.motifEdit = editWithLabel("Motif", self, placeholders=["Motif"])
        self.observationEdit = editWithLabel("Observation", self, placeholders=["Observation"])
        self.row_5.addLayout(self.motifEdit)
        self.row_5.addLayout(self.observationEdit)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.row_2)
        self.viewLayout.addLayout(self.row_4)
        self.viewLayout.addLayout(self.row_5)
        self.viewLayout.addWidget(self.accTitle, Qt.AlignCenter)
        self.viewLayout.addLayout(self.row_3)
        self.viewLayout.addWidget(self.accTable)

        # change the text of button
        self.yesButton.setText('Ajouter')
        self.yesButton.setEnabled(False)
        self.cancelButton.setText('Annuler')

        self.widget.setMinimumWidth(650)
        
    def addAccessory(self):
        labelEdit = self.accessoryEdit.lineEdit(0)
        self.accessory.append([self.accCountSpinBox.getValue(),labelEdit.text()])
        labelEdit.setText("")
        self.accTable.setData(self.accessory)
        
    def mouseRightClick(self, event):
        selectedItems = self.accTable.selectedItems()
        if (len(selectedItems) != 0):
            menu = RoundMenu(parent=self.parent)
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: self.__deleteAccessory(selectedItems)))
            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def __deleteAccessory(self, items: list):
        for i, acc in enumerate(self.accessory):
            if acc[0] == int(items[0].text()) and acc[1] == items[1].text():
                self.accessory.remove(acc)
        self.accTable.setData(self.accessory)
        
    def __isAccValid(self, value):
        cnt = self.accCountSpinBox.getValue()
        text = self.accessoryEdit.lineEdit(0).text()
        if len(text) > 3 and cnt > 0:
            self.btnAddAccessory.setEnabled(True)
        else:
            self.btnAddAccessory.setEnabled(False)
            
    def __isValid(self, text):
        name = self.nameEdit.lineEdit(0).text()
        nType = self.typeEdit.lineEdit(0).text()
        count = self.countSpinBox.getValue()
        self.yesButton.setEnabled(len(name) > 2 and len(nType) > 2 and count > 0)

