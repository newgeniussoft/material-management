from PyQt5.QtGui import QCursor, QColor
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QTableWidgetItem
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
        self.setTableHeaderLabels(["ID", "DESIGNATION DE MATERIEL", 
                                   "EN BON", "GRADE", "NOM ET PRENOM", 
                                   "CONTACT", "MOTIF", "LIEU", "DATE DE PERCEPTION", 
                                   "DATE DE REINTEGRATION", "ETAT DU MAT LORS \nDE LA REINTEGRATION"])
        self.setTableContextMenu(self.mouseRightClick)
        
    def fetchData(self, data):
        nData = self.moveModel.select_join(
            ['mouvements.id', 'materials.name', 'mouvements.in_good',
             'mouvements.grade','mouvements.full_name',
             'mouvements.contact', 'mouvements.motif', 
             'mouvements.place', 'mouvements.date_perc', 'mouvements.date_reinteg', 'mouvements.state_mat_integr'], 'materials', 'material_id', order='materials.name')
        return super().fetchData(nData)
        
    def handleResult(self, data: list):
        vItems = []
        rows = []
        self.view.progressBar.setVisible(False)
        nData = [list(item) for item in data]
        self.view.tableView.setRowCount(len(nData))
        for i, item in enumerate(nData):
            for j, nItem in enumerate(item):
                if j == 1:
                    if nItem not in vItems:
                        vItems.append(nItem)
                        rows.append(i)
                self.view.tableView.setItem(i,j,QTableWidgetItem(str(nItem)))
                if nItem == "" and j == len(item) - 2:
                    self.view.tableView.setColorRow(i, 'red')
                if nItem == "EN PANNE" and j == len(item) - 1:
                    self.view.tableView.setColorRow(i, 'red')
        rows.append(len(nData))
        differences = [rows[i] - rows[i-1] for i in range(1, len(rows))]
        for i, row in enumerate(rows):
            if i < len(differences) and differences[i] > 1:
                self.view.tableView.setSpan(row, 1, differences[i], 1)
        self.view.tableView.resizeColumnsToContents()
        
    
    def mouseRightClick(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if (len(selectedItems) != 0):
            if selectedItems[len(selectedItems)-2].text() == "":
                idItem = selectedItems[0].text()
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
        dialog.gradeEdit.setText(str(move.grade))
        dialog.fullNameEdit.setText(str(move.full_name))
        dialog.contactEdit.setText(str(move.contact))
        if dialog.exec():
            inGood = dialog.countInGood.spinbox.value()
            nInGood = str(int(material.in_good) - inGood)
            inStore = dialog.inStoreSpinBox.lineEdit.text()
            be = dialog.beSpinBox.lineEdit.text()
            breakdown = dialog.breakdownSpinBox.lineEdit.text()
            dateReinteg =  dialog.dateReintegEdit.text()
            state = dialog.stateMatIntegr.combox.currentText()
            self.moveModel.update_item(idItem, 
                                       in_good          = nInGood, 
                                       date_reinteg     = dateReinteg,
                                       state_mat_integr = state)
            self.model.update_item(material.id, 
                                   in_good  = nInGood,
                                   in_store = inStore,
                                   be       = be,
                                   breakdown= breakdown)
            self.view.parent.depot.emit()