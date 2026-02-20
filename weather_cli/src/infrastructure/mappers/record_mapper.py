from typing import Dict, Any, Optional
from datetime import datetime
from weather_cli.src.domain.models import Record
from weather_cli.src.domain.interfaces.data_interfaces import IDataMapper

class RecordMapper(IDataMapper):
    def to_object(self, data: Dict[str, Any]) -> Optional[Record]:
        try:
            temperature = data.get("temperature_en_degre_c")
            humidity = data.get("humidite")
            pressure = data.get("pression")
            timestamp_str = data.get("heure_de_paris")

            if all([temperature is not None, humidity is not None, pressure is not None, timestamp_str]):
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                return Record(
                    temperature=float(temperature),
                    humidity=float(humidity),
                    pressure=float(pressure),
                    timestamp=timestamp
                )
            return None
        except (ValueError, TypeError) as e:
            print(f"Erreur lors du mappage des données de record: {e} — Données brutes: {data}")
            return None
