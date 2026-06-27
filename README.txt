═══════════════════════════════════════════════════════════
  MOTORE RATING ARTISTI — Sandro Renghi
  Sviluppato giugno 2026
═══════════════════════════════════════════════════════════

CONTENUTO CARTELLA
──────────────────

1. Motore_Rating_v1.html
   Prima versione del motore. Funziona con prompt AI + copia/incolla JSON.
   Schema base senza tier. Apri con doppio clic nel browser.

2. Motore_Rating_v2_Tier.html
   Versione aggiornata con sistema tier completo per musei, gallerie,
   premi e fiere. Inserimento manuale + modalità AI.
   → VERSIONE CONSIGLIATA PER USO CORRENTE

3. Report_Motore_Rating_Artisti_v3.pdf
   Report metodologico completo (8 sezioni):
   - Struttura input e pesi v3
   - Tabelle tier complete
   - Dati Artprice certificati (11 artisti)
   - Classifica rating italiana
   - Confronto v2 vs v3
   - Fonti e metodologia

4. report_rating_source.py
   Sorgente Python per rigenerare il PDF. Richiede: pip install reportlab

DATI ARTPRICE RACCOLTI (giugno 2026)
──────────────────────────────────────
Artista              | Fatt.2025 | Fatt.3anni | Record
─────────────────────|───────────|────────────|───────
Pablo Picasso        | €185M     | €800M      | €530M (2018)
Andy Warhol          | €150M     | €445M      | €465M (2022)
Jean-Michel Basquiat | €115M     | €440M      | €325M (2021)
Jackson Pollock      | €135M     | €150M      | €135M (2025)
Lucio Fontana        | €47M      | €156M      | €170M (2015)
Alighiero Boetti     | €7.5M     | €48.5M     | €27M  (2022)
Maurizio Cattelan    | €11.5M    | €16.6M     | €13.5M(2016)
Alberto Burri        | €9.0M     | €14.0M     | €33.5M(2016)
Michelangelo Pistoletto | €2.0M  | €7.0M      | €21.0M(2015)
Giuseppe Penone      | €0.55M    | €1.68M     | €1.35M(2015)
Giulio Paolini       | €0.38M    | €1.0M      | €1.38M(2015)

PESI v3 (sintesi)
──────────────────
Musei:   Tier A +50pt / B +30pt / C +15pt / D +5pt
Gallerie: Tier A +25pt / B +15pt / C +8pt / D +3pt
Premi:   Tier A +30pt / B +15pt / C +7pt
Fiere:   Tier A +5pt / B +3pt / C +1pt
Aste:    x0.000005 (dimezzato vs v2)
Web rep: citaz.critiche x2 / media x1 / social x0.3

PROSSIMI PASSI
──────────────
- Aggiungere artisti al database (usare Artprice)
- Inserire dati web reputation reali
- Sviluppare versione v3 del motore HTML con pesi aggiornati

═══════════════════════════════════════════════════════════
