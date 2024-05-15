from qfluentwidgets import MessageBoxBase, StrongBodyLabel, BodyLabel, ComboBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from ...models import Material

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
        
        self.row = QHBoxLayout()
        self.row.addLayout(ValueWithLabel("Date", material.date))
        self.row.addLayout(ValueWithLabel("Rubrique", material.name))
        self.row.addLayout(ValueWithLabel("Type", material.type))
        self.row.addLayout(ValueWithLabel("Marque", material.brand))
        
        self.row2 = QHBoxLayout()
        self.row2.addLayout(ValueWithLabel("Modèle", material.model))
        self.row2.addLayout(ValueWithLabel("Accessoires", material.accessory))
        
        self.row3 = QHBoxLayout()
        self.row3.addLayout(ValueWithLabel("Etat", material.state))
        self.row3.addLayout(ValueWithLabel("Fonctionnalité", material.fonctionality))
        self.row3.addLayout(ValueWithLabel("Motifs", material.motif))
        
        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.row2)
        self.viewLayout.addLayout(self.row3)
        self.viewLayout.addLayout(ValueWithLabel("Observation", material.fonctionality))
        
        self.mouvementCombox = ComboBox(self)
        self.mouvementCombox.addItems(["Entrée", "Sortie"])
        
        self.viewLayout.addWidget(StrongBodyLabel("Mouvement"))
        self.viewLayout.addWidget(self.mouvementCombox)
        
        
        
        