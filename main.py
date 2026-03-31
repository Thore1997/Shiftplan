from Mitarbeiter_config import get_mitarbeiter_df
from Timetable_confiq import Timetable
from Opt import opt_plan


def main():
    print("=" * 30)
    print("  Erstelle Dienstplan  ")
    print("=" * 30)

    # 1. ABFRAGEN ÜBER DIE KONSOLE
    try:
        datei = input("CSV-Datei der Mitarbeiter (Standard: Mitarbeiter.csv): ") or "Mitarbeiter.csv"

        start = input("Start-Datum: ")
        ende = input("End-Datum: ")

        output_name = input("Name des Dienstplans: ") or "Dienstplan_Output.csv"


        df_ma = get_mitarbeiter_df(datei)

        print(f"Erstelle Schichtplan von {start} bis {ende}...")
        df_Plan = Timetable(start, ende)

        print("Starte  Optimierung")
        fertiger_plan = opt_plan(df_ma, df_Plan)


        if fertiger_plan is not None:
            fertiger_plan.to_csv(output_name, sep=';', index=False, encoding='utf-8-sig')
            print(f"Done! Datei gespeichert als: {output_name}")
        else:
            print("\nFehler: Optimierung fehlgeschlagen.")

    except Exception as e:
        print(f"\nAbbruch durch Fehler: {e}")


if __name__ == "__main__":
    main()