import flet as ft
import random
from collections import deque

class Puzzle8(ft.Column):
    def __init__(self):
        
        self.board_resolu = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.origine = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(self.origine)
        
        
        self.squares = [
            ft.TextField(
                value=str(i),
                text_align=ft.TextAlign.CENTER,
               
                border_color=ft.Colors.TRANSPARENT if i == 0 else ft.Colors.INDIGO,
                color=ft.Colors.WHITE,
                text_size=20,
                width=60,
                read_only=True
            ) for i in self.origine
        ]

        self.message_area = ft.Text("Prêt")

        self.cells = [
            ft.Container(
                content=self.squares[i], 
                bgcolor=ft.Colors.RED if self.origine[i] == 0 else ft.Colors.INDIGO, 
                alignment=ft.Alignment.CENTER
            ) 
            for i in range(9)
        ]

       
        grid = ft.GridView(controls=self.cells, runs_count=3, expand=True)
        buttons = ft.Row([
            ft.IconButton(ft.Icons.SHUFFLE, on_click=self.melange),
            ft.IconButton(ft.Icons.NEXT_PLAN, on_click=self.my_callback),
            ft.IconButton(ft.Icons.CATCHING_POKEMON, on_click=self.resoudre),
            ft.IconButton(ft.Icons.BAKERY_DINING, on_click=self.recommence),
            ft.IconButton(ft.Icons.QUESTION_MARK, on_click=self.verifier_solubilite)
        ])

        super().__init__([self.message_area, grid, buttons], width=300, height=400)

    def actualiser(self):
        for cell in self.cells:
            is_zero = cell.content.value == "0"
            
            cell.bgcolor = ft.Colors.RED if is_zero else ft.Colors.INDIGO
            
            cell.content.border_color = ft.Colors.TRANSPARENT if is_zero else ft.Colors.INDIGO
        self.update()

    
    def adjacence(self, i):
        adj = {0:[1,3], 1:[0,2,4], 2:[1,5], 3:[0,4,6], 4:[1,3,5,7], 5:[2,4,8], 6:[3,7], 7:[4,6,8], 8:[5,7]}
        return adj.get(i, [])

    def case_vide(self, board):
        for i in range(9):
            if int(board[i]) == 0: return i
        return 0

    def echange_cases(self, board, i, j):
        new_board = list(board)
        new_board[i], new_board[j] = new_board[j], new_board[i]
        return new_board

    def Dijkstra(self, init):
        distance_a_init, origine = {tuple(init): 0}, {}
        liste_boards = deque([init])
        while liste_boards:
            board = liste_boards.popleft()
            vide = self.case_vide(board)
            t = tuple(board)
            for adj_idx in self.adjacence(vide):
                board1 = self.echange_cases(board, vide, adj_idx)
                t1 = tuple(board1)
                if list(board1) == self.board_resolu:
                    origine[t1] = t
                    return origine
                if t1 not in distance_a_init:
                    liste_boards.append(board1)
                    distance_a_init[t1] = distance_a_init[t] + 1
                    origine[t1] = t
        return None

    def findsequence(self, board_init):
        res = self.Dijkstra(board_init)
        if not res: return None
        liste_etapes = [self.board_resolu]
        while list(liste_etapes[0]) != list(board_init):
            parent = res[tuple(liste_etapes[0])]
            liste_etapes.insert(0, list(parent))
        return liste_etapes

    def my_callback(self, event):
        current_board = [int(s.value) for s in self.squares]
        sequence = self.findsequence(current_board)
        if sequence and len(sequence) > 1:
            prochain_etat = sequence[1]
            for i in range(9): self.squares[i].value = str(prochain_etat[i])
            self.actualiser()
        else:
            self.message_area.value = "Terminé !"
            self.update()

    def verifier_solubilite(self, event):
        actuelle = [int(s.value) for s in self.squares]
        tiles = [t for t in actuelle if t != 0]
        inversions = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])
        self.message_area.value = "SOLUBLE !" if inversions % 2 == 0 else "INSOLUBLE !"
        self.message_area.color = ft.Colors.GREEN if inversions % 2 == 0 else ft.Colors.RED
        self.update()

    def melange(self, event):
        lst = [i for i in range(9)]
        random.shuffle(lst)
        for i in range(9): self.squares[i].value = str(lst[i])
        self.actualiser()

    def recommence(self, event):
        for i in range(9): self.squares[i].value = str(self.origine[i])
        self.actualiser()

    def resoudre(self, event):
        for i in range(9): self.squares[i].value = str(self.board_resolu[i])
        self.actualiser()

def main(page: ft.Page):
    page.title = "8-Puzzle"
    page.add(Puzzle8())

ft.app(target=main)