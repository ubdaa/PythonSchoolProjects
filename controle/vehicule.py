from datetime import date

class Vehicule:
    def __init__(self, 
                 marque : str, 
                 modele : str, 
                 annee : date, 
                 kilometrage : int, 
                 disponible : bool):
        self.marque = marque
        self.modele = modele
        self.annee = annee
        self.kilometrage = kilometrage
        self.disponible = disponible
        
    def __str__(self):
        return f"{self.marque} {self.modele} {self.annee} {self.kilometrage} km - {'Disponible' if self.disponible else 'Indisponible'}"
    
    def __repr__(self):
        return f"Vehicule(marque={self.marque}, modele={self.modele}, annee={self.annee}, kilometrage={self.kilometrage}, disponible={self.disponible})"
    
    @property
    def age(self):
        return date.today().year - self.annee.year
    
    def louer(self):
        self.disponible = False
        return
    
    def retourneer(self, km_parcourus : int):
        self.kilometrage += km_parcourus
        self.disponible = True
        return
    
    
class VehiculeElectrique(Vehicule):
    def __init__(self, 
                 marque : str, 
                 modele : str, 
                 annee : date, 
                 kilometrage : int, 
                 disponible : bool,
                 autonomie_km : int,
                 niveau_batterie : float):
        super().__init__(marque, modele, annee, kilometrage, disponible)
        self.autonomie_km = autonomie_km
        self.niveau_batterie = niveau_batterie
        
    def recharger(self):
        self.niveau_batterie = 100.0
        return
    
    def __str__(self):
        return f"{self.marque} {self.modele} {self.annee} {self.kilometrage} km - {'Disponible' if self.disponible else 'Indisponible'}. " + \
                f"Autonomie: {self.autonomie_km} km, batterie: {self.niveau_batterie}%"
        