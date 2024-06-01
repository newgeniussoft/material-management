from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor
from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType, MessageDialog
from ..models import MaterialModel
from .base_presenter import BasePresenter
from ..view import EntryTab

class InPresenter(BasePresenter):
    
    def __init__(self, parent):
        self.model: MaterialModel = parent.model
        tableMove = "mouvements"
        self.data = self.model.join("id", "material_id", 
                                    [f"{tableMove}.id", f"{tableMove}.date", 
                                     f"{self.model.TABLE}.name", 
                                     f"{self.model.TABLE}.type", 
                                     f"{self.model.TABLE}.brand",
                                     f"{self.model.TABLE}.model",
                                     f"{tableMove}.count"], tableMove, type="Entrée")
        
        super().__init__(self.data , parent)
        self.view: EntryTab = parent.view.entryInterface
        self.refresh.connect(lambda: self.fetchData(self.data ))
        self.setTableHeaderLabels(["Id", "Date", "Rubriques", "Types","Marque", "Model",  "Nombre", ""])
        self.view.tableView.contextMenuEvent = lambda e : self.tableRightClick(e)
            
    def tableRightClick(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if (len(selectedItems) != 0):
            menu = RoundMenu(parent=self.view)
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: self.confirmDialog(selectedItems[0].text())))
            self.posCur = QCursor().pos()
            menu.exec(QPoint(self.posCur.x(), self.posCur.y()), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
        
    def confirmDialog(self, item):
        dialog = MessageDialog("Supprimer?", "Voulez-vous le supprimer vraiment?", self.view.parent.nParent)
        if dialog.exec():
            self.deleteItem(item)
            
    def deleteItem(self, item):
        self.model.delete_item(item)
        
    def handleResult(self, data: list):
        super().handleResult(data)
        self.view.tableView.setData(data)