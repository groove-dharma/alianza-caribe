import argparse
from datetime import datetime, timedelta
import pytz
import sys

def calculate_end_time(start_iso, hours_to_add):
    tz = pytz.timezone('America/Caracas')
    
    # 1. SANITIZACIÓN DE ENTRADA (Vital para el encadenamiento)
    start_iso = start_iso.strip() 

    # Parsear el tiempo de inicio
    if start_iso == "now":
        start_dt = datetime.now(tz)
    else:
        try:
            # Limpieza básica de ISO para Python
            clean_iso = start_iso.replace('Z', '+00:00')
            start_dt = datetime.fromisoformat(clean_iso).astimezone(tz)
        except ValueError as e:
            # Si falla, imprimimos error a stderr para no ensuciar el stdout
            sys.stderr.write(f"Error parsing date: {e}")
            sys.exit(1)

    # MAPEO TURBO:
    # 24h -> 5 minutos
    # 48h -> 10 minutos
    minutos = 5 if hours_to_add == 24 else 10
    
    final_dt = start_dt + timedelta(minutes=minutos)
    
    # Retornamos el ISO
    return final_dt.isoformat()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="now")
    parser.add_argument("--hours", type=int, required=True)
    args = parser.parse_args()
    
    # 2. SANITIZACIÓN DE SALIDA (Vital para el JSON)
    # end="" evita el salto de línea (\n) que rompe los JSONs
    print(calculate_end_time(args.start, args.hours), end="")