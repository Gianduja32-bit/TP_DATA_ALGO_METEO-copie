from rich.console import Console
from rich.panel import Panel
from datetime import datetime

from weather_cli.src.api_manager import ApiDataExtractor, RecordMapper, Configuration
from weather_cli.src.services.data_service import WeatherDataService
from weather_cli.src.services.display_service import StationDisplayDecorator, RecordDisplayDecorator
from weather_cli.src.utils.validators import validate_station_name
from weather_cli.src.domain.models import Station
from weather_cli.src.domain.station_queue import StationQueue

console = Console()

def display_main_menu():
    """Affiche le menu principal de l'application."""
    console.print(Panel("[bold green]=== APPLICATION MÉTÉO TOULOUSAINE ===[/bold green]"))
    console.print("1. Choisir une station")
    console.print("2. Actualiser les données")
    console.print("3. Station suivante")
    console.print("4. Quitter")
    console.print("-" * 37)

def get_station_choice(data_service: WeatherDataService) -> str:
    """
    Demande à l'utilisateur de choisir une station parmi celles disponibles.
    
    Args:
        data_service: Service de données météo
        
    Returns:
        L'identifiant de la station choisie ou une chaîne vide
    """
    available_stations = data_service.get_available_stations()
    if not available_stations:
        console.print("[red]Aucune station disponible. Impossible de choisir.[/red]")
        return ""

    stations_str = ", ".join(available_stations)
    while True:
        station_input = console.input(f"[bold blue]Entrez le nom de la station ({stations_str}) : [/bold blue]")
        validated_station = validate_station_name(station_input, available_stations)
        if validated_station:
            return validated_station


def display_weather_data(station_data: Station | None, station_id: str):
    """
    Affiche les données météo pour une station donnée.
    Fonction créée pour respecter le principe DRY (Don't Repeat Yourself).
    
    Args:
        station_data: Données de la station ou None
        station_id: Identifiant de la station
    """
    if station_data and station_data.mesures:
        station_decorator = StationDisplayDecorator(station_data)
        station_decorator.show()
        for record in station_data.mesures:
            record_decorator = RecordDisplayDecorator(record)
            record_decorator.show()
    else:
        console.print("[yellow]Aucune donnée météo disponible pour cette station et cette date.[/yellow]")

def run_application():
    extractor = ApiDataExtractor()
    mapper = RecordMapper()
    data_service = WeatherDataService(extractor, mapper)

    station_queue = StationQueue()
    for station_name in Configuration.STATION_URLS.keys():
        station_queue.enqueue(station_name)

    initial_station = station_queue.dequeue()
    station_queue.enqueue(initial_station) 
    station_id = initial_station
    
    chosen_date = datetime.now()
    
    while True:
        display_main_menu()

        if station_id:
            console.print(f"Station : {station_id}")
            console.print(f"Date : {chosen_date.strftime('%Y-%m-%d')}")
            
            station_data = data_service.get_weather_data_for_station_and_date(chosen_date, station_id)
            display_weather_data(station_data, station_id)

        choice = console.input("[bold yellow]Action (1: Choisir station, 2: Actualiser, 3: Station suivante, 4: Quitter) : [/bold yellow]")

        if choice == '1':
            station_id = get_station_choice(data_service)
            chosen_date = datetime.now()
        elif choice == '2':
            console.print("[green]Actualisation des données...[/green]")
            if station_id:
                chosen_date = datetime.now() 
                station_data = data_service.get_weather_data_for_station_and_date(chosen_date, station_id)
                display_weather_data(station_data, station_id)
            else:
                console.print("[red]Veuillez choisir une station avant d'actualiser.[/red]")
        elif choice == '3':
            if not station_queue.is_empty():
                station_queue.enqueue(station_id) 
                station_id = station_queue.dequeue() 
                console.print(f"[green]Passage à la station suivante : {station_id}[/green]")
                chosen_date = datetime.now() 
            else:
                console.print("[red]La file des stations est vide.[/red]")
        elif choice == '4' or choice.lower() == 'q':
            console.print("[bold blue]Au revoir ![/bold blue]")
            break
        else:
            console.print("[red]Choix invalide. Veuillez réessayer.[/red]")

if __name__ == "__main__":
    run_application()
