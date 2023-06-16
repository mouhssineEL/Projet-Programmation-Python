from .Ressource import *

class Tile:
    def __init__(self):
        self.xTile = 0
        self.yTile = 0
        self.empty = True
        self.ressource = Ressource.__init__()
        self.idElem = -1
        self.nomElement = ""


    def __init__(self, xTile, yTile, empty, ressource, idElem):
        self.xTile = xTile
        self.yTile = yTile
        self.empty = empty
        self.ressource = ressource
        self.idElem = idElem
        self.nomElement = ""

    def isEmpty(self):
        return self.empty

    def getRessource(self):
        return self.ressource

    def setRessource(self, ressource):
        self.ressource = ressource

    def reduceRessource(self, nbRessources):
        self.ressource = ressource - nbRessources

    def setEmpty(self,empty):
        self.empty = empty

    def setIdElement(self,idElem):
        self.idElem = idElem

    def getIdElement(self):
        return self.idElem