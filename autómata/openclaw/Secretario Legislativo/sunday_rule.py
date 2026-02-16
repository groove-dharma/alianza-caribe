import argparse
from datetime import datetime, timedelta
import pytz
import sys

def calculate_end_time(start_iso, hours_to_add):
    # Zona horaria estricta según LODL-01
    tz = pytz.timezone('America/Caracas')
    
    # 1. SANITIZACIÓN DE ENTRADA
    # Elimina espacios o saltos de línea basura que vengan del comando anterior
    if start_iso:
        start_iso = start_iso.strip()

    # Parsear el tiempo de inicio
    if start_iso == "now" or not start_iso:
        current_dt = datetime.now(tz)
    else:
        try:
            # Limpieza estándar de ISO (Z -> +00:00) para compatibilidad
            clean_iso = start_iso.replace('Z', '+00:00')
            current_dt = datetime.fromisoformat(clean_iso).astimezone(tz)
        except ValueError as e:
            sys.stderr.write(f"Error parsing date input: {start_iso} -> {e}")
            sys.exit(1)

    remaining_hours = hours_to_add

    # 2. LÓGICA DEL AXIOMA DEL DOMINGO
    # Avanzamos hora por hora. Si caemos en domingo, el contador de "horas restantes" se pausa.
    # El tiempo real avanza, pero el "tiempo procesal" no.
    while remaining_hours > 0:
        current_dt += timedelta(hours=1)
        
        # 6 representa Domingo en Python (Lunes=0, Domingo=6)
        if current_dt.weekday() != 6:
            remaining_hours -= 1
        # Si ES domingo, el bucle continúa (avanza el reloj real) 
        # pero 'remaining_hours' NO disminuye.
            
    return current_dt.isoformat()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="now")
    parser.add_argument("--hours", type=int, required=True)
    args = parser.parse_args()
    
    try:
        result = calculate_end_time(args.start, args.hours)
        # 3. SANITIZACIÓN DE SALIDA (CRÍTICO)
        # end="" evita que Python agregue un \n invisible al final,
        # lo cual rompería el JSON del cron si el agente captura este output.
        print(result, end="")
    except Exception as e:
        sys.stderr.write(f"Error in calculation: {e}")
        sys.exit(1)