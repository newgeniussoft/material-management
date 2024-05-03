from ..view import MaterialsInterface, NewMaterielDialog

class MaterialPresenter:
    
    def __init__(self, view:MaterialsInterface, model):
        self.view = view
        self.model = model
        self.__actions()
        
    def __actions(self):
        self.view.addAction.triggered.connect(lambda : self.showDialogNew())
        
    def showDialogNew(self):
        dialog = NewMaterielDialog(self.view)
        dialog.exec()