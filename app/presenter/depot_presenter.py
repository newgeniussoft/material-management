from PyQt5.QtCore import QThread
from ..models import DatabaseWorker

class DepotPresenter:
    
    def __init__(self, parent) -> None:
        
        self.view = parent.view.depotInterface
        self.model = parent.model
        self.refresh = parent.view.depot
        self.workerThread = None
        self.defaultData = self.model.fetch_all()
        self.fetchData(self.defaultData)
        
        self.refresh.connect(lambda: self.fetchData(self.model.fetch_all()))
        self.__initWidget()
        
    def __initWidget(self):
        self.headerLabel = ["Date","Rubriques","Types", "Marques", "Modele", "Nombre", "Accessoires", "Etat", "Fonctionnalité", "Motif", "Observation", ""]
        self.view.tableView.setHorizontalHeaderLabels(self.headerLabel)
    
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
            listData.append([material.date, material.name, 
                             material.type, material.brand, 
                             material.model, material.count, 
                             material.accessory, material.state,  
                             material.fonctionality,material.motif, material.observation])
        self.view.tableView.setData(listData)
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
            
    