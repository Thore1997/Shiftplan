from employee_config import get_employee_df
from timetable_config import create_timetable
from opt import optimize_schedule


def main():
    print("=" * 30)
    print("  Welcome to Ephemereia - Shift Plan Optimization  ")
    print("=" * 30)

    print("What would you like to do?")
    print("[1] Export (Generate a new template)")
    print("[2] Import (Load and optimize shift plan)")

    # 1. CONSOLE QUERIES
    try:
        file_path = input("Employee CSV file (Default: Mitarbeiter.csv): ") or "Mitarbeiter.csv"

        start_date = input("Start Date: ")
        end_date = input("End Date: ")

        output_name = input("Schedule output name: ") or "Schedule_Output.csv"

        # Load employee data
        df_employees = get_employee_df(file_path)

        print(f"Generating shift plan from {start_date} to {end_date}...")
        df_timetable_lectrue_period = create_timetable(start_date, end_date)

        print("Starting optimization...")
        final_schedule = optimize_schedule(df_employees, df_timetable_lectrue_period)

        if final_schedule is not None:
            final_schedule.to_csv(output_name, sep=';', index=False, encoding='utf-8-sig')
            print(f"Done! File saved as: {output_name}")
        else:
            print("\nError: Optimization failed.")

    except Exception as e:
        print(f"\nTerminated due to error: {e}")


if __name__ == "__main__":
    main()

