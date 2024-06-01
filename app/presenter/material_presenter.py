from ..view import MaterialsInterface, AddMaterialDialog
from ..models import Material, MaterialModel
from .depot_presenter import DepotPresenter
from .in_presenter import InPresenter
from .out_presenter import OutPresenter

class MaterialPresenter:
    
    
    def __init__(self, view:MaterialsInterface, model: MaterialModel):
        self.view = view
        self.model = model
        self.__actions()
        self.depotPresenter = DepotPresenter(self)
        self.inPresenter = InPresenter(self)
        self.outPresenter = OutPresenter(self)
        
    def __actions(self):
        self.view.addAction.triggered.connect(lambda : self.showDialogNew())
        
    def showDialogNew(self):
        dialog = AddMaterialDialog(self.view)
        if dialog.exec():
            date = dialog.dateEdit.lineEdit.text()
            name = dialog.nameEdit.lineEdit.text();
            mtype = dialog.typeEdit.lineEdit.text()
            brand = dialog.brandEdit.lineEdit.text()
            model = dialog.modelEdit.lineEdit.text()
            accessories = dialog.accessory
            accessory = ""
            for acc in accessories:
                accessory += f'{acc[0]} {acc[1]} '
            
            state = dialog.stateEdit.lineEdit.text()
            fonctionality = dialog.fonctionalityEdit.lineEdit.text()
            motif = dialog.motifEdit.lineEdit.text();
            observation = dialog.observationEdit.lineEdit.text()
            count = dialog.countSpinBox.spinbox.text()
            material = Material(date=date,
                                name=name, type=mtype, 
                                brand=brand, model=model, 
                                accessory=accessory, state=state, 
                                fonctionality=fonctionality,motif=motif, 
                                observation=observation, count=count)
            self.model.create(material)
            self.view.depot.emit()