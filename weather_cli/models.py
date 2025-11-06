from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Record:
    temperature: float
    humidity: float
    pressure: float
    timestamp: datetime = field(compare=False)

@dataclass
class Station:
    nom: str
    mesures: List[Record] = field(default_factory=list)

    def add_mesure(self, mesure: Record):
        self.mesures.append(mesure)

@dataclass
class Ville:
    nom: str
    stations: List[Station] = field(default_factory=list)

    def add_station(self, station: Station):
        self.stations.append(station)
