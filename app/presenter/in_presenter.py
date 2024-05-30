from ..models import MaterialModel
from .base_presenter import MaterialPresenter
from ..view import EntryTab

class InPresenter(MaterialPresenter):
    
    def __init__(self, parent):
        self.model: MaterialModel = parent.model
        data = self.model.selectJoin("id", "material_id", 
                                     ['id', 'name', 'type', 'brand', 'model'], 
                                     ['type', 'count', 'date'], 
                                     'mouvements', type="Entrée")
        
        super().__init__(data, parent)
        self.view: EntryTab = parent.view.entryInterface
        self.refresh.connect(lambda: self.fetchData(data))
        self.setTableHeaderLabels(["Id", "Rubriques", "Types","Marque", "Model", "Mouvements", "Nombre", "Date", ""])
        
    def handleResult(self, data: list):
        super().handleResult(data)
        self.view.tableView.setData(data)