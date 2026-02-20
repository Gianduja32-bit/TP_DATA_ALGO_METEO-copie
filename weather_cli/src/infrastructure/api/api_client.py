import requests
import pytz
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from weather_cli.src.domain.interfaces.data_interfaces import IDataExtractor
from weather_cli.src.infrastructure.config.settings import Configuration

class ApiDataExtractor(IDataExtractor):
    def __init__(self):
        pass

    def extract(self, date: datetime, station_id: Optional[str] = None) -> List[Dict[str, Any]]:
        base_url = Configuration.STATION_URLS.get(station_id)
        if not base_url:
            raise ValueError(f"Station ID '{station_id}' not found in configuration.")

        try:
            params = {
                "limit": 5,
                "order_by": "-heure_de_paris",
                "timezone": "Europe/Paris"
            }

            if station_id:
                params["refine.nom_de_la_station"] = station_id

            response = requests.get(base_url, params=params)
            response.raise_for_status()

            records = response.json().get("results", [])

            paris_tz = pytz.timezone('Europe/Paris')

            target_date_aware = paris_tz.localize(date.replace(hour=0, minute=0, second=0, microsecond=0))
            end_of_target_day_aware = target_date_aware + timedelta(days=1, microseconds=-1)

            filtered_records = []

            for record in records:
                record_date_str = record.get("heure_de_paris")
                if not record_date_str:
                    continue

                record_datetime = datetime.fromisoformat(record_date_str.replace("Z", "+00:00"))
                record_datetime = record_datetime.astimezone(paris_tz)

                if target_date_aware <= record_datetime <= end_of_target_day_aware:
                    filtered_records.append(record)

            return filtered_records

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données API: {e}")
            return []
