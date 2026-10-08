import pulp import LpVariable as pl
import pandas as pd
from employee_config import get_employee_df
from timetable_config import create_timetable_lecture_period


def optimize_schedule(df_employees, df_timetable):
    # Initialize the optimization problem
    prob = pl.LpProblem("Schedule_Optimization", pl.LpMinimize)

    # IDs
    employee_ids = df_employees.index.tolist()
    shift_ids = df_timetable['shift_id'].tolist()

    # Decision Variables: x(m, s) is 1 if employee m is assigned to shift s
    x = pl.LpVariable.dicts("assign",
                              ((m, s) for m in employee_ids for s in shift_ids),
                              cat=pl.LpBinary)

    # 1. Constraint: Each shift must have exactly 1 person assigned
    for s in shift_ids:
        prob += pl.lpSum([x[(m, s)] for m in employee_ids]) == 1

    # 2. Constraint: Employee total hours must not exceed their maximum hours
    for m in employee_ids:
        max_h = df_employees.at[m, 'Hours']

        # Calculate total hours assigned to this employee
        planned_hours = pl.lpSum([
            x[(m, s)] * df_timetable.loc[df_timetable['shift_id'] == s, 'duration'].values[0]
            for s in shift_ids
        ])
        prob += planned_hours <= max_h

    # 3. Solve
    prob.solve(pl.PULP_CBC_CMD(msg=0))

    # 4. Check results and return the updated dataframe
    if pl.LpStatus[prob.status] == 'Optimal':
        print("\n--- Working Hours Summary ---")

        for m in employee_ids:
            limit = df_employees.at[m, 'Hours']

            # Calculate actual assigned hours from solver results
            actual_hours = 0
            for s in shift_ids:
                if pl.value(x[(m, s)]) == 1:
                    duration = df_timetable.loc[df_timetable['shift_id'] == s, 'duration'].values[0]
                    actual_hours += duration

            remaining = limit - actual_hours
            employee_name = df_employees.at[m, 'Name'] if 'Name' in df_employees.columns else m

            print(
                f"Employee: {employee_name:<15} | Limit: {limit:>5}h | Planned: {actual_hours:>5}h | Remainder: {remaining:>5}h")

        print("-" * 50)

        # Map results back to the timetable
        assignments = {}
        for s in shift_ids:
            for m in employee_ids:
                if pl.value(x[(m, s)]) == 1:
                    assignments[s] = m

        # Create new column for assigned employees
        df_timetable['Employee_ID'] = df_timetable['shift_id'].map(assignments)
        return df_timetable

    else:
        print("No optimal solution found! Perhaps not enough employees for the required shifts?")
        return None


# --- EXECUTION ---
if __name__ == "__main__":
    # Ensure these filenames and parameters match your setup
    df_employees = get_employee_df("Employees.csv")
    df_timetable = (create_timetable("2026-04-06", "2026-04-10"))

    # Clean column names
    df_employees.columns = df_employees.columns.str.strip()
    df_timetable.columns = df_timetable.columns.str.strip()

    final_schedule = optimize_schedule(df_employees, df_timetable)

    if final_schedule is not None:
        # Displaying key columns (Date, Start, End, Employee)
        print(final_schedule[['date', 'start', 'end', 'Employee_ID']])
        final_schedule.to_csv("Schedule_Final.csv", sep=';', index=False, encoding='utf-8-sig')