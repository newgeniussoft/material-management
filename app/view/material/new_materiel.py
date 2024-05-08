from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, ComboBox, BodyLabel, CompactSpinBox, DateEdit

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

        self.row = QHBoxLayout()
        self.dateEdit = editWithLabel("Date", self, date="date")
        self.nameEdit = editWithLabel("Rubrique", self, placeholders=["Rubrique"])
        self.typeEdit = editWithLabel("Types", self, placeholders=["Types"])
        self.row.addLayout(self.dateEdit)
        self.row.addLayout(self.nameEdit)
        self.row.addLayout(self.typeEdit)
        
        self.row_2 = QHBoxLayout()
        self.brandEdit = editWithLabel("Marque", self, placeholders=["Marque"])
        self.modelEdit = editWithLabel("Model", self, placeholders=["Model"])
        
        self.countSpinBox = editWithLabel("Nombre", self, spinbox="Nombre")
        self.row_2.addLayout(self.brandEdit)
        self.row_2.addLayout(self.modelEdit)
        self.row_2.addLayout(self.countSpinBox)
        
        self.row_3 = QHBoxLayout()
        self.accessoryEdit = editWithLabel("Accessoire", self, placeholders=["Accessoire"])
        self.stateEdit = editWithLabel("Etat", self, placeholders=["Etat"])
        self.fonctionalityEdit = editWithLabel("Fonctionnalité", self, placeholders=["Fonctionnalité"])
        self.row_3.addLayout(self.accessoryEdit)
        self.row_3.addLayout(self.stateEdit)
        self.row_3.addLayout(self.fonctionalityEdit)
        
        self.row_4 = QHBoxLayout()
        self.motifEdit = editWithLabel("Motif", self, placeholders=["Motif"])
        self.observationEdit = editWithLabel("Observation", self, placeholders=["Observation"])
        self.row_4.addLayout(self.motifEdit)
        self.row_4.addLayout(self.observationEdit)
        

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.row_2)
        self.viewLayout.addLayout(self.row_3)
        self.viewLayout.addLayout(self.row_4)

        # change the text of button
        self.yesButton.setText('Ajouter')
        self.cancelButton.setText('Annuler')

        self.widget.setMinimumWidth(650)
    
    def __isValid(self, text):
        name = self.lastnameEdit.text(0)
        matricule = self.matriculeEdit.text(0)
        if len(name) > 2 and len(matricule) == 4:
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)
