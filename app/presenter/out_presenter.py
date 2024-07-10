from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QPoint, Qt
from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType
from ..models import MaterialModel, Mouvement, MouvementModel, Material
from .base_presenter import BasePresenter
from ..view import OutTab, ReintMaterialDialog

class OutPresenter(BasePresenter):
    
    def __init__(self, parent):
        self.model: MaterialModel = parent.model
        self.moveModel: MouvementModel = parent.moveModel
        super().__init__([], parent)
        self.view: OutTab = parent.view.outInterface
        self.refresh.connect(lambda: self.fetchData([]))
        self.setTableHeaderLabels(["ID", "DESIGNATION DE MATERIEL", "EN BON", "GRADE", "NOM ET PRENOM", "CONTACT", "MOTIF", "LIEU", "DATE DE PERCEPTION"])
        self.setTableContextMenu(self.mouseRightClick)
        
    def fetchData(self, data):
        nData = self.moveModel.select_join(
            ['mouvements.id', 'materials.name', 'mouvements.in_good',
             'mouvements.grade','mouvements.full_name',
             'mouvements.contact', 'mouvements.motif', 
             'mouvements.place', 'mouvements.date_perc'], 'materials', 'material_id')
        return super().fetchData(nData)
        
    def handleResult(self, data: list):
        self.view.progressBar.setVisible(False)
        self.view.tableView.setData([list(item) for item in data])
        
    
    def mouseRightClick(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if (len(selectedItems) != 0):
            idItem = self.view.tableView.selectedItems()[0].text()
            menu = RoundMenu(parent=self.view)
            menu.addAction(Action(FluentIcon.SHARE, 'Réintegration', triggered=lambda: self.showDialog(idItem)))

            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def showDialog(self, idItem):
        move = self.moveModel.fetch_all(id=idItem)[0]
        material = self.model.fetch_all(id=move.material_id)[0]
        dialog = ReintMaterialDialog(material, self.view)
        dialog.countInGood.spinbox.setValue(move.in_good)
        dialog.countInGood.spinbox.setMaximum(move.in_good)
        if dialog.exec():
            pass