class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Configuration(metaclass=SingletonMeta):
    STATION_URLS = {
        "Toulouse Parc Compans-Caffarelli": "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/42-station-meteo-toulouse-parc-compans-cafarelli/records",
        "Toulouse Université Paul Sabatier": "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/37-station-meteo-toulouse-universite-paul-sabatier/records"
    }
