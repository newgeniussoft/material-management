from ..models import MaterialModel
from .base_presenter import BasePresenter
from ..view import OutTab

class OutPresenter(BasePresenter):
    
    def __init__(self, parent):
        self.model: MaterialModel = parent.model
        data = []
        
        super().__init__(data, parent)
        '''self.view: OutTab = parent.view.outInterface
        self.refresh.connect(lambda: self.fetchData(data))'''
        self.setTableHeaderLabels(["Id", "Rubriques", "Types","Marque", "Model", "Mouvements", "Nombre", "Date", ""])
        
    '''def handleResult(self, data: list):
        super().handleResult(data)
        self.view.tableView.setData(data)'''