from Tirage.backend_tirage import LDC
from Tirage.frontend_tirage import PDF
import json, time


for _ in range(3):
    tirage = LDC(r'Ressources\api object\teams.json')
    tirage.tirer_les_equipes_par_chapeau()
    tirage.sauvegarder_json()
    time.sleep(3)

# Génération du PDF avec les logos et les pages pour chaque chapeau
tirage_fichier = 'matchs_ligue.json'

with open(tirage_fichier, 'r', encoding='utf-8') as file:
    matchs = json.load(file)

pdf = PDF(orientation='L', unit='mm', format='A4')
pdf.add_custom_font()

for chapeau in range(1, 5):
    pdf.add_page()
    pdf.corps_de_page("Ressources/images/ChampionsLeague2018.jpg")
    pdf.titre(chapeau)
    pdf.sous_titre()
    pdf.ajouter_logos_pour_equipes(matchs[f'Chapeau {chapeau}'])

pdf.output("champions_league_matches.pdf")