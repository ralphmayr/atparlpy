"""Example usage for the atparlpy wrappers."""

from pathlib import Path
from pprint import pprint
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from atparlpy import CommitteeReports, Motions, Inquiries, Resolutions, Parliamentarians, PlenarySessions


def main() -> None:
    # Beispiel: Alle Ausschussberichte im Nationalrat in der XXV. Gesetzgebungsperiode zum Thema Arbeit
    reports = CommitteeReports(nrbr="NR", gp_code="XXV", themen="Arbeit").AsList()
    print(f"{len(reports)} Ausschussberichte gefunden.")
    if reports:
        # Beispiel: Beschreibung des ersten gefundenen Ausschussberichts
        details = reports[0].GetDetails()
        if details.content:
            print(f"  Beschreibung des ersten Ausschussberichts: {details.content['description']}")

        # Beispiel: Einbringer des ersten gefundenen Ausschussberichts
        if details.names:
            initiators = list(filter(lambda n: n.funktext == 'Eingebracht von', details.names))
            initiator_names = ', '.join(map(lambda n: n.name, initiators))
            print(f"  Einbringer des ersten Ausschussberichts: {initiator_names}")

    # Beispiel: Abfrage nach allen Anträgen im Nationalrat während der XXVII. GP zum Thema Arbeit
    motions = Motions(gp_code="XXVII").nrbr("NR").themen(["Arbeit"]).AsList()
    print(f"{len(motions)} Anträge gefunden.")

    # Beispiel: Abfrage nach allen Anträgen im Nationalrat während der 28. GP denen die Grünen zugestimmt haben
    motions = Motions(gp=28).nrbr("NR").AsList()
    motions = list(filter(lambda m: m.dafuer != None and 'GRÜNE' in m.dafuer, motions))

    # Beispiel: Abfrage nach allen Beschlüssen im Nationalrat während der 25. GP zum Thema Kultur
    resolutions = Resolutions().nrbr("NR").gp_code("XXV").themen("Kultur").AsList()
    print(f"{len(resolutions)} Beschlüsse des Nationalrats gefunden.")

    # Beispiel: Abfrage nach allen parlamentarischen Anfragen im Nationalrat während der XXVIII. GP zum Thema Arbeit oder Bildung
    inquiries = Inquiries(gp=28, nrbr="NR").themen(["Arbeit", "Bildung"]).AsList()
    print(f"{len(inquiries)} Anfragen im Nationalrat gefunden.")
    df = Inquiries(gp=28, nrbr="NR").AsDataFrame()
    print(df['status'].value_counts())

    # Beispiel: Abfrage nach allen Anfragen im Bundesrat während der 27. GP
    inquiries = Inquiries(gp=27, nrbr="BR").AsList()
    print(f"{len(inquiries)} Anfragen im Bundesrat gefunden.")

    # Beispiel: Abfrage nach allen aktuellen Abgeordneten zum Nationalrat
    members_of_parliament = Parliamentarians(nrbr="NR").AsList()
    print(f"{len(members_of_parliament)} Abgeordnete zum Nationalrat gefunden.")
    df = Parliamentarians(nrbr="NR").AsDataFrame()
    print(df['sort_wp'].value_counts())

    # Beispiel: Abfrage nach dem aktuellen Präsidenten des Nationalrats
    president = Parliamentarians(nrbr="NR").funk("1PNR").AsList()[0]
    print(f"Präsident des NR: {president.name}")

    person = president.GetDetails()
    print(f"Link zum Foto: {person.image}")
    print(f"Sitzplatz: {person.sitzplatz}")

    # Beispiel: Abfrage nach allen aktuellen Mitgliedern des Bundesrats
    members_of_the_national_council = Parliamentarians(nrbr="BR").AsList()
    print(f"{len(members_of_the_national_council)} Mitglieder des Bundesrats gefunden.")

    # Beispiel: Abfrage nach allen Plenarsitzungen des Nationalrats in der 28. GP
    sessions = PlenarySessions(nrbr="NR",gp=28).AsList()
    print(f"{len(sessions)} Sitzungen des Nationalrats gefunden")

if __name__ == "__main__":
    main()
