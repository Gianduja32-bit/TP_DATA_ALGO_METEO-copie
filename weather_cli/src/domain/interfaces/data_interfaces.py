from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Optional

class IDataExtractor(ABC):
    @abstractmethod
    def extract(self, date: datetime, station_id: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

class IDataMapper(ABC):
    @abstractmethod
    def to_object(self, data: Dict[str, Any]) -> Any:
        pass
