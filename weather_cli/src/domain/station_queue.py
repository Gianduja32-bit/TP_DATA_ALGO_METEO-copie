class Maillon:
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant

    def get_valeur(self):
        return self.valeur

    def get_suivant(self):
        return self.suivant

    def set_suivant(self, suivant):
        self.suivant = suivant


class StationQueue:
    def __init__(self):
        self.premier_maillon = None

    def enqueue(self, station_id: str):
        nouveau_maillon = Maillon(station_id)
        
        if self.premier_maillon is None:
            self.premier_maillon = nouveau_maillon
            return
            
        maillon_actuel = self.premier_maillon
        while maillon_actuel.get_suivant() is not None:
            maillon_actuel = maillon_actuel.get_suivant()
            
        maillon_actuel.set_suivant(nouveau_maillon)

    def dequeue(self) -> str | None:
        if self.is_empty():
            return None
            
        valeur = self.premier_maillon.get_valeur()
        self.premier_maillon = self.premier_maillon.get_suivant()
        return valeur

    def is_empty(self) -> bool:
        return self.premier_maillon is None

