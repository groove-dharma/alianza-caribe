import argparse
from datetime import datetime, timedelta
import pytz

def calculate_end_time(start_iso, hours_to_add):
    tz = pytz.timezone('America/Caracas')
    
    # Parse start time and ensure it's in VET
    if start_iso == "now":
        start_dt = datetime.now(tz)
    else:
        start_dt = datetime.fromisoformat(start_iso.replace('Z', '+00:00')).astimezone(tz)

    current_dt = start_dt
    remaining_hours = hours_to_add

    # Progress hour by hour to handle the Sunday pause correctly
    while remaining_hours > 0:
        current_dt += timedelta(hours=1)
        # If it's Sunday, we don't count the hour
        if current_dt.weekday() != 6:  # 6 is Sunday
            remaining_hours -= 1
            
    return current_dt.isoformat()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="now")
    parser.add_argument("--hours", type=int, required=True)
    args = parser.parse_args()
    
    print(calculate_end_time(args.start, args.hours))