import time
import math
from geopy.geocoders import Nominatim
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich.console import Console

# --- 1. KONSTANTEN & FAKTEN (Die Wissenschaft) ---
# Quellen: NASA, Wikipedia Astrophysics Data
# Alle Geschwindigkeiten in km/s (Kilometer pro Sekunde)

# Geschwindigkeit der Erde um die Sonne (Durchschnitt)
# Quelle: NASA
SPEED_ORBIT_SUN_KM_S = 29.78 

# Geschwindigkeit des Sonnensystems um das galaktische Zentrum
# Quelle: NASA / IAU
SPEED_GALACTIC_KM_S = 220.0

# Äquatoriale Rotationsgeschwindigkeit der Erde
# Umfang am Äquator ca. 40.075 km / 24h
SPEED_ROTATION_EQUATOR_KM_S = 0.4651

# --- 2. LOGIK KLASSE ---

class CosmicCalculator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="cosmic_odometer_v1")
        self.latitude = 0.0
        self.location_name = "Unbekannt"
        self.local_rotation_speed = 0.0
        self.start_time = time.time()

    def set_location(self, city_name):
        """Ermittelt Koordinaten und berechnet lokale Rotationsgeschwindigkeit"""
        try:
            location = self.geolocator.geocode(city_name)
            if location:
                self.latitude = location.latitude
                self.location_name = location.address.split(",")[0] # Nur Stadtname
                
                # Physik: Geschwindigkeit = Äquatorgeschwindigkeit * cos(Breitengrad)
                # Wir müssen Grad in Radiant umrechnen für math.cos
                rad = math.radians(abs(self.latitude))
                self.local_rotation_speed = SPEED_ROTATION_EQUATOR_KM_S * math.cos(rad)
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_distances(self):
        """Berechnet die zurückgelegte Strecke seit Start des Programms"""
        elapsed_seconds = time.time() - self.start_time
        
        dist_rotation = self.local_rotation_speed * elapsed_seconds
        dist_orbit = SPEED_ORBIT_SUN_KM_S * elapsed_seconds
        dist_galaxy = SPEED_GALACTIC_KM_S * elapsed_seconds
        
        total_km = dist_rotation + dist_orbit + dist_galaxy
        
        return {
            "rotation": dist_rotation,
            "orbit": dist_orbit,
            "galaxy": dist_galaxy,
            "total": total_km,
            "elapsed": elapsed_seconds
        }

# --- 3. UI & DARSTELLUNG (Rich Library) ---

def generate_table(data, location, lat, speed_rot):
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Referenzrahmen", style="dim", width=25)
    table.add_column("Geschwindigkeit (km/s)", justify="right")
    table.add_column("Zurückgelegt (km)", justify="right", style="bold green")

    # Zeile 1: Erdrotation
    table.add_row(
        "Erdrotation (Lokal)", 
        f"{speed_rot:.4f} km/s", 
        f"{data['rotation']:.2f} km"
    )
    
    # Zeile 2: Orbit um Sonne
    table.add_row(
        "Orbit um Sonne", 
        f"{SPEED_ORBIT_SUN_KM_S:.2f} km/s", 
        f"{data['orbit']:.2f} km"
    )

    # Zeile 3: Galaktische Reise
    table.add_row(
        "Milchstraßen-Orbit", 
        f"{SPEED_GALACTIC_KM_S:.2f} km/s", 
        f"{data['galaxy']:.2f} km"
    )
    
    return table

def make_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    return layout

# --- 4. MAIN PROGRAMM ---

def main():
    console = Console()
    calc = CosmicCalculator()
    
    console.clear()
    console.print(Panel.fit("[bold cyan]🌌 The Cosmic Odometer[/bold cyan]\n[dim]Berechne deine Reise durch das Universum, während du sitzt.[/dim]"))
    
    city = console.input("\n[bold yellow]Bitte gib deine Stadt ein (z.B. Berlin, Munich): [/bold yellow]")
    
    with console.status(f"[bold green]Lokalisiere {city} und berechne Vektoren...[/bold green]"):
        success = calc.set_location(city)
        time.sleep(1.5) # Dramatische Pause für den User ;)

    if not success:
        console.print("[bold red]Fehler:[/bold red] Stadt nicht gefunden. Bitte Internet prüfen oder Schreibweise korrigieren.")
        return

    # Live Update Loop
    layout = make_layout()
    
    # Header setzen
    header_text = Text(f"📍 Standort: {calc.location_name} (Breitengrad: {calc.latitude:.4f}°)", style="bold white", justify="center")
    layout["header"].update(Panel(header_text, style="blue"))

    with Live(layout, refresh_per_second=10, screen=True) as live:
        while True:
            data = calc.get_distances()
            
            # Main Table Update
            table = generate_table(data, calc.location_name, calc.latitude, calc.local_rotation_speed)
            
            # Total Summary Panel
            summary = Align.center(
                f"\n[bold orange1]Gesamtstrecke seit Start:[/bold orange1]\n"
                f"[bold white size=24]{data['total']:,.2f} km[/bold white size=24]\n\n"
                f"[dim]Laufzeit: {data['elapsed']:.1f} sekunden[/dim]"
            )
            
            layout["main"].update(Panel(table, title="Echtzeit-Telemetrie"))
            layout["footer"].update(Panel(summary, style="green"))
            
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nReise beendet. Willkommen zurück auf dem Boden der Tatsachen.")
