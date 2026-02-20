from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional

from weather_cli.src.domain.models import Record, Station

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError("Cette méthode doit être redéfinie dans les sous-classes.")


class ExtractWeatherCommand(Command):
    def __init__(self, data_extractor, date: datetime, station_id: str):
        self._extractor = data_extractor
        self._date = date
        self._station_id = station_id
        self._raw_records: List[Dict[str, Any]] = []

    def execute(self) -> None:
        self._raw_records = self._extractor.extract(self._date, self._station_id)

    def get_data(self) -> List[Dict[str, Any]]:
        return self._raw_records

class TransformWeatherCommand(Command):
    def __init__(self, data_mapper, station_id: str, raw_records: List[Dict[str, Any]]):
        self._mapper = data_mapper
        self._station_id = station_id
        self._raw_records = raw_records
        self._station: Optional[Station] = None

    def execute(self) -> None:
        if not self._raw_records:
            return

        station = Station(nom=self._station_id)
        for raw_record in self._raw_records:
            record: Optional[Record] = self._mapper.to_object(raw_record)
            if record:
                station.add_mesure(record)

        self._station = station

    def get_data(self) -> Optional[Station]:
        return self._station

class LoadWeatherCommand(Command):
    def __init__(self, cache, cache_key: str, station: Optional[Station]):
        self._cache = cache
        self._cache_key = cache_key
        self._station = station

    def execute(self) -> None:
        if self._station and self._station.mesures:
            self._cache.set(self._cache_key, self._station)

    def get_data(self) -> Optional[Station]:
        return self._station

class WeatherInvoker:
    def __init__(self):
        self._commands: List[Command] = []

    def add_command(self, command: Command) -> None:
        self._commands.append(command)

    def execute_commands(self) -> None:
        for command in self._commands:
            command.execute()
        self._commands.clear()
