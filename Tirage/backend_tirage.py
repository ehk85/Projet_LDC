import json
import random

class LDC:
    def __init__(self, fichier_teams_json):
        with open(fichier_teams_json, 'r', encoding='utf-8') as file:
            self.teams = json.load(file)
        self.matches = {f'Chapeau {chapeau}': {} for chapeau in range(1, 5)}
        self.chapeaux = {chapeau: [] for chapeau in range(1, 5)}
        self.match_counts = {team['nom']: 0 for team in self.teams}
        self.chapeau_selections = {chapeau: {team['nom']: 0 for team in self.teams} for chapeau in range(1, 5)}
        self._prepare_chapeaux()

    def _prepare_chapeaux(self):
        for team in self.teams:
            chapeau = team['chapeau']
            self.chapeaux[chapeau].append(team)
            self.matches[f'Chapeau {chapeau}'][team['nom']] = {'matches': []}
            self.chapeau_selections[chapeau][team['nom']] = 0

    def tirer_les_equipes_par_chapeau(self):
        for chapeau in range(1, 5):
            print(f"\nEntrée dans le chapeau {chapeau}")
            # Réinitialiser les compteurs de sélection pour toutes les équipes
            for chapeau_key in self.chapeau_selections:
                for equipe_nom in self.chapeau_selections[chapeau_key]:
                    self.chapeau_selections[chapeau_key][equipe_nom] = 0

            for equipe in self.chapeaux[chapeau]:
                print(f"Traitement de l'équipe {equipe['nom']} du chapeau {chapeau}")
                self._traiter_equipe(equipe, chapeau)
            print(f"Sortie du chapeau {chapeau}")

        self._verifier_et_completer_matchs()

    def _traiter_equipe(self, equipe, chapeau_actuel):
        nom_equipe = equipe['nom']
        chapeau_equipe = equipe['chapeau']
        matchs_restants = 8 - self.match_counts[nom_equipe]

        if matchs_restants <= 0:
            return

        adversaires_a_trouver = {
            'meme_chapeau': 2 if chapeau_actuel == chapeau_equipe else 0,
            'autres_chapeaux': {i: 2 for i in range(1, 5) if i != chapeau_actuel}
        }

        adversaires_existants = self.matches[f'Chapeau {chapeau_equipe}'][nom_equipe]['matches']
        for match in adversaires_existants:
            chapeau_adversaire = match['Chapeau']
            if chapeau_adversaire == chapeau_actuel:
                adversaires_a_trouver['meme_chapeau'] -= 1
            else:
                adversaires_a_trouver['autres_chapeaux'][chapeau_adversaire] -= 1

        adversaires_choisis = []

        if adversaires_a_trouver['meme_chapeau'] > 0:
            adversaires_choisis.extend(self._tirer_adversaires(nom_equipe, chapeau_actuel, adversaires_a_trouver['meme_chapeau'], equipe['pays'], chapeau_actuel))

        for chapeau in sorted(adversaires_a_trouver['autres_chapeaux'].keys()):
            nombre_a_tirer = adversaires_a_trouver['autres_chapeaux'][chapeau]
            if nombre_a_tirer > 0:
                adversaires_choisis.extend(self._tirer_adversaires(nom_equipe, chapeau, nombre_a_tirer, equipe['pays'], chapeau_actuel))

        self._enregistrer_matchs(equipe, adversaires_choisis)

    def _tirer_adversaires(self, nom_equipe, chapeau, nombre_a_tirer, pays_equipe, chapeau_equipe_principal):
        adversaires_possibles = [adversaire for adversaire in self.chapeaux[chapeau]
                                 if adversaire['nom'] != nom_equipe
                                 and adversaire['pays'] != pays_equipe
                                 and self.match_counts[adversaire['nom']] < 8
                                 and self.chapeau_selections[chapeau][adversaire['nom']] < 2]
        if len(adversaires_possibles) < nombre_a_tirer:
            nombre_a_tirer = len(adversaires_possibles)

        adversaires_selectionnes = random.sample(adversaires_possibles, nombre_a_tirer)
        
        for adversaire in adversaires_selectionnes:
            self.chapeau_selections[chapeau][adversaire['nom']] += 1

        return adversaires_selectionnes

    def _enregistrer_matchs(self, equipe, adversaires_choisis):
        nom_equipe = equipe['nom']
        chapeau_equipe = equipe['chapeau']

        for adversaire in adversaires_choisis:
            location = 'home' if len(self.matches[f'Chapeau {chapeau_equipe}'][nom_equipe]['matches']) % 2 == 0 else 'away'
            self.matches[f'Chapeau {chapeau_equipe}'][nom_equipe]['matches'].append(
                {
                    'opponent': adversaire['nom'],
                    'Chapeau': adversaire['chapeau'],
                    'location': location
                }
            )
            self.match_counts[nom_equipe] += 1
            location_inverse = 'away' if location == 'home' else 'home'
            self.matches[f"Chapeau {adversaire['chapeau']}"][adversaire['nom']]['matches'].append(
                {
                    'opponent': nom_equipe,
                    'Chapeau': chapeau_equipe,
                    'location': location_inverse
                }
            )
            self.match_counts[adversaire['nom']] += 1

    def _verifier_et_completer_matchs(self):
        equipes_incompletes = [equipe for chapeau in range(1, 5) for equipe in self.chapeaux[chapeau] if self.match_counts[equipe['nom']] < 8]

        while equipes_incompletes:
            for equipe in equipes_incompletes:
                matchs_restants = 8 - self.match_counts[equipe['nom']]
                if matchs_restants > 0:
                    self._completer_matchs(equipe, matchs_restants)
            equipes_incompletes = [equipe for chapeau in range(1, 5) for equipe in self.chapeaux[chapeau] if self.match_counts[equipe['nom']] < 8]

    def _completer_matchs(self, equipe, matchs_restants):
        nom_equipe = equipe['nom']
        adversaires_choisis = []

        adversaires_possibles = [adversaire for adversaire in self.teams if adversaire['nom'] != nom_equipe and self.match_counts[adversaire['nom']] < 8]
        if len(adversaires_possibles) < matchs_restants:
            matchs_restants = len(adversaires_possibles)

        adversaires_selectionnes = random.sample(adversaires_possibles, matchs_restants)
        adversaires_choisis.extend(adversaires_selectionnes)

        self._enregistrer_matchs(equipe, adversaires_choisis)

    def sauvegarder_json(self, fichier_sortie='matchs_ligue.json'):
        with open(fichier_sortie, 'w', encoding='utf-8') as outfile:
            json.dump(self.matches, outfile, indent=4, ensure_ascii=False)
        print("Résultats enregistrés dans 'matchs_ligue.json'.")

# Exemple d'utilisation
tirage = LDC(r'Ressources\api object\teams.json')
tirage.tirer_les_equipes_par_chapeau()
tirage.sauvegarder_json()
 