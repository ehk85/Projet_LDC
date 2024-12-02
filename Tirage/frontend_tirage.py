from fpdf import FPDF
import json

class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logo_directory = "Ressources/Logos/"
    
    def add_custom_font(self):
        # Ajouter une police personnalisée en format TTF
        self.add_font("Anton", "", r"Ressources/fonts/Anton.ttf", uni=True)

    def corps_de_page(self, image_fond):
        # Image en fond sur toute la page (adapter x, y, w, h selon l'image)
        self.image(image_fond, x=-30, y=0, w=360, h=210)

        # Couleur des lignes
        self.set_draw_color(255, 255, 255) 
        # Épaisseur des lignes
        self.set_line_width(1)
        # Hauteur des lignes (par exemple)
        line_height = 190
        # Calcul de l'espacement entre chaque ligne
        largeur_page = 297  # Largeur totale de la page
        nombre_lignes = 9  # Nombre total de lignes
        espace_entre_lignes = largeur_page / nombre_lignes  # Espacement des lignes
         # Tracer les 9 lignes verticales
        for i in range(1, nombre_lignes):
            x_position = i * espace_entre_lignes  # Position en x pour chaque ligne
            self.line(x_position, 70, x_position, line_height)  # Limiter la hauteur de la ligne

    def titre(self, chapeau_num):
        # Titre dynamique pour chaque chapeau
        x, y, width, height = 10, 10, 260, 15
        
        # Positionner le texte et définir le style
        self.set_xy(x, y)
        self.set_font("Anton", "", 35)
        self.set_text_color(255, 255, 255)
        self.cell(width, height, f"LE PARCOURS DES CLUBS DU CHAPEAU {chapeau_num}", 0, 1)

    def sous_titre(self):
        x_s, y_s, width_s, height_s = 10, 22, 260, 15
        
        # Positionner le texte et définir le style
        self.set_xy(x_s, y_s)
        self.set_font("Anton", "", 25)
        self.set_text_color(255, 255, 255)
        self.cell(width_s, height_s, "Ligue des champions 2024-2025", 0, 1)

    def ajouter_logos_pour_equipes(self, equipes_dict):
        largeur_page = 297
        nombre_colonnes = 9
        espace_entre_colonnes = largeur_page / nombre_colonnes

        largeur_grand_logo, hauteur_grand_logo = 18, 20
        largeur_petit_logo, hauteur_petit_logo = 13, 13
        espacement_vertical_petit = 14

        for i, (nom_equipe, data_equipe) in enumerate(equipes_dict.items()):
            # Vérifier que la clé est bien une équipe
            if 'matches' not in data_equipe:
                continue

            x_grand = 5 + (i * espace_entre_colonnes)
            y_grand = 42

            # Logo de l'équipe principale
            logo_principal = f"{self.logo_directory}{nom_equipe}.png"
            try:
                self.image(logo_principal, x=x_grand, y=y_grand, w=largeur_grand_logo, h=hauteur_grand_logo)
            except RuntimeError:
                # Si le logo est manquant, continuer sans planter
                print(f"Logo manquant pour l'équipe : {nom_equipe}")

            # Adversaires
            y_position_petit = 75
            direction = 1

            for j, adversaire in enumerate(data_equipe['matches']):
                x_petit = x_grand - 3
                logo_adversaire = f"{self.logo_directory}{adversaire['opponent']}.png"

                if j % 2 == 0:
                    y_petit = y_position_petit
                else:
                    y_petit = (y_position_petit - 10) + (-1.2) * (7 - j)
                    x_petit = x_grand + 13
                    espacement_vertical_petit = 13

                try:
                    self.image(logo_adversaire, x=x_petit, y=y_petit, w=largeur_petit_logo, h=hauteur_petit_logo)
                except RuntimeError:
                    # Si le logo est manquant, continuer sans planter
                    print(f"Logo manquant pour l'adversaire : {adversaire['opponent']}")

                if j % 2 == 0:
                    y_position_petit += hauteur_petit_logo + espacement_vertical_petit


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




