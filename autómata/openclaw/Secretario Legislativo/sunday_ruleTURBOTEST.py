import argparse
from datetime import datetime, timedelta
import pytz

def calculate_end_time(start_iso, hours_to_add):
    tz = pytz.timezone('America/Caracas')
    
    # Parsear el tiempo de inicio
    if start_iso == "now":
        start_dt = datetime.now(tz)
    else:
        # Limpieza básica de ISO para Python
        start_dt = datetime.fromisoformat(start_iso.replace('Z', '+00:00')).astimezone(tz)

    # MAPEO TURBO:
    # 24h (Fases I y III) -> 5 minutos
    # 48h (Fase II)       -> 10 minutos
    minutos = 5 if hours_to_add == 24 else 10
    
    final_dt = start_dt + timedelta(minutes=minutos)
    
    # Retornamos el ISO para que el flag --at del cron lo entienda
    return final_dt.isoformat()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="now")
    parser.add_argument("--hours", type=int, required=True)
    args = parser.parse_args()
    
    print(calculate_end_time(args.start, args.hours))