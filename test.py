from Mitarbeiter_config import get_mitarbeiter_df

with open("Mitarbeiter.csv", "r", encoding="utf-8-sig") as f:
    for i in range(5): # Zeige die ersten 3 Zeilen
        print(f"Zeile {i}: '{f.readline().strip()}'")