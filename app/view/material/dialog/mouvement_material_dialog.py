from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from qfluentwidgets import Dialog, SubtitleLabel, StrongBodyLabel, PrimaryPushButton, FluentIcon, \
    RoundMenu, Action, BodyLabel
from ....components import LineEditWithLabel, DateEditWithLabel, SpinBoxEditWithLabel, TableView, ComboxEditWithLabel
from ....models import Material

class ValueWithLabel(QVBoxLayout):
    def __init__(self, label:str, value, parent=None):
        super().__init__(None)
        self.addWidget(StrongBodyLabel(label))
        self.addWidget(BodyLabel(str(value)))
        self.setSpacing(2)
        
class MouvementMaterialDialog(Dialog):
    
    def __init__(self, material: Material, parent=None):
        super().__init__("", "", parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        self.textLayout.addWidget(SubtitleLabel("Mouvement"))
        self.row = QHBoxLayout()
        self.row.addLayout(ValueWithLabel("Designation", material.name))
        self.row.addLayout(ValueWithLabel("En compte", material.into_account))
        self.row.addLayout(ValueWithLabel("En bon", material.in_good))
        self.row.addLayout(ValueWithLabel("En magasin", material.in_store))
        self.row.addLayout(ValueWithLabel("En bonne état", material.be))
        self.row.addLayout(ValueWithLabel("En panne", material.breakdown))
        
        self.textLayout.addLayout(self.row)
        self.setFixedWidth(600)