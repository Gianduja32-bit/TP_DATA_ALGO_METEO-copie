import inquirer
from rich.console import Console
from rich.panel import Panel
from datetime import datetime

from weather_cli.api_manager import ApiDataExtractor, RecordMapper, Configuration
from weather_cli.services.data_service import WeatherDataService
from weather_cli.services.display_service import StationDisplayDecorator, RecordDisplayDecorator
from weather_cli.utils.validators import validate_date_range, validate_station_name

console = Console()

def display_main_menu():
    console.print(Panel("[bold green]=== APPLICATION MÉTÉO TOULOUSAINE ===[/bold green]"))
    console.print("1. Choisir une station")
    console.print("2. Actualiser les données")
    console.print("3. Quitter")
    console.print("-" * 37)

def get_station_choice(data_service: WeatherDataService) -> str:
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

def run_application():
    extractor = ApiDataExtractor(Configuration.BASE_URL)
    mapper = RecordMapper()
    data_service = WeatherDataService(extractor, mapper)

    station_name = None
    # La date est maintenant toujours la date du jour
    chosen_date = datetime.now()
    
    while True:
        display_main_menu()

        if station_name:
            console.print(f"Station : {station_name}")
            console.print(f"Date : {chosen_date.strftime('%Y-%m-%d')}")
            
            station_data = data_service.get_weather_data_for_station_and_date(chosen_date, station_name)
            if station_data and station_data.mesures:
                station_decorator = StationDisplayDecorator(station_data)
                station_decorator.show()
                for record in station_data.mesures:
                    record_decorator = RecordDisplayDecorator(record)
                    record_decorator.show()
            else:
                console.print("[yellow]Aucune donnée météo disponible pour cette station et cette date.[/yellow]")

        choice = console.input("[bold yellow]Action (1: Choisir station, 2: Actualiser, 3: Quitter) : [/bold yellow]")

        if choice == '1':
            station_name = get_station_choice(data_service)
            chosen_date = datetime.now() # Actualiser la date du jour lors du choix de la station
        elif choice == '2':
            console.print("[green]Actualisation des données...[/green]")
            if station_name:
                chosen_date = datetime.now() # Actualiser la date du jour lors de l'actualisation
                station_data = data_service.get_weather_data_for_station_and_date(chosen_date, station_name)
                if station_data and station_data.mesures:
                    station_decorator = StationDisplayDecorator(station_data)
                    station_decorator.show()
                    for record in station_data.mesures:
                        record_decorator = RecordDisplayDecorator(record)
                        record_decorator.show()
                else:
                    console.print("[yellow]Aucune donnée météo disponible pour cette station et cette date après actualisation.[/yellow]")
            else:
                console.print("[red]Veuillez choisir une station avant d'actualiser.[/red]")
        elif choice == '3' or choice.lower() == 'q': # Permettre de quitter avec '3' ou 'q'
            console.print("[bold blue]Au revoir ![/bold blue]")
            break
        else:
            console.print("[red]Choix invalide. Veuillez réessayer.[/red]")

if __name__ == "__main__":
    run_application()
