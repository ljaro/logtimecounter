#!/usr/bin/env python3

import re
import os
import argparse
from datetime import datetime, timedelta

def parse_connection_time(time_str):
    """Parse a time string in the format HH:MM:SS.mmm and return a timedelta object."""
    hours, minutes, seconds = map(float, time_str.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def sum_connection_times_from_logs(start_date_str):
    """Sum the connection times from log files starting from a specific date."""
    # Parse the start date
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    # Initialize total connection time
    total_connection_time = timedelta()

    # Iterate over the files in the current directory
    for file_name in os.listdir('.'):
        # Check if the file name matches the pattern and the date is >= start_date
        match = re.match(r"(\d{4}-\d{2}-\d{2})#\d{2}-\d{2}-\d{2}\.txt", file_name)
        if match:
            file_date_str = match.group(1)
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            if file_date >= start_date:
                # Process the file
                with open(file_name, 'r') as file:
                    for line in file:
                        if "Connection time:" in line:
                            time_str = line.split("Connection time:")[1].strip()
                            connection_time = parse_connection_time(time_str)
                            print(f"Found connection time {connection_time} in file {file_name}")
                            total_connection_time += connection_time
    
    return total_connection_time

def get_start_of_week():
    """Get the date of the Monday of the current week."""
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    return start_of_week.strftime('%Y-%m-%d')

def main():
    parser = argparse.ArgumentParser(description="Sum connection times from log files starting from a specific date.")
    parser.add_argument('start_date', nargs='?', default=None, type=str, help="The start date in the format YYYY-MM-DD")
    
    args = parser.parse_args()
    
    # Use the provided start date or calculate the start of the current week
    start_date_str = args.start_date if args.start_date else get_start_of_week()
    
    print(f"Using start date: {start_date_str}")
    total_time = sum_connection_times_from_logs(start_date_str)
    print(f"\nTotal connection time from {start_date_str}: {total_time}")

if __name__ == "__main__":
    main()
