from ..view import MaterialsInterface, NewMaterielDialog
from ..models import Material, MaterialModel
from .depot_presenter import DepotPresenter
from .in_presenter import InPresenter

class MaterialPresenter:
    
    
    def __init__(self, view:MaterialsInterface, model: MaterialModel):
        self.view = view
        self.model = model
        self.__actions()
        self.depotPresenter = DepotPresenter(self)
        self.inPresenter = InPresenter(self)
        
    def __actions(self):
        self.view.addAction.triggered.connect(lambda : self.showDialogNew())
        
    def showDialogNew(self):
        dialog = NewMaterielDialog(self.view)
        if dialog.exec():
            date = dialog.dateEdit.date.text()
            name = dialog.nameEdit.text(0);
            mtype = dialog.typeEdit.text(0);
            brand = dialog.brandEdit.text(0);
            model = dialog.modelEdit.text(0);
            accessories = dialog.accessory
            accessory = ""
            for acc in accessories:
                accessory += f'{acc[0]} {acc[1]} '
            
            state = dialog.stateEdit.text(0);
            fonctionality = dialog.fonctionalityEdit.text(0);
            motif = dialog.motifEdit.text(0);
            observation = dialog.observationEdit.text(0);
            count = dialog.countSpinBox.getValue()
            material = Material(date=date,
                                name=name, type=mtype, 
                                brand=brand, model=model, 
                                accessory=accessory, state=state, 
                                fonctionality=fonctionality,motif=motif, 
                                observation=observation, count=count)
            self.model.create(material)
            self.view.depot.emit()