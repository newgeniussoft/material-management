from ..view import MaterialsInterface

class DepotPresenter:
    
    def __init__(self, view:MaterialsInterface, model) -> None:
        self.view = view
        self.model = model
        self.view.addAction