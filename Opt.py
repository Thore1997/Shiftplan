import pulp
import pandas as pd
from Mitarbeiter_config import get_mitarbeiter_df
from Timetable_confiq import Timetable


def opt_plan(df_MA, df_Plan):
    prob = pulp.LpProblem("Dienstplan_Optimierung", pulp.LpMinimize)

    # IDs
    ma_ids = df_MA.index.tolist()
    schicht_ids = df_Plan['schicht_id'].tolist()

    # Decision Variables
    x = pulp.LpVariable.dicts("x",
                              ((m, s) for m in ma_ids for s in schicht_ids),
                              cat=pulp.LpBinary)

    # 3. Nebenbedingung: Jede Schicht muss genau 1 Person haben
    for s in schicht_ids:
        prob += pulp.lpSum([x[(m, s)] for m in ma_ids]) >= 2

    #Constraints
        for m in ma_ids:
            max_h = df_MA.at[m, 'Hours']

            stunden_im_plan = pulp.lpSum([
                x[(m, s)] * df_Plan.loc[df_Plan['schicht_id'] == s, 'dauer'].values[0]
                for s in schicht_ids
            ])
            prob += stunden_im_plan <= max_h

        #for m in ma_ids:
        #    stunden_im_plan = pulp.lpSum([
        #        x[(m,s)] * df_Plan.loc[df_Plan['schicht_id'] == s, 'Hours'].values(0)
        #        for s in schicht_ids
        #    ])

        #    max_h = df_MA.at[m, 'Hours']
        #    prob += stunden_im_plan == max_h

    # 5. Lösen
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # 6. Ergebnisse in den Schicht-Dataframe zurückschreiben
    if pulp.LpStatus[prob.status] == 'Optimal':

        if pulp.LpStatus[prob.status] == 'Optimal':
            print("\n--- Zusammenfassung der Arbeitsstunden ---")

            for m in ma_ids:
                # 1. Das Limit aus dem DataFrame holen
                limit = df_MA.at[m, 'Hours']

                # 2. Die tatsächlich zugeteilten Stunden berechnen
                geplante_stunden = 0
                for s in schicht_ids:
                    # Wenn der "Schalter" für diese Kombi auf 1 steht
                    if pulp.value(x[(m, s)]) == 1:
                        # Dauer der Schicht aus dem Plan-DF holen
                        dauer = df_Plan.loc[df_Plan['schicht_id'] == s, 'dauer'].values[0]
                        geplante_stunden += dauer

                # 3. Differenz berechnen
                rest = limit - geplante_stunden

                # 4. In der Konsole ausgeben
                # Wir holen uns den Namen des MA (falls vorhanden), sonst die ID
                ma_name = df_MA.at[m, 'Name'] if 'Name' in df_MA.columns else m
                print(
                    f"Mitarbeiter: {ma_name:<15} | Limit: {limit:>5}h | Geplant: {geplante_stunden:>5}h | Rest: {rest:>5}h")

            print("-" * 50)

        zuordnungen = {}
        for s in schicht_ids:
            for m in ma_ids:
                if pulp.value(x[(m, s)]) == 1:
                    zuordnungen[s] = m

        # Neue Spalte im Dataframe erstellen
        df_Plan['Mitarbeiter_ID'] = df_Plan['schicht_id'].map(zuordnungen)
        return df_Plan
    else:
        print("Keine optimale Lösung gefunden! Vielleicht zu wenige Mitarbeiter für zu viele Schichten?")
        return None


# --- START ---
if __name__ == "__main__":
    df_MA = get_mitarbeiter_df("Mitarbeiter.csv")
    df_Plan = Timetable("2026-04-06", "2026-04-10")

    df_MA.columns = df_MA.columns.str.strip()
    df_Plan.columns = df_Plan.columns.str.strip()

    fertiger_plan = opt_plan(df_MA, df_Plan)

    if fertiger_plan is not None:
        print(fertiger_plan[['datum', 'start', 'ende', 'Mitarbeiter_ID']])
        fertiger_plan.to_csv("Dienstplan_Fertig.csv", sep=';', index=False)