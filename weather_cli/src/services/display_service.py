from abc import ABC, abstractmethod
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from weather_cli.src.domain.models import Station, Record

class DisplayDecorator(ABC):
    @abstractmethod
    def show(self):
        pass

class StationDisplayDecorator(DisplayDecorator):
    def __init__(self, station: Station):
        self.station = station
        self.console = Console()

    def show(self):
        self.console.print(Panel(f"[bold blue]Station : {self.station.nom}[/bold blue]"))

class RecordDisplayDecorator(DisplayDecorator):
    def __init__(self, record: Record):
        self.record = record
        self.console = Console()

    def show(self):
        table = Table(show_header=False, show_edge=False, show_lines=False, box=None)
        table.add_column(style="dim")
        table.add_column(justify="right")

        table.add_row("Température :", f"[bold]{self.record.temperature}°C[/bold]")
        table.add_row("Humidité :", f"[bold]{self.record.humidity}%[/bold]")
        table.add_row("Pression :", f"[bold]{self.record.pressure} hPa[/bold]")
        table.add_row("Heure :", f"[dim]{self.record.timestamp.strftime('%H:%M:%S')}[/dim]")
        self.console.print(table)
