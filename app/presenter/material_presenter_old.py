from ..view import MaterialsInterface, NewMaterialDialog, InitialMaterialDialog
from ..models import Material, MaterialModel, MouvementModel, Mouvement
from .depot_presenter import DepotPresenter
from .in_presenter import InPresenter
from .out_presenter import OutPresenter

class MaterialPresenter:
    
    def __init__(self, view:MaterialsInterface, model: MaterialModel):
        self.view = view
        self.model = model
        self.moveModel = MouvementModel()
        self.__actions()
        self.depotPresenter = DepotPresenter(self)
        self.inPresenter = InPresenter(self)
        self.outPresenter = OutPresenter(self)
        
    def __actions(self):
        self.view.addAction.triggered.connect(lambda : self.showDialogNew())
        
    def showDialogNew(self):
        dialog = InitialMaterialDialog(self.view)
        if dialog.exec():
            
            '''name = dialog.nameEdit.lineEdit.text()
            intoAccount = dialog.intoAccountSpinBox.spinbox.value()
            inGood = dialog.inGoodSpinBox.spinbox.value()
            inStore = dialog.inStoreSpinBox.spinbox.value()
            be = dialog.beSpinBox.spinbox.value()
            breakdown = dialog.breakdownSpinBox.spinbox.value()
            grade = dialog.gradeEdit.lineEdit.text()
            fullName = dialog.fullNameEdit.lineEdit.text()
            contact = dialog.contactEdit.lineEdit.text()
            motif = dialog.motifEdit.lineEdit.text()
            place = dialog.placeEdit.lineEdit.text()
            datePerc = dialog.datePercEdit.lineEdit.text()
            dateReinteg = dialog.dateReintegEdit.lineEdit.text()
            stateMatIntegr = dialog.stateMatIntegr.combox.currentText()
            material = Material(
                name         = name,
                into_account = intoAccount,
                in_good      = inGood,
                in_store     = inStore,
                be           = be,
                breakdown    = breakdown,
                grade        = grade,
                full_name    = fullName,
                contact      = contact,
                motif        = motif,
                place        = place,
                date_perc    = datePerc,
                date_reinteg = dateReinteg,
                state_mat_integr=stateMatIntegr
            )
            self.model.create(material)
            self.view.depot.emit()'''