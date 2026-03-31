import pandas as pd
from datetime import datetime, timedelta
import holidays


bankdays_ger = holidays.Germany(prov='BY')
def Timetable (start_datum_str, end_datum_str):

    schichten_mo_do = [
        {"name": "Vormittag", "start": "09:00", "ende": "11:15", "dauer": 2.25},
        {"name": "Mittag", "start": "12:15", "ende": "14:00", "dauer": 1.75},
        {"name": "Nachmittag", "start": "14:00", "ende": "15:30", "dauer": 1.5},
        {"name": "Abend", "start": "15:30", "ende": "17:30", "dauer": 2.0}
    ]

    schichten_fr = [
        {"name": "Vormittag", "start": "09:00", "ende": "11:15", "dauer": 2.25},
        {"name": "Mittag", "start": "12:15", "ende": "14:00", "dauer": 1.75},
        {"name": "Nachmittag", "start": "14:00", "ende": "15:00", "dauer": 1.0}
    ]

    # Daten umwandeln
    start = datetime.strptime(start_datum_str, "%d.%m.%Y")
    ende = datetime.strptime(end_datum_str, "%d.%m.%Y")

    liste_df = []
    aktueller_tag = start

    # Schleife über den Zeitraum
    while aktueller_tag <= ende:
        if aktueller_tag in bankdays_ger:
            print(f"Skipping {aktueller_tag.strftime('%d.%m.%Y')} - Grund: {bankdays_ger.get(aktueller_tag)}")
            aktueller_tag += timedelta(days=1)
            continue

        wochentag = aktueller_tag.weekday()  # 0=Mo, 4=Fr
        tag_name = aktueller_tag.strftime("%A")  # z.B. "Monday"
        datum_iso = aktueller_tag.strftime("%d.%m.%Y")

        # Nur Mo-Fr (Wochentag 0 bis 4)
        if wochentag <= 4:
            # Entscheidung: Mo-Do oder Fr?
            vorlagen = schichten_mo_do if wochentag <= 3 else schichten_fr

            for s in vorlagen:
                schicht_eintrag = s.copy()
                schicht_eintrag["datum"] = datum_iso
                schicht_eintrag["wochentag"] = tag_name
                # Eindeutige ID für die Optimierung später
                schicht_eintrag["schicht_id"] = f"{datum_iso}_{s['name']}"
                liste_df.append(schicht_eintrag)

        aktueller_tag += timedelta(days=1)

    # DataFrame erstellen
    df_Plan = pd.DataFrame(liste_df)
    return df_Plan


# Beispiel-Aufruf und Speichern als CSV
if __name__ == "__main__":
    df_Plan = Timetable("2026-04-06", "2026-04-10")  # Eine Beispielwoche
    df.to_csv("leerer_schichtplan.csv", index=False, sep=";", encoding="utf-8-sig")
