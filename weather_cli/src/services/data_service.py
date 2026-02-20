from datetime import datetime
from typing import List, Optional

from weather_cli.src.api_manager import IDataExtractor, IDataMapper
from weather_cli.src.domain.models import Record, Station
from weather_cli.src.domain.weather_dict import WeatherDictionary
from weather_cli.src.infrastructure.config.settings import Configuration
from weather_cli.src.domain.commands.weather_commands import (
    ExtractWeatherCommand,
    TransformWeatherCommand,
    LoadWeatherCommand,
    WeatherInvoker,
)


class WeatherDataService:
    def __init__(self, data_extractor: IDataExtractor, data_mapper: IDataMapper):
        self.data_extractor = data_extractor
        self.data_mapper = data_mapper
        self.cache = WeatherDictionary(size=20)

    def get_weather_data_for_station_and_date(
        self, date: datetime, station_name: str
    ) -> Optional[Station]:
        cache_key = f"{station_name}_{date.strftime('%Y-%m-%d')}"

        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data

        extract_command = ExtractWeatherCommand(
            data_extractor=self.data_extractor,
            date=date,
            station_id=station_name,
        )
        extract_command.execute()
        raw_records = extract_command.get_data()

        if not raw_records:
            return None

        transform_command = TransformWeatherCommand(
            data_mapper=self.data_mapper,
            station_id=station_name,
            raw_records=raw_records,
        )
        transform_command.execute()
        station = transform_command.get_data()

        load_command = LoadWeatherCommand(
            cache=self.cache,
            cache_key=cache_key,
            station=station,
        )

        invoker = WeatherInvoker()
        invoker.add_command(load_command)
        invoker.execute_commands()

        return station

    def get_available_stations(self) -> List[str]:
        return list(Configuration.STATION_URLS.keys())
