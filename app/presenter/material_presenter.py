from ..view import MaterialsInterface, NewMaterialDialog, InitialMaterialDialog, LotDialog
from ..models import Material, MaterialModel, MouvementModel, Mouvement, Lot, LotModel
from .depot_presenter import DepotPresenter
from .in_presenter import InPresenter
from .out_presenter import OutPresenter

class MaterialPresenter:
    
    def __init__(self, view:MaterialsInterface, model: MaterialModel):
        self.view = view
        self.model = model
        self.moveModel = MouvementModel()
        self.lotModel = LotModel()
        self.__actions()
        self.depotPresenter = DepotPresenter(self)
        self.inPresenter = InPresenter(self)
        self.outPresenter = OutPresenter(self)
        
    def __actions(self):
        self.view.addAction.triggered.connect(lambda : self.showDialogNew())
        self.view.addLot.triggered.connect(lambda : self.showLotDialog())
        
    def showLotDialog(self):
        dialog = LotDialog(self.view)
        data = self.lotModel.fetch_all()
        lots = [[item.id, item.name] for item in data]
        dialog.table.setData(lots)
        dialog.yesBtn.clicked.connect(lambda: self.createUpdateLots(dialog))
        dialog.exec()
            
    def createUpdateLots(self, dialog: LotDialog):
        data = dialog.table.getData()
        ids = [int(item[0]) if item[0] != '' else 0 for item in data]
        lots = [Lot(id=int(item[0]) if item[0] != "" else 0, name=item[1]) for item in data]
        for item in self.lotModel.fetch_all():
            if item.id not in ids:
                self.lotModel.delete_item(item.id)
        for lot in lots:
            if lot.id == 0:
                self.lotModel.create(lot)
            else:
                self.lotModel.update_item(lot.id, name=lot.name)
        dialog.accept()
        
    def showDialogNew(self):
        dialog = InitialMaterialDialog(self.view)
        if dialog.exec():
            name = dialog.nameEdit.lineEdit.text()
            intoAccount = dialog.intoAccountSpinBox.spinbox.value()
            be = dialog.beSpinBox.spinbox.value()
            breakdown = dialog.breakdownSpinBox.spinbox.value()
            grade = dialog.gradeEdit.lineEdit.text()
            fullName = dialog.fullNameEdit.lineEdit.text()
            contact = dialog.contactEdit.lineEdit.text()
            dateReinteg = dialog.dateReintegEdit.lineEdit.text()
            material = Material(
                name         = name,
                into_account = intoAccount,
                be           = be,
                breakdown    = breakdown,
                grade        = grade,
                full_name    = fullName,
                contact      = contact,
                date_reinteg = dateReinteg
            )
            self.model.create(material)
            self.view.depot.emit()