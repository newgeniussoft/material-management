from datetime import datetime
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor
from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType
from .base_presenter import BasePresenter
from .menu_presenter import MenuAction
from ..models import Material, Mouvement
from ..view import MouvementMaterialDialog

class DepotPresenter(BasePresenter):
    
    def __init__(self, parent):
        self.model = parent.model
        super().__init__(self.model.fetch_all(),parent)
        self.setTableHeaderLabels(["ID", "DESIGNATION DE MATERIEL", "EN COMPTE", "EN BON", "EN MAGASIN", "BONNE ETAT", "PANNE", "DATE"])
        self.setTableContextMenu(self.mouseRightClick)
        self.view.parent.refresh.connect(lambda: self.fetchData(self.model.fetch_all()))
        
    def fetchData(self, data):
        nData = self.model.fetch_all()
        return super().fetchData(nData)
        
    def handleResult(self, data: list[Material]):
        super().handleResult(data)
        listData = []
        for material in data:
            listData.append(
                [material.id, material.name, material.into_account, material.in_good, 
                 material.in_store, material.be, material.breakdown, material.date_reinteg] )
        self.view.tableView.setData(listData)
    
    def mouseRightClick(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if (len(selectedItems) != 0):
            idItem = self.view.tableView.selectedItems()[0].text()
            action = MenuAction(self)
            menu = RoundMenu(parent=self.view)
            #menu.addAction(Action(FluentIcon.FOLDER, 'Voir', triggered = lambda:action.show(matricule_item)))
            '''menu.addAction(Action(FluentIcon.EDIT, 'Modifier', triggered = lambda: action.update(idItem)))'''
            menu.addAction(Action(FluentIcon.SHARE, 'Mouvement', triggered = lambda: self.showDialog(idItem)))
            menu.addSeparator()
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: action.confirmDelete(idItem)))

            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def showDialog(self, selectedId):
        material : Material= self.model.fetch_item_by_id(selectedId)
        dialog = MouvementMaterialDialog(material, self.view)
        if dialog.exec():
            # Current date and time
            now = datetime.now()
            today = now.strftime("%d/%m/%Y")
            count = dialog.count.spinbox.value()
            moveType = dialog.typeCombox.combox.text()
            
            self.moveModel.create(Mouvement(
                material_id=selectedId, 
                type=moveType,
                date=today,
                count=count))
            updatedCount = material.count + count
            if moveType == "Sortie" :
                updatedCount = material.count - count
            self.model.update_item(selectedId, count=str(updatedCount))
            self.view.parent.nParent.refresh.emit()