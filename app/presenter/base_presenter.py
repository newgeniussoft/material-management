from PyQt5.QtCore import QThread, QPoint
from ..models import MaterialModel, MouvementModel, DatabaseWorker

class MaterialPresenter:
    
    def __init__(self, data, parent):
        self.__init_var(data,parent)
        self.refresh.connect(lambda: self.fetchData(data))
        
    def __init_var(self, data,  parent):
        self.parent = parent
        self.view = parent.view.depotInterface
        self.model : MaterialModel = parent.model
        self.moveModel = MouvementModel()
        self.refresh = parent.view.depot
        self.workerThread = None
        self.defaultData = data
        self.fetchData(self.defaultData)
    
    def fetchData(self, data):
        self.view.progressBar.setVisible(True)
        self.actionWorkerThread(data)
        
    def setTableHeaderLabels(self, headerLabels: list):
        self.view.tableView.setHorizontalHeaderLabels(headerLabels)
        
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
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        
    def setTableContextMenu(self, contextMenu):
        self.view.tableView.contextMenuEvent = lambda event: contextMenu(event)
            
        