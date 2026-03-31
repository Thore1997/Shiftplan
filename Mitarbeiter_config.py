import pandas as pd
import io


def get_mitarbeiter_df(dateipfad="Mitarbeiter.csv"):
    # Wir lesen die Datei erst als rohen Text, um sicherzugehen
    with open(dateipfad, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Wir entfernen alle Anführungszeichen manuell, falls welche da sind
    content = content.replace('"', '')

    # Jetzt lesen wir den bereinigten Text mit dem Semikolon-Trenner
    df = pd.read_csv(io.StringIO(content), sep=';')

    # Spaltennamen säubern
    df.columns = df.columns.str.strip()

    # Index setzen
    if 'ID' in df.columns:
        df.set_index('ID', inplace=True)
        # WICHTIG: Index zu String machen, damit PuLP keine Typ-Fehler macht
        df.index = df.index.astype(str)

    return df