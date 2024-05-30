from ..models import MaterialModel
from .base_presenter import MaterialPresenter
from ..view import OutTab

class OutPresenter(MaterialPresenter):
    
    def __init__(self, parent):
        self.model: MaterialModel = parent.model
        data = self.model.selectJoin("id", "material_id", 
                                     ['id', 'name', 'type', 'brand', 'model'], 
                                     ['type', 'count', 'date'], 
                                     'mouvements', type="Sortie")
        
        super().__init__(data, parent)
        self.view: OutTab = parent.view.outInterface
        self.refresh.connect(lambda: self.fetchData(data))
        self.setTableHeaderLabels(["Id", "Rubriques", "Types","Marque", "Model", "Mouvements", "Nombre", "Date", ""])
        
    def handleResult(self, data: list):
        super().handleResult(data)
        self.view.tableView.setData(data)