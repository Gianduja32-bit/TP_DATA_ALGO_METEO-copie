from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Record:
    """Représente une mesure météo à un instant donné."""
    temperature: float
    humidity: float
    pressure: float
    timestamp: datetime = field(compare=False)

@dataclass
class Station:
    """Représente une station météo avec ses mesures."""
    nom: str
    mesures: List[Record] = field(default_factory=list)

    def add_mesure(self, mesure: Record):
        """
        Ajoute une mesure à la station.
        
        Args:
            mesure: La mesure météo à ajouter
        """
        self.mesures.append(mesure)
