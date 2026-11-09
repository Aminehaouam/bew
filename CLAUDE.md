# Projekt: Bewerbungen Amine Haouam (Ausbildung Elektroniker, Deutschland)

Ziel: Für Ausbildungsangebote (Bundesagentur für Arbeit Jobbörse, ganz Deutschland) je Firma einen angepassten Anschreiben-Text erzeugen, Seite 2 der Bewerbungsdatei `base.pdf` ersetzen und alles in eine Excel-Liste eintragen.
Berufe: Elektroniker für Betriebstechnik (aktuell bevorzugt) und Elektroniker für Energie- und Gebäudetechnik.
Region: ganz Deutschland. Ziel: 50 Firmen MIT E-Mail-Adresse.

## Ablauf
1. Anzeigen suchen (BA-API `https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs`, Header `X-API-Key: jobboerse-jobsuche`, `angebotsart=4` = Ausbildung, `was=Elektroniker`; Details über `/pc/v4/jobdetails/{base64(refnr)}`). Nur Anzeigen mit sichtbarer E-Mail im Text oder auf der Firmen-Impressum-Seite nehmen. Die Sicherheitsfrage der Jobbörse NICHT umgehen.
2. Je Firma ein JSON-Eintrag (Muster: `firms.json`, `bt.json`): name, file (Kurzname für Dateinamen), addr (4 Zeilen), date, betreff, anrede, p1, beruf (nur bei Betriebstechnik: "Elektroniker für Betriebstechnik").
3. `python assemble.py liste.json out` erzeugt `out/Amine_Haouam_Ausbildung_Elektroniker_<firma>.pdf` (nur Seite 2 wird ersetzt, alle anderen Seiten bleiben).
4. Excel-Liste `Bewerbungsliste.xlsx`: Firma, Ansprechpartner, E-Mail, Adresse, Beginn, Ort, Link, Datei, Hinweis. Firmen ohne verwertbare Kontaktdaten auf ein eigenes Blatt.
E-Mails werden NICHT von Claude verschickt, Amine sendet selbst.

## Regeln für den Anschreiben-Teil (nur diese Teile werden angepasst)
Adressblock: Firma / `z. Hd. Herrn|Frau Nachname` (oder `Personalabteilung`) / Straße / PLZ Ort (immer genau 4 Zeilen).
Datum: `Tebessa, TT.MM.JJJJ` (Tagesdatum, Absprache mit Amine falls er für morgen schreibt).
Betreff (fett): `Bewerbung um eine Ausbildung zum Elektroniker für Energie- und Gebäudetechnik (m/w/d)` plus `in <Standort> ab <Datum>`, wenn die Anzeige beides nennt.
Anrede: `Sehr geehrter Herr X,` / `Sehr geehrte Frau X,` / `Sehr geehrte Damen und Herren,` danach zwei Leerzeilen (Layout macht letter.py).
Erster Absatz (Vorlage): "bei Ihnen spricht mich besonders an, dass [ein echtes Firmendetail], deshalb möchte ich meine Ausbildung zum Elektroniker für Energie- und Gebäudetechnik gern in Ihrem Betrieb machen. [Ein Zusatzsatz zur Firma, mit Motivation verbunden]. Der Beruf verbindet Technik mit praktischer Arbeit, und genau das suche ich."
- Erstes Wort "bei" klein; sonst normale Rechtschreibung.
- Höchstens EIN echtes Firmendetail, nichts Erfundenes. Keine Gründungsjahre, Mitarbeiterzahlen, Statistiken, Firmengeschichte.
- Kein "Hiermit bewerbe ich mich", kein übertriebenes Lob, keine Aufzählungen.
- Deutsch B2-C1, einfach und kurz. Absatz höchstens 5 Zeilen.
- Wenn kein sinnvolles Firmendetail vorhanden: "Der Beruf des Elektronikers für Energie- und Gebäudetechnik verbindet Technik mit praktischer Arbeit, und genau das suche ich. Deshalb möchte ich meine Ausbildung gern bei Ihnen machen."
- Kein B2-Sprachsatz im ersten Absatz.
Absätze 2-4, Gruß und Unterschrift bleiben unverändert (stehen in letter.py).

## Bereits bearbeitet / nicht erneut aufnehmen
Böhle, Elektro Schelling, Friess & Merkle, Lauxmann, Krämer, Braun, Elektro Stuttgart, Heldele, Leuchtenmeister, Schulmeister, Metzger, Sauereisen, Kienzle, ElektroService Kunst, Steckroth, Johan Technik, Schreier Service, Lehmann (Ispringen), Rudolf Fritz, Burkhard, Gronover, HISTA, Perger, SE-Gebäudeautomation, Barth Kerner, ZECH, Solar und Energie, Apleona, Bertram, Axalta, Zimmerly, Guggemos, Fehl & Sohn, F&E Elektroanlagen, Hans Loy, LTB Leitungsbau, Bürener Maschinenfabrik.
Amine ergänzt hier, an welche er wirklich schon gesendet hat.

## Technik
`pip install -r requirements.txt`. Schriften liegen in `fonts/` (Carlito, metrisch wie Calibri). Seite 2 wurde pixelgenau gegen das Original geprüft.
