from ..models import MaterialModel, Mouvement
from .base_presenter import BasePresenter
from ..view import OutTab

class OutPresenter(BasePresenter):
    
    def __init__(self, parent):
        self.model: MaterialModel = parent.model
        
        data = parent.moveModel.fetch_all()
        
        super().__init__(data, parent)
        self.view: OutTab = parent.view.outInterface
        self.refresh.connect(lambda: self.fetchData(data))
        self.setTableHeaderLabels(["ID", "DESIGNATION DE MATERIEL", "EN BON", "GRADE NOM ET PRENOM", "CONTACT", "MOTIF", "LIEU", "DATE"])
        
    def handleResult(self, data: list[Mouvement]):
        nData = []
        for move in data:
            nData.append([
                move.id,
                move.material_id,
                move.in_good,
                f'{move.grade} {move.full_name}',
                move.contact,
                move.motif,
                move.place,
                move.date_perc
            ])
        self.view.tableView.setData(nData)