from PyQt5.QtCore import QThread, QPoint
from PyQt5.QtGui import QCursor
from ..models import DatabaseWorker, MaterialModel, Material, MouvementModel, Mouvement
from .menu_presenter import MenuAction
from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType
from ..view import MouvementMaterielDialog

class DepotPresenter:
    
    def __init__(self, parent) -> None:
        
        self.view = parent.view.depotInterface
        self.model : MaterialModel = parent.model
        self.moveModel = MouvementModel()
        self.refresh = parent.view.depot
        self.workerThread = None
        self.defaultData = self.model.fetch_all()
        self.fetchData(self.defaultData)
        
        self.refresh.connect(lambda: self.fetchData(self.model.fetch_all()))
        self.__initWidget()
        print(self.model.selectJoin("id","material_id", ["name", "type", "brand"], ["type", "count"], "mouvements"))
        
    def __initWidget(self):
        self.headerLabel = ["Id", "Date", "Rubriques", "Types", "Marques", "Modele", "Nombre", 
                            "Accessoires", "Etat", "Fonctionnalité", "Motif", "Observation", ""]
        self.view.tableView.setHorizontalHeaderLabels(self.headerLabel)
        self.view.tableView.contextMenuEvent = lambda event: self.mouseRightClick(event)
    
    def mouseRightClick(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if (len(selectedItems) != 0):
            idItem = self.view.tableView.selectedItems()[0].text()
            action = MenuAction(self)
            menu = RoundMenu(parent=self.view)
            #menu.addAction(Action(FluentIcon.FOLDER, 'Voir', triggered = lambda:action.show(matricule_item)))
            menu.addAction(Action(FluentIcon.EDIT, 'Modifier', triggered = lambda: action.update(idItem)))
            menu.addAction(Action(FluentIcon.SHARE, 'Mouvement', triggered = lambda: self.showDialog(idItem)))
            menu.addSeparator()
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: action.confirmDelete(idItem)))

            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def showDialog(self, selectedId):
        material : Material= self.model.fetch_item_by_id(selectedId)
        dialog = MouvementMaterielDialog(material, self.view)
        if dialog.exec():
            count = dialog.count.getValue()
            moveType = dialog.typeCombox.combox.text()
            self.moveModel.create(Mouvement(
                material_id=selectedId, 
                type=moveType, 
                count=count))
            updatedCount = material.count + count
            if moveType == "Sortie" :
                updatedCount = material.count - count
            self.model.update_item(selectedId, count=str(updatedCount))
    
    def fetchData(self, data):
        self.view.progressBar.setVisible(True)
        #self.intColFilter()
        self.actionWorkerThread(data)
        
    def actionWorkerThread(self, data):
        if self.workerThread is None or not self.workerThread.isRunning():
            self.workerThread = QThread()
            self.worker = DatabaseWorker(data)
            self.worker.moveToThread(self.workerThread)
            self.workerThread.started.connect(self.worker.run)
            self.worker.progress.connect(self.updateProgress)
            self.worker.result.connect(self.handleResult)
            self.worker.finished.connect(self.workerThread.quit)
            self.workerThread.start()
        else:
            self.workerThread.quit()
    
    def updateProgress(self, progress):
        self.view.progressBar.setValue(int(progress))
        
    def handleResult(self, data:list):
        self.view.progressBar.setVisible(False)
        listData = []
        listData.clear()
        for material in data:
            listData.append([material.id, material.date, material.name, 
                             material.type, material.brand, 
                             material.model, material.count, 
                             material.accessory, material.state,  
                             material.fonctionality,material.motif, material.observation])
        self.view.tableView.setData(listData)
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
            
    