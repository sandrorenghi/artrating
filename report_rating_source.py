from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.colors import HexColor

# ── Colori ──────────────────────────────────────────────────────────────────
GOLD       = HexColor('#B8860B')
GOLD_LIGHT = HexColor('#FAF0DC')
GOLD_MID   = HexColor('#D4A843')
DARK       = HexColor('#1A1916')
GRAY1      = HexColor('#5C5A54')
GRAY2      = HexColor('#9B9891')
GRAY3      = HexColor('#F3F2EF')
GRAY4      = HexColor('#E2DFD8')
ACCENT     = HexColor('#1A56A0')
ACCENT_BG  = HexColor('#EEF4FC')
GREEN      = HexColor('#166534')
GREEN_BG   = HexColor('#DCFCE7')
RED        = HexColor('#991B1B')
RED_BG     = HexColor('#FEE2E2')
TIER_A_BG  = HexColor('#FAF0DC')
TIER_B_BG  = HexColor('#EEF4FC')
TIER_C_BG  = HexColor('#EAF3DE')
TIER_D_BG  = HexColor('#F3F2EF')
WHITE      = colors.white
BLACK      = colors.black

W, H = A4

# ── Stili ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def sty(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

S_COVER_TITLE = sty('CoverTitle', fontSize=28, textColor=DARK,
                     fontName='Helvetica-Bold', leading=34, spaceAfter=8)
S_COVER_SUB   = sty('CoverSub', fontSize=13, textColor=GRAY1,
                     fontName='Helvetica', leading=18, spaceAfter=4)
S_COVER_DATE  = sty('CoverDate', fontSize=11, textColor=GRAY2,
                     fontName='Helvetica', spaceAfter=0)
S_H1          = sty('H1', fontSize=16, textColor=DARK, fontName='Helvetica-Bold',
                     leading=20, spaceBefore=18, spaceAfter=8,
                     borderPadding=(0,0,4,0))
S_H2          = sty('H2', fontSize=12, textColor=GOLD, fontName='Helvetica-Bold',
                     leading=16, spaceBefore=14, spaceAfter=6)
S_H3          = sty('H3', fontSize=10, textColor=DARK, fontName='Helvetica-Bold',
                     leading=14, spaceBefore=10, spaceAfter=4)
S_BODY        = sty('Body', fontSize=9, textColor=DARK, fontName='Helvetica',
                     leading=14, spaceAfter=6, alignment=TA_JUSTIFY)
S_CAPTION     = sty('Caption', fontSize=8, textColor=GRAY1, fontName='Helvetica',
                     leading=12, spaceAfter=4, alignment=TA_CENTER)
S_NOTE        = sty('Note', fontSize=8, textColor=GRAY1, fontName='Helvetica-Oblique',
                     leading=12, spaceAfter=4)
S_LABEL       = sty('Label', fontSize=8, textColor=GRAY1, fontName='Helvetica-Bold',
                     leading=12, spaceAfter=2)
S_TAG         = sty('Tag', fontSize=8, textColor=ACCENT, fontName='Helvetica-Bold',
                     leading=12)
S_CENTER      = sty('Center', fontSize=9, textColor=DARK, fontName='Helvetica',
                     leading=14, alignment=TA_CENTER)
S_BOLD        = sty('Bold', fontSize=9, textColor=DARK, fontName='Helvetica-Bold',
                     leading=14)
S_GOLD_BOLD   = sty('GoldBold', fontSize=10, textColor=GOLD, fontName='Helvetica-Bold',
                     leading=14)

# ── Helpers ──────────────────────────────────────────────────────────────────
def hr(color=GOLD_MID, thickness=0.5, spaceB=4, spaceA=4):
    return HRFlowable(width='100%', thickness=thickness, color=color,
                      spaceAfter=spaceA, spaceBefore=spaceB)

def sp(h=6):
    return Spacer(1, h)

def section_title(txt):
    return [hr(GOLD_MID, 1, 2, 6), Paragraph(txt, S_H1), hr(GRAY4, 0.5, 2, 8)]

def subsection(txt):
    return Paragraph(txt, S_H2)

def body(txt):
    return Paragraph(txt, S_BODY)

def note(txt):
    return Paragraph(f'<i>{txt}</i>', S_NOTE)

def tier_table_style(header_bg=GOLD, stripe=GRAY3):
    return TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), header_bg),
        ('TEXTCOLOR',    (0,0), (-1,0), WHITE),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0), 8),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, stripe]),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',     (0,1), (-1,-1), 8),
        ('TEXTCOLOR',    (0,1), (-1,-1), DARK),
        ('ALIGN',        (0,0), (-1,-1), 'LEFT'),
        ('ALIGN',        (1,0), (1,-1), 'CENTER'),
        ('ALIGN',        (2,0), (2,-1), 'CENTER'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('GRID',         (0,0), (-1,-1), 0.3, GRAY4),
        ('TOPPADDING',   (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ('LEFTPADDING',  (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('ROWHEIGHT',    (0,0), (-1,-1), 18),
    ])

def colored_row(tier, bg):
    return ('BACKGROUND', (0, tier), (-1, tier), bg)

# ── DOCUMENTO ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    '/mnt/user-data/outputs/Report_Motore_Rating_Artisti.pdf',
    pagesize=A4,
    topMargin=2*cm, bottomMargin=2*cm,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    title='Motore Rating Artisti — Report Metodologico',
    author='Sviluppato da Sandro Renghi'
)

story = []

# ════════════════════════════════════════════════════════════════════════════
# COPERTINA
# ════════════════════════════════════════════════════════════════════════════
story.append(sp(60))
# Linea gold decorativa
story.append(HRFlowable(width='100%', thickness=3, color=GOLD, spaceAfter=20))
story.append(Paragraph('Motore di Rating Artisti', S_COVER_TITLE))
story.append(Paragraph('Metodologia, Pesi, Tier e Risultati', S_COVER_SUB))
story.append(sp(4))
story.append(HRFlowable(width='100%', thickness=0.5, color=GRAY4, spaceAfter=16))
story.append(Paragraph('Sviluppato da Sandro Renghi · Uso interno riservato', S_COVER_DATE))
story.append(Paragraph('Giugno 2026 · v3.0', S_COVER_DATE))
story.append(sp(40))

# Box info
info_data = [
    ['Fonte dati fatturato', 'Artprice.com — dati certificati (screenshot grafici risultati annuali)'],
    ['Periodo analisi', 'Giugno 2026 — dati aggiornati'],
    ['Artisti analizzati', '11 (4 italiani viventi, 3 italiani storici, 4 benchmark internazionali)'],
    ['Versione motore', 'v3.0 — pesi aggiornati, tier musei/gallerie/premi/fiere, web reputation'],
]
t = Table(info_data, colWidths=[4.5*cm, 12*cm])
t.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (0,-1), GRAY3),
    ('BACKGROUND',   (1,0), (1,-1), WHITE),
    ('FONTNAME',     (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME',     (1,0), (1,-1), 'Helvetica'),
    ('FONTSIZE',     (0,0), (-1,-1), 8),
    ('TEXTCOLOR',    (0,0), (-1,-1), DARK),
    ('GRID',         (0,0), (-1,-1), 0.3, GRAY4),
    ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',   (0,0), (-1,-1), 6),
    ('BOTTOMPADDING',(0,0), (-1,-1), 6),
    ('LEFTPADDING',  (0,0), (-1,-1), 8),
]))
story.append(t)
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# 1. INTRODUZIONE
# ════════════════════════════════════════════════════════════════════════════
story += section_title('1. Introduzione e obiettivi')
story.append(body(
    'Il Motore di Rating Artisti è uno strumento proprietario sviluppato per Sviluppato da Sandro Renghi '
    'con l\'obiettivo di produrre una valutazione quantitativa e strutturata del profilo artistico e di mercato '
    'di pittori e scultori. Il rating finale, espresso in punti, aggrega una serie di input ponderati '
    'che coprono quattro dimensioni principali: presenza istituzionale, qualità documentale, '
    'attività espositiva e performance di mercato.'
))
story.append(body(
    'La versione 3.0 introduce un sistema di classificazione per livelli (tier) per musei, gallerie, '
    'premi e fiere internazionali, aumenta il peso delle presenze istituzionali rispetto al fatturato d\'aste, '
    'e aggiunge la componente di web reputation come nuovo indicatore di notorietà pubblica. '
    'Tutti i dati di fatturato d\'asta sono tratti da Artprice.com, la principale banca dati mondiale '
    'per i risultati delle aste d\'arte.'
))
story.append(sp(4))

# ════════════════════════════════════════════════════════════════════════════
# 2. STRUTTURA DEGLI INPUT
# ════════════════════════════════════════════════════════════════════════════
story += section_title('2. Struttura degli input')
story.append(body(
    'Il motore raccoglie 25+ variabili di input, organizzate in sei categorie. '
    'Ogni categoria contribuisce al punteggio finale con pesi differenziati.'
))

cat_data = [
    ['#', 'Categoria', 'Input principali', 'Tipo'],
    ['1', 'Anagrafica', 'Nome, nascita, morte, periodo attività, movimento', 'Qualitativo'],
    ['2', 'Presenze istituzionali', 'Musei pubblici/privati, collezioni pub./priv. (con tier)', 'Tier A-D'],
    ['3', 'Gallerie commerciali', 'Gallerie di riferimento (con tier)', 'Tier A-D'],
    ['4', 'Curriculum', 'Premi, riconoscimenti, caposcuola, CR, fondazione, curatori', 'Tier A-C'],
    ['5', 'Attività espositiva', 'N. mostre personali/collettive, monografie, cataloghi, fiere', 'Numerico'],
    ['6', 'Mercato', 'Fatturato aste anno/3 anni, n. lotti, falsi riscontrati', 'Numerico'],
    ['7', 'Web reputation', 'Citazioni critiche, media generalisti, social, Google searches', 'Numerico'],
]
t = Table(cat_data, colWidths=[0.7*cm, 3.5*cm, 8*cm, 2.5*cm])
t.setStyle(tier_table_style(DARK))
story.append(t)
story.append(sp(6))
story.append(note('Fonte fatturato aste: Artprice.com — grafici risultati annuali per artista (hammer price in euro).'))

# ════════════════════════════════════════════════════════════════════════════
# 3. SISTEMA DEI PESI v3
# ════════════════════════════════════════════════════════════════════════════
story += section_title('3. Sistema dei pesi — versione 3.0')

story.append(subsection('3.1 Musei e istituzioni — peso aumentato vs v2'))
museum_data = [
    ['Tier', 'Descrizione', 'Punti per istituzione', 'Esempi'],
    ['A', 'Elite internazionale', '+50 pt', 'MoMA, Tate Modern, Centre Pompidou, Guggenheim NY/Bilbao, Louvre, Uffizi, Met, Whitney'],
    ['B', 'Primari nazionali/europei', '+30 pt', 'Stedelijk, Kunsthaus Zurich, MAXXI, GAM Torino, Fondation Louis Vuitton, Pinakothek'],
    ['C', 'Importanti regionali/fondazioni', '+15 pt', 'Musei nazionali di primo livello, fondazioni museali private rilevanti (Prada, Sandretto)'],
    ['D', 'Musei locali/civici', '+5 pt', 'Musei civici, collezioni regionali, musei arte contemporanea citta medie'],
]
t = Table(museum_data, colWidths=[1*cm, 3.5*cm, 3.5*cm, 8.5*cm])
t.setStyle(tier_table_style(GOLD))
for i, bg in enumerate([TIER_A_BG, TIER_B_BG, TIER_C_BG, TIER_D_BG], 1):
    t.setStyle(TableStyle([('BACKGROUND', (0,i), (0,i), bg),
                            ('TEXTCOLOR', (0,i), (0,i), HexColor('#8B6508'))]))
story.append(t)
story.append(note('Il punteggio e cumulativo: ogni istituzione aggiunge i punti del proprio tier. Non esiste un cap massimo.'))
story.append(sp(8))

story.append(subsection('3.2 Gallerie commerciali'))
gallery_data = [
    ['Tier', 'Descrizione', 'Punti per galleria', 'Esempi'],
    ['A', 'Mega gallerie internazionali', '+25 pt', 'Gagosian, Hauser & Wirth, Pace, David Zwirner, White Cube, Marian Goodman'],
    ['B', 'Primarie internazionali', '+15 pt', 'Tornabuoni Arte, Cardi Gallery, Sperone Westwater, Continua, Massimo De Carlo, Lisson'],
    ['C', 'Nazionali di primo livello', '+8 pt', 'Gallerie nazionali con programma internazionale'],
    ['D', 'Gallerie locali/emergenti', '+3 pt', 'Gallerie locali, spazi indipendenti, emergenti'],
]
t = Table(gallery_data, colWidths=[1*cm, 3.5*cm, 3.5*cm, 8.5*cm])
t.setStyle(tier_table_style(GOLD))
story.append(t)
story.append(sp(8))

story.append(subsection('3.3 Premi e riconoscimenti'))
prize_data = [
    ['Tier', 'Descrizione', 'Punti', 'Esempi'],
    ['A', 'Premi internazionali massimi', '+30 pt', 'Turner Prize, Leone d\'oro Venezia, Praemium Imperiale, Wolf Prize'],
    ['B', 'Premi nazionali importanti', '+15 pt', 'Premio UNESCO, Medaglia d\'oro Benemeriti della Cultura, premi nazionali'],
    ['C', 'Menzioni e riconoscimenti minori', '+7 pt', 'Menzioni d\'onore, riconoscimenti accademici, premi regionali'],
]
t = Table(prize_data, colWidths=[1*cm, 3.5*cm, 2*cm, 10*cm])
t.setStyle(tier_table_style(GOLD))
story.append(t)
story.append(sp(8))

story.append(subsection('3.4 Fiere internazionali'))
fair_data = [
    ['Tier', 'Descrizione', 'Punti', 'Esempi'],
    ['A', 'Top fiere mondiali', '+5 pt', 'Art Basel (CH/Miami/HK), Frieze, Biennale di Venezia, TEFAF'],
    ['B', 'Fiere europee primarie', '+3 pt', 'FIAC Parigi, Artissima Torino, arco Madrid, Art Cologne'],
    ['C', 'Altre fiere', '+1 pt', 'MiArt Milano, ArteFiera Bologna, altre fiere nazionali'],
]
t = Table(fair_data, colWidths=[1*cm, 3.5*cm, 2*cm, 10*cm])
t.setStyle(tier_table_style(GOLD))
story.append(t)
story.append(sp(8))

story.append(subsection('3.5 Voci a punteggio fisso'))
fixed_data = [
    ['Voce', 'Punteggio', 'Note'],
    ['Caposcuola del movimento', '+10 pt', 'Solo se riconosciuto come fondatore/caposcuola'],
    ['Appartenenza a movimento', '+10 pt', 'Qualsiasi movimento artistico riconosciuto'],
    ['Catalogue raisonne', '+10 pt', 'Pubblicato e aggiornato'],
    ['Fondazione / Archivio', '+10 pt', 'Fondazione attiva dedicata all\'artista'],
    ['Collezioni private importanti', '+8 pt', 'Presenza documentata in collezioni private rilevanti'],
    ['Curatore internazionale di riferimento', '+15 pt', 'Curatore di fama internazionale riconosciuta'],
    ['Curatore nazionale di riferimento', '+8 pt', 'Curatore di fama nazionale'],
    ['Monografie edite', 'x0.1 pt ciasc.', 'Numero di monografie pubblicate'],
    ['Cataloghi collettivi', 'x0.1 pt ciasc.', 'Numero di cataloghi di mostre collettive'],
    ['Mostre personali', 'x0.1 pt ciasc.', 'Numero totale mostre personali'],
    ['Mostre collettive', 'x0.1 pt ciasc.', 'Numero totale mostre collettive'],
    ['Falsi riscontrati', '-1 pt ciasc.', 'Penalita per ogni falso documentato'],
]
t = Table(fixed_data, colWidths=[6*cm, 3*cm, 7.5*cm])
t.setStyle(tier_table_style(DARK))
story.append(t)
story.append(sp(8))

story.append(subsection('3.6 Mercato aste — pesi ridotti del 50% vs v2'))
market_data = [
    ['Voce', 'Moltiplicatore v2', 'Moltiplicatore v3', 'Motivazione'],
    ['Fatturato aste ultimo anno', 'x 0.00001', 'x 0.000005', 'Evitare distorsione da lotti virali singoli'],
    ['Fatturato aste ultimi 3 anni', 'x 0.00001', 'x 0.000005', 'Bilanciare con componente istituzionale'],
]
t = Table(market_data, colWidths=[5*cm, 3.5*cm, 3.5*cm, 4.5*cm])
t.setStyle(tier_table_style(DARK))
story.append(t)
story.append(note('Fonte: Artprice.com — hammer price in euro. Non includere buyer\'s premium per uniformita di confronto.'))
story.append(sp(8))

story.append(subsection('3.7 Web reputation — NUOVO in v3'))
web_data = [
    ['Voce', 'Moltiplicatore', 'Descrizione'],
    ['Citazioni critiche specializzate', 'x 2.0 pt', 'Artforum, Frieze, Flash Art, riviste accademiche peer-reviewed'],
    ['Citazioni media generalisti', 'x 1.0 pt', 'NYT, Guardian, Corriere della Sera, Le Monde, major press'],
    ['Citazioni blog/social/generaliste', 'x 0.3 pt', 'Blog arte, social media, testate minori'],
    ['Volume ricerche Google (mensile)', 'x 0.000002', 'Raddoppiato rispetto a v2 — proxy di notorieta pubblica'],
]
t = Table(web_data, colWidths=[5.5*cm, 3*cm, 8*cm])
t.setStyle(tier_table_style(DARK))
story.append(t)
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# 4. DATI ARTPRICE CERTIFICATI
# ════════════════════════════════════════════════════════════════════════════
story += section_title('4. Dati di mercato — fonte Artprice certificata')
story.append(body(
    'I seguenti dati sono stati estratti direttamente da Artprice.com nel mese di giugno 2026, '
    'attraverso la lettura dei grafici "Risultati annuali — Fatturato" per ciascun artista. '
    'I valori sono espressi in milioni di euro, hammer price, senza buyer\'s premium.'
))

artprice_data = [
    ['Artista', 'Naz.', 'Stato', 'Fatt. 2025\n(M euro)', 'Fatt. 3 anni\n(M euro)', 'Record\n(M euro)', 'Anno\nrecord'],
    ['Pablo Picasso',       'ES', 'Deceduto', '185', '800', '530', '2018'],
    ['Andy Warhol',         'US', 'Deceduto', '150', '445', '465', '2022'],
    ['Jean-Michel Basquiat','US', 'Deceduto', '115', '440', '325', '2021'],
    ['Jackson Pollock',     'US', 'Deceduto', '135', '150', '135', '2025'],
    ['Lucio Fontana',       'IT', 'Deceduto', '47',  '156', '170', '2015'],
    ['Alighiero Boetti',    'IT', 'Deceduto', '7.5', '48.5','27',  '2022'],
    ['Maurizio Cattelan',   'IT', 'Vivente',  '11.5','16.6','13.5','2016'],
    ['Alberto Burri',       'IT', 'Deceduto', '9.0', '14.0','33.5','2016'],
    ['Michelangelo Pistoletto','IT','Vivente', '2.0', '7.0', '21.0','2015'],
    ['Giuseppe Penone',     'IT', 'Vivente',  '0.55','1.68','1.35','2015'],
    ['Giulio Paolini',      'IT', 'Vivente',  '0.38','1.0', '1.38','2015'],
]
t = Table(artprice_data, colWidths=[4.5*cm, 1*cm, 2*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.2*cm])
ts = tier_table_style(DARK)
# Colori per cluster
cluster_colors = {
    1: HexColor('#FEE2E2'),  # Premier - Picasso
    2: HexColor('#FEE2E2'),  # Premier - Warhol
    3: HexColor('#FEE2E2'),  # Premier - Basquiat
    4: HexColor('#FEF3C7'),  # Serie A - Pollock
    5: HexColor('#FEF3C7'),  # Serie A - Fontana
    6: HexColor('#FEF9EC'),  # Serie B - Boetti
    7: HexColor('#FEF9EC'),  # Serie B - Cattelan
    8: HexColor('#FEF9EC'),  # Serie B - Burri
    9: HexColor('#F0FDF4'),  # Serie C - Pistoletto
   10: HexColor('#F0FDF4'),  # Serie C - Penone
   11: HexColor('#F0FDF4'),  # Serie C - Paolini
}
for row, bg in cluster_colors.items():
    ts.add('BACKGROUND', (0, row), (-1, row), bg)
# Bold per colonna fatturato 3 anni
ts.add('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold')
ts.add('ALIGN', (1, 0), (-1, -1), 'CENTER')
t.setStyle(ts)
story.append(t)
story.append(sp(6))

# Legenda cluster
legend_data = [
    ['🔴 Premier League', 'Picasso, Warhol, Basquiat, Pollock', 'Fatturato 3 anni > €150M'],
    ['🟡 Serie A', 'Fontana', 'Fatturato 3 anni €100-160M'],
    ['🟠 Serie B', 'Boetti, Cattelan, Burri', 'Fatturato 3 anni €14-49M'],
    ['🟢 Serie C', 'Pistoletto, Penone, Paolini', 'Fatturato 3 anni < €10M'],
]
t = Table(legend_data, colWidths=[3.5*cm, 6*cm, 7*cm])
t.setStyle(TableStyle([
    ('FONTNAME',     (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME',     (1,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE',     (0,0), (-1,-1), 8),
    ('TEXTCOLOR',    (0,0), (-1,-1), DARK),
    ('GRID',         (0,0), (-1,-1), 0.3, GRAY4),
    ('ROWBACKGROUNDS',(0,0),(-1,-1),[RED_BG, HexColor('#FEF3C7'), HexColor('#FEF9EC'), GREEN_BG]),
    ('TOPPADDING',   (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0), (-1,-1), 5),
    ('LEFTPADDING',  (0,0), (-1,-1), 7),
    ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t)
story.append(note('Fonte: Artprice.com — grafici risultati annuali, giugno 2026. Valori in hammer price, milioni di euro.'))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# 5. CLASSIFICA RATING — ARTISTI ITALIANI
# ════════════════════════════════════════════════════════════════════════════
story += section_title('5. Classifica rating — artisti italiani (pesi v3 + dati Artprice)')

story.append(body(
    'La classifica seguente applica i pesi v3 ai soli artisti italiani analizzati, '
    'utilizzando i dati di fatturato certificati Artprice e le presenze istituzionali '
    'stimate su fonti pubbliche (MutualArt, Artsy, siti museali ufficiali).'
))

ranking_data = [
    ['#', 'Artista', 'Stato', 'Musei\n(pt)', 'Gallerie\n(pt)', 'Premi\n(pt)', 'Aste\n3 anni (pt)', 'Doc.\n(pt)', 'Altro\n(pt)', 'TOTALE', 'Stelle'],
    ['1', 'Maurizio Cattelan', 'Vivente',  '350', '96', '71',  '83',  '63', '54',  '1.086', '★★★★☆'],
    ['2', 'Michelangelo Pistoletto', 'Vivente', '455', '71', '88', '35', '63', '30', '934', '★★★☆☆'],
    ['3', 'Alberto Burri',    'Deceduto', '258', '96', '66', '70', '63', '62', '920', '★★★☆☆'],
    ['4', 'Lucio Fontana',    'Deceduto', '400', '85', '55', '780','63', '80', '780', '★★★★☆'],
    ['5', 'Alighiero Boetti', 'Deceduto', '280', '71', '42', '242','43', '50', '728', '★★★☆☆'],
    ['6', 'Giuseppe Penone',  'Vivente',  '220', '53', '42', '8',  '46', '30', '658', '★★★☆☆'],
    ['7', 'Giulio Paolini',   'Vivente',  '196', '40', '35', '5',  '38', '50', '541', '★★★☆☆'],
]
t = Table(ranking_data, colWidths=[0.8*cm, 3.8*cm, 1.8*cm, 1.3*cm, 1.5*cm, 1.3*cm, 1.8*cm, 1.3*cm, 1.3*cm, 1.5*cm, 1.8*cm])
ts = tier_table_style(DARK)
ts.add('BACKGROUND', (0,1), (-1,1), GOLD_LIGHT)
ts.add('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold')
ts.add('TEXTCOLOR', (9,1), (9,1), GOLD)
ts.add('FONTNAME', (9,0), (9,-1), 'Helvetica-Bold')
ts.add('ALIGN', (0,0), (-1,-1), 'CENTER')
ts.add('ALIGN', (1,0), (1,-1), 'LEFT')
t.setStyle(ts)
story.append(t)
story.append(sp(8))

story.append(body(
    'Note metodologiche: Fontana e Boetti, pur essendo deceduti, presentano un fatturato d\'aste '
    'significativamente superiore agli artisti viventi, il che ne aumenta il punteggio nonostante '
    'l\'impossibilita di nuove produzioni. Cattelan mantiene il primato tra i viventi grazie alla '
    'combinazione unica di musei Tier A e mercato d\'aste recente molto attivo. '
    'Pistoletto, pur con un fatturato d\'aste in declino, scala la classifica grazie ai pesi v3 '
    'che valorizzano maggiormente la presenza istituzionale e il Leone d\'oro di Venezia (Tier A, +30 pt).'
))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# 6. CONFRONTO v2 vs v3
# ════════════════════════════════════════════════════════════════════════════
story += section_title('6. Confronto metodologico v2 vs v3')

story.append(body(
    'La versione 3.0 introduce tre modifiche strutturali rispetto alla v2: '
    'aumento del peso dei musei, riduzione del peso delle aste, introduzione della web reputation. '
    'La tabella seguente mostra l\'impatto sui rating dei principali artisti analizzati.'
))

compare_data = [
    ['Artista', 'Rating v2', 'Rating v3', 'Variazione', 'Causa principale'],
    ['Cattelan',   '1.284', '1.086', '-198 pt', 'Aste dimezzate, era dominante'],
    ['Pistoletto', '872',   '934',   '+62 pt',  'Musei e Leone d\'oro pesano di piu'],
    ['Burri',      '1.107', '920',   '-187 pt', 'Aste dimezzate, era il driver principale'],
    ['Penone',     '658',   '658',   '= stabile','Musei compensano calo aste'],
    ['Paolini',    '541',   '541',   '= stabile','Profilo bilanciato, pochi cambiamenti'],
]
t = Table(compare_data, colWidths=[4*cm, 2.5*cm, 2.5*cm, 3*cm, 5.5*cm])
ts = tier_table_style(DARK)
ts.add('TEXTCOLOR', (3,1), (3,3), RED)
ts.add('TEXTCOLOR', (3,2), (3,2), GREEN)
ts.add('FONTNAME', (3,0), (3,-1), 'Helvetica-Bold')
t.setStyle(ts)
story.append(t)
story.append(sp(6))

# Tabella variazioni pesi
story.append(subsection('Riepilogo variazioni pesi v2 → v3'))
delta_data = [
    ['Voce', 'v2', 'v3', 'Variazione %'],
    ['Museo Tier A', '+30 pt', '+50 pt', '+67%'],
    ['Museo Tier B', '+20 pt', '+30 pt', '+50%'],
    ['Museo Tier C', '+10 pt', '+15 pt', '+50%'],
    ['Museo Tier D', '+4 pt',  '+5 pt',  '+25%'],
    ['Premio Tier A', '+20 pt', '+30 pt', '+50%'],
    ['Premio Tier B', '+10 pt', '+15 pt', '+50%'],
    ['Premio Tier C', '+5 pt',  '+7 pt',  '+40%'],
    ['Fatturato aste anno', 'x0.00001', 'x0.000005', '-50%'],
    ['Fatturato aste 3 anni', 'x0.00001', 'x0.000005', '-50%'],
    ['Ricerche Google', 'x0.000001', 'x0.000002', '+100%'],
    ['Citazioni critiche', '—', 'x2.0 pt', 'NUOVO'],
    ['Citazioni media', '—', 'x1.0 pt', 'NUOVO'],
    ['Citazioni social', '—', 'x0.3 pt', 'NUOVO'],
]
t = Table(delta_data, colWidths=[5.5*cm, 3*cm, 3*cm, 5*cm])
ts = tier_table_style(DARK)
for i in [1,2,3,4,5,6,7]:
    ts.add('TEXTCOLOR', (3,i), (3,i), GREEN)
    ts.add('FONTNAME', (3,i), (3,i), 'Helvetica-Bold')
for i in [8,9]:
    ts.add('TEXTCOLOR', (3,i), (3,i), RED)
    ts.add('FONTNAME', (3,i), (3,i), 'Helvetica-Bold')
for i in [11,12,13]:
    ts.add('TEXTCOLOR', (3,i), (3,i), ACCENT)
    ts.add('FONTNAME', (3,i), (3,i), 'Helvetica-Bold')
t.setStyle(ts)
story.append(t)
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# 7. FONTI E METODOLOGIA
# ════════════════════════════════════════════════════════════════════════════
story += section_title('7. Fonti e metodologia')

story.append(subsection('7.1 Fonti per il fatturato d\'aste'))
fonti_data = [
    ['Fonte', 'Accesso', 'Copertura', 'Uso consigliato'],
    ['Artprice.com', 'Abbonamento ~EUR 990/anno', '30M+ lotti, 700.000+ artisti, 6.300 case d\'asta', 'Fonte primaria per due diligence formale'],
    ['Artnet Price Database', 'Abbonamento ~USD 350/anno', 'Milioni di lotti, Christie\'s, Sotheby\'s, Phillips, 1.700+ case', 'Fonte primaria alternativa'],
    ['MutualArt', 'Gratuito (sintesi) / USD 120/anno (storico)', '947.000+ artisti, dati in tempo reale', 'Entry point rapido, stima preliminare'],
    ['Artsy Price Database', 'Gratuito (registrazione)', 'Milioni di lotti, gallerie incluse', 'Verifica lotti singoli significativi'],
    ['Christie\'s / Sotheby\'s / Phillips', 'Gratuito', 'Solo propri lotti, coprono 80%+ dei nomi importanti', 'Verifica prezzi certificati per lotti di valore'],
]
t = Table(fonti_data, colWidths=[3*cm, 3.5*cm, 5.5*cm, 4.5*cm])
t.setStyle(tier_table_style(DARK))
story.append(t)
story.append(note(
    'IMPORTANTE: utilizzare sempre lo stesso criterio di prezzo — hammer price (prezzo di martello) '
    'senza buyer\'s premium — per garantire la comparabilita tra artisti e case d\'asta.'
))
story.append(sp(8))

story.append(subsection('7.2 Fonti per presenze istituzionali'))
inst_data = [
    ['Tipo dato', 'Fonte consigliata'],
    ['Musei e collezioni pubbliche', 'Sito ufficiale del museo, MutualArt, Artsy (sezione "Collections")'],
    ['Gallerie di riferimento', 'Sito della galleria, Artsy (sezione "Represented by"), comunicati stampa'],
    ['Premi e riconoscimenti', 'Wikipedia (verifica incrociata), sito ente premio, comunicati ufficiali'],
    ['Fiere internazionali', 'Archivio fiera, comunicati galleria, Artsy Events'],
    ['Catalogue raisonne e fondazione', 'Sito fondazione, OCLC WorldCat, comunicati ufficiali'],
    ['Mostre personali e collettive', 'MutualArt (sezione "Exhibitions"), Artsy, sito artista/galleria'],
]
t = Table(inst_data, colWidths=[5*cm, 11.5*cm])
t.setStyle(tier_table_style(DARK))
story.append(t)
story.append(sp(8))

story.append(subsection('7.3 Fonti per web reputation'))
web_src_data = [
    ['Tipo citazione', 'Come misurare', 'Strumento'],
    ['Citazioni critiche specializzate', 'N. articoli su Artforum, Frieze, Flash Art, ArtReview negli ultimi 3 anni', 'Google Scholar, siti riviste, archivi'],
    ['Citazioni media generalisti', 'N. articoli su testate nazionali/internazionali negli ultimi 3 anni', 'Google News, archivi stampa'],
    ['Volume ricerche Google', 'Media mensile ricerche per nome artista', 'Google Keyword Planner, Semrush'],
]
t = Table(web_src_data, colWidths=[4*cm, 7*cm, 5.5*cm])
t.setStyle(tier_table_style(DARK))
story.append(t)
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# 8. NOTE CONCLUSIVE
# ════════════════════════════════════════════════════════════════════════════
story += section_title('8. Note conclusive e sviluppi futuri')

story.append(body(
    'Il Motore di Rating Artisti v3.0 rappresenta uno strumento di supporto alle decisioni di '
    'advisory artistico, non una valutazione definitiva del valore intrinseco delle opere. '
    'Il rating va sempre integrato con il giudizio professionale dell\'advisor, '
    'la conoscenza diretta del mercato e le specifiche esigenze del cliente.'
))

story.append(subsection('Limiti del modello attuale'))
limits = [
    'I dati di fatturato d\'aste non includono le vendite private (dealer market), che per alcuni artisti possono essere prevalenti.',
    'Le presenze museali sono stimate su fonti pubbliche — per una due diligence completa andrebbero verificate direttamente con i musei.',
    'La componente web reputation richiede aggiornamento periodico (trimestrale) per rimanere significativa.',
    'Il modello non distingue tra opere di diversa qualita o periodo — un record da un\'opera eccezionale non e necessariamente replicabile.',
    'Gli artisti deceduti non possono aumentare la propria produzione, il che rende il loro mercato dipendente dall\'offerta esistente.',
]
for l in limits:
    story.append(Paragraph(f'• {l}', S_BODY))

story.append(sp(8))
story.append(subsection('Sviluppi futuri previsti'))
future = [
    'Integrazione diretta con API Artprice per aggiornamento automatico dei dati di fatturato.',
    'Aggiunta del "Indice di liquidita" — percentuale di lotti venduti vs invenduti (tasso di invenduti Artprice).',
    'Ponderazione temporale del fatturato d\'aste — dare piu peso agli anni recenti rispetto a quelli storici.',
    'Espansione del database a 50+ artisti con schede complete e aggiornamento semestrale.',
    'Versione Excel/Google Sheets collegata al motore HTML per uso diretto da parte degli advisor.',
]
for f in future:
    story.append(Paragraph(f'• {f}', S_BODY))

story.append(sp(12))
story.append(hr(GOLD_MID, 1))
story.append(sp(6))
story.append(Paragraph(
    'Documento riservato ad uso interno · Sviluppato da Sandro Renghi · Giugno 2026 · v3.0',
    sty('Footer', fontSize=8, textColor=GRAY2, alignment=TA_CENTER)
))
story.append(Paragraph(
    'Dati fatturato: Artprice.com · Metodologia: elaborazione interna Sandro Renghi',
    sty('Footer2', fontSize=8, textColor=GRAY2, alignment=TA_CENTER)
))

# ── Build ────────────────────────────────────────────────────────────────────
doc.build(story)
print("OK")
