import flet as ft
import random

class Puzzle8(ft.Column):
    """
    Objet Column représentant le jeu de Taquin avec une interface Flet.
    """

    def __init__(self):
        # 1. Préparation des champs de texte (Chiffres blancs, gros et centrés)
        self.squares = [
            ft.TextField(
                value=str(i),
                color=ft.Colors.WHITE,
                text_align=ft.TextAlign.CENTER,
                text_size=35,
                border=ft.InputBorder.NONE,
            ) for i in range(9)
        ]
        
        # 2. Préparation des conteneurs (Rouge pour le 0, Indigo pour les autres)
        self.containers = [
            ft.Container(
                content=self.squares[i],
                bgcolor=ft.Colors.RED if i == 0 else ft.Colors.INDIGO,
                border_radius=5,
                # Utilisation de ft.Alignment(0, 0) pour centrer parfaitement
                alignment=ft.Alignment(0, 0), 
            ) for i in range(9)
        ]

        # 3. Création locale du texte pour éviter l'erreur SyntaxError sur self.
        message_area = ft.Text("Prêt à jouer", size=16)
        
        children = [
            # Zone de message
            ft.Row([message_area]),

            # Grille 3x3 (adaptée pour une largeur de fenêtre de 400)
            ft.GridView(
                controls=self.containers,
                runs_count=3,
                height=350, 
            ),

            # Barre d'outils (Boutons)
            ft.Row([
                ft.IconButton(
                    ft.Icons.SHUFFLE,
                    icon_color=ft.Colors.INDIGO,
                    on_click=lambda e: self.melange(e)
                ),
                ft.IconButton(
                    ft.Icons.NEXT_PLAN,
                    icon_color=ft.Colors.INDIGO,
                    on_click=lambda e: self.my_callback(e),
                ),
                ft.IconButton(
                    ft.Icons.CATCHING_POKEMON,
                    icon_color=ft.Colors.INDIGO,
                    on_click=lambda e: self.resoudre(e),
                ),
                ft.IconButton(
                    ft.Icons.BAKERY_DINING,
                    icon_color=ft.Colors.INDIGO,
                    on_click=lambda e: self.recommence(e),
                ),
                ft.IconButton(
                    ft.Icons.CHECK_CIRCLE,
                    icon_color=ft.Colors.GREEN,
                    on_click=lambda e: self.verifier_solubilite(e)
                )
            ])
        ]
        
        super().__init__(children)

        # On stocke les références pour les utiliser dans les méthodes
        self.message_area = message_area

    def my_callback(self, event):
        self.message_area.value = "Bouton Start cliqué"
        self.squares[0].value = "X"
        self.update()

    def melange(self, event):
        """Mélange les nombres et met à jour la couleur rouge sur le 0."""
        liste_nombres = list(range(9))
        random.shuffle(liste_nombres)
        for i in range(9):
            val = liste_nombres[i]
            # On affiche le chiffre ou rien si c'est 0
            self.squares[i].value = str(val) if val != 0 else ""
            # La case rouge suit le chiffre 0
            self.containers[i].bgcolor = ft.Colors.RED if val == 0 else ft.Colors.INDIGO
        
        self.message_area.value = "Grille mélangée"
        self.message_area.color = ft.Colors.WHITE
        self.update()

    def verifier_solubilite(self, event):
        """Calcule si la grille actuelle peut être résolue."""
        # On récupère les valeurs numériques (0 si vide ou texte)
        actuelle = []
        for s in self.squares:
            val = s.value
            actuelle.append(int(val) if (val and val.isdigit()) else 0)

        # Calcul des inversions
        tiles = [t for t in actuelle if t != 0]
        inversions = 0
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i] > tiles[j]:
                    inversions += 1
        
        perm_parite = (inversions % 2 == 0)

        # Distance de Manhattan de la case vide (0) vers la cible (2,2)
        idx_zero = actuelle.index(0)
        r, c = divmod(idx_zero, 3)
        dist_manhattan = abs(2 - r) + abs(2 - c)
        dist_parite = (dist_manhattan % 2 == 0)

        if perm_parite == dist_parite:
            self.message_area.value = "SOLUBLE ! ✅"
            self.message_area.color = ft.Colors.GREEN
        else:
            self.message_area.value = "INSOLUBLE ! ❌"
            self.message_area.color = ft.Colors.RED
        self.update()

    def recommence(self, event):
        """Réinitialise la grille dans l'ordre (0 à 8)."""
        for i in range(9):
            self.squares[i].value = str(i) if i != 0 else ""
            self.containers[i].bgcolor = ft.Colors.RED if i == 0 else ft.Colors.INDIGO
        
        self.message_area.value = "Réinitialisé"
        self.message_area.color = ft.Colors.WHITE
        self.update()

    def resoudre(self, event):
        self.message_area.value = "IA en attente..."
        self.update()


def main(page: ft.Page):
    page.title = "Puzzle 8"
    page.window_width = 400
    page.window_height = 550
    page.window_resizable = False
    page.add(Puzzle8())

if __name__ == "__main__":
    ft.app(target=main)