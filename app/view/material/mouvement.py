from qfluentwidgets import MessageBoxBase, StrongBodyLabel, BodyLabel, ComboBox, SubtitleLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from ...models import Material
from ...components import ComboxEditWithLabel, SpinBoxEditWithLabel

class ValueWithLabel(QVBoxLayout):
    def __init__(self, label:str, value:str, parent=None):
        super().__init__(None)
        self.addWidget(StrongBodyLabel(label))
        self.addWidget(BodyLabel(value))
        self.setSpacing(2)

class MouvementMaterielDialog(MessageBoxBase):

    def __init__(self,material: Material, parent=None):
        super().__init__(parent)
        self.material = material
        
        self.viewLayout.addWidget(SubtitleLabel("Mouvement"))
        self.viewLayout.addWidget(BodyLabel(f'{material.name} {material.type} {material.brand} {material.model}'))
        
        self.row = QHBoxLayout()
        self.row.addLayout(ValueWithLabel("Accessoires", material.accessory))
        
        self.row2 = QHBoxLayout()
        self.row2.addLayout(ValueWithLabel("Etat", material.state))
        self.row2.addLayout(ValueWithLabel("Fonctionnalité", material.fonctionality))
        self.row2.addLayout(ValueWithLabel("Motifs", material.motif))
        
        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.row2)
        #self.viewLayout.addLayout(self.row3)
        self.viewLayout.addLayout(ValueWithLabel("Observation", material.fonctionality))
        
        
        self.viewLayout.addWidget(StrongBodyLabel("Mouvement"))
        
        self.typeCombox = ComboxEditWithLabel("Type", ["Entrée", "Sortie"], self)
        self.count = SpinBoxEditWithLabel("Nombre", self)
        
        self.row3 = QHBoxLayout()
        self.row3.addLayout(self.typeCombox)
        self.row3.addLayout(self.count)
        self.viewLayout.addLayout(self.row3)
        
        
        
        