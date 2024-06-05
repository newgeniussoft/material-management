from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from qfluentwidgets import Dialog, SubtitleLabel, StrongBodyLabel, PrimaryPushButton, FluentIcon, \
    RoundMenu, Action, BodyLabel
from ....components import LineEditWithLabel, DateEditWithLabel, SpinBoxEditWithLabel, TableView, ComboxEditWithLabel

class ValueWithLabel(QVBoxLayout):
    def __init__(self, label:str, value:str, parent=None):
        super().__init__(None)
        self.addWidget(StrongBodyLabel(label))
        self.addWidget(BodyLabel(value))
        self.setSpacing(2)
        
class MouvementMaterialDialog(Dialog):
    
    def __init__(self, material, parent=None):
        super().__init__("", "", parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        self.material = material
        
        self.textLayout.addWidget(SubtitleLabel("Mouvement"))
        self.textLayout.addWidget(BodyLabel(f'{material.name} {material.type} {material.brand} {material.model}'))
        
        self.row = QHBoxLayout()
        self.row.addLayout(ValueWithLabel("Accessoires", material.accessory))
        
        self.row2 = QHBoxLayout()
        self.row2.addLayout(ValueWithLabel("Etat", material.state))
        self.row2.addLayout(ValueWithLabel("Fonctionnalité", material.fonctionality))
        self.row2.addLayout(ValueWithLabel("Motifs", material.motif))
        
        self.textLayout.addLayout(self.row)
        self.textLayout.addLayout(self.row2)
        self.textLayout.addLayout(ValueWithLabel("Observation", material.fonctionality))
        self.textLayout.addWidget(StrongBodyLabel("Mouvement"))
        
        self.typeCombox = ComboxEditWithLabel("Type", ["Entrée", "Sortie"])
        self.count = SpinBoxEditWithLabel("Nombre")
        self.motif = LineEditWithLabel("Motif")
        
        self.row3 = QHBoxLayout()
        self.row3.addLayout(self.typeCombox)
        self.row3.addLayout(self.count)
        self.textLayout.addLayout(self.row3)
        self.textLayout.addLayout(self.motif)
        
        self.setFixedWidth(600)