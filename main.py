from employee_config import get_employee_df
#from datetime import time
from opt import optimize_schedule
from timetable_config import (
    create_timetable_lecture_period,
    create_timetable_semester_break,
    create_timetable_transition,
    )


def select_phase(start_date: str, end_date: str) -> pd.DataFrame:
    print("=" * 45)
    print(f"\nWelcome to Ephemereia - Shift Plan Optimization")
    print("=" * 45)

    print(f"What would you like to do?")
    print("[1] Generate a new timetable template (empty)")
    print("[2] Optimize shift plan")
    choice = input("Select mode (1 or 2):").strip()

    try:
        if choice == "1":
            print("\nSelect period type for the template:")
            print("[1] Lecture Period")
            print("[2] Semester Break")
            print("[3] Transition Period")
            phase_choice = input("Choice (Default: 1):").strip()

            start_date = input("Start Date").strip()
            end_date = input("End Date").strip()

            if phase_choice == "1":
                df_template = create_timetable_lecture_period(start_date, end_date)
            elif phase_choice == "2":
                df_template = create_timetable_semester_break(start_date, end_date)
            elif phase_choice == "3":
                df_template = create_timetable_transistion(start_date, end_date)
            else:
                raise ValueError(f"Invalid phase choice: {phase_choice}")

            df_template.to_csv(output_name; sep=";", index=False, encoding="utf-8-sig")
            print(f"\nDone! Template with {len(df_template)} shifts saved as: {output_name}")







    # 1. CONSOLE QUERIES
    try:
        file_path = input("Employee CSV file (Default: Mitarbeiter.csv): ") or "Mitarbeiter.csv"

        start_date = input("Start Date: ")
        end_date = input("End Date: ")

        output_name = input("Schedule output name: ") or "Schedule_Output.csv"

        # Load employee data
        df_employees = get_employee_df(file_path)

        print(f"Generating shift plan from {start_date} to {end_date}...")
        create_timetable = create_timetable_lecture_period(start_date, end_date)

        print("Starting optimization...")
        final_schedule = optimize_schedule(df_employees, create_timetable)

        if final_schedule is not None:
            final_schedule.to_csv(output_name, sep=';', index=False, encoding='utf-8-sig')
            print(f"Done! File saved as: {output_name}")
        else:
            print("\nError: Optimization failed.")

    except Exception as e:
        print(f"\nTerminated due to error: {e}")


if __name__ == "__main__":
    main()

