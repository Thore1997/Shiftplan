import pandas as pd
from datetime import datetime, timedelta
import holidays

# Using Bavaria (BY) holidays
bank_holidays_ger = holidays.Germany(prov='BY')


def create_timetable_lecture_period(start_date_str, end_date_str):
    # Shift templates for Monday - Thursday
    shifts_mon_thu = [
        {"name": "Morning", "start": "09:00", "end": "11:15", "duration": 2.25},
        {"name": "Midday", "start": "12:15", "end": "14:00", "duration": 1.75},
        {"name": "Afternoon", "start": "14:00", "end": "15:30", "duration": 1.5},
        {"name": "Evening", "start": "15:30", "end": "17:30", "duration": 2.0}
    ]

    # Shift templates for Friday
    shifts_fri = [
        {"name": "Morning", "start": "09:00", "end": "11:15", "duration": 2.25},
        {"name": "Midday", "start": "12:15", "end": "14:00", "duration": 1.75},
        {"name": "Afternoon", "start": "14:00", "end": "15:00", "duration": 1.0}
    ]

    # Convert date strings using DD.MM.YYYY
    start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
    end_date = datetime.strptime(end_date_str, "%d.%m.%Y")

    schedule_list = []
    current_day = start_date

    while current_day <= end_date:
        if current_day in bank_holidays_ger:
            print(f"Skipping {current_day.strftime('%d.%m.%Y')} - Reason: {bank_holidays_ger.get(current_day)}")
            current_day += timedelta(days=1)
            continue

        weekday_idx = current_day.weekday()
        day_name = current_day.strftime("%A")
        date_str = current_day.strftime("%d.%m.%Y")

        if weekday_idx <= 4:
            templates = shifts_mon_thu if weekday_idx <= 3 else shifts_fri

            for s in templates:
                shift_entry = s.copy()
                shift_entry["date"] = date_str
                shift_entry["weekday"] = day_name
                # Unique ID for optimization logic
                shift_entry["shift_id"] = f"{date_str}_{s['name']}"
                schedule_list.append(shift_entry)

        current_day += timedelta(days=1)

    df_timetable_lectrue_period = pd.DataFrame(schedule_list)
    return df_timetable_lectrue_period


def create_timetabl_semester_break(start_date_str, end_date_str):

    shifts_mon_fri = [
        {"name": "Morning", "start": "09:00", "end": "11:15", "duration": 2.25},
        {"name": "Midday", "start": "12:15", "end": "14:00", "duration": 1.75},
        {"name": "Afternoon", "start": "14:00", "end": "15:00", "duration": 1.0},
    ]

    # Convert date strings using DD.MM.YYYY
    start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
    end_date = datetime.strptime(end_date_str, "%d.%m.%Y")

    schedule_list = []
    current_day = start_date

    while current_day <= end_date:
        if current_day in bank_holidays_ger:
            print(f"Skipping {current_day.strftime('%d.%m.%Y')} - Reason: {bank_holidays_ger.get(current_day)}")
            current_day += timedelta(days=1)
            continue

        weekday_idx = current_day.weekday()
        day_name = current_day.strftime("%A")
        date_str = current_day.strftime("%d.%m.%Y")


def create_timetable_transistion(start_date_str, end_date_str):
    shifts_mon_thu = [
        {"name": "Morning", "start": "09:00", "end": "11:15", "duration": 2.25},
        {"name": "Midday", "start": "12:15", "end": "14:00", "duration": 1.75},
        {"name": "Afternoon", "start": "14:00", "end": "15:30", "duration": 1.5},
        {"name": "Evening", "start": "15:30", "end": "17:30", "duration": 2.0}
    ]

    # Shift templates for Friday
    shifts_fri = [
        {"name": "Morning", "start": "09:00", "end": "11:15", "duration": 2.25},
        {"name": "Midday", "start": "12:15", "end": "14:00", "duration": 1.75},
        {"name": "Afternoon", "start": "14:00", "end": "15:00", "duration": 1.0}
    ]

    # Convert date strings using DD.MM.YYYY
    start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
    end_date = datetime.strptime(end_date_str, "%d.%m.%Y")



if __name__ == "__main__":
    # Example call with original date format
    df_result = Timetable("06.04.2026", "10.04.2026")

    if not df_result.empty:
        print(df_result.head())
        df_result.to_csv("empty_timetable.csv", index=False, sep=";", encoding="utf-8-sig")
