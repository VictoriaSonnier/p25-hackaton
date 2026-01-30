import flet as ft
import random

class Puzzle8(ft.Column):
    def __init__(self):
        squares = [ft.TextField(str(i),text_align=ft.TextAlign.CENTER,border_color=ft.Colors.INDIGO,color=ft.Colors.WHITE,text_size=20) for i in range(9)]
        children = [
                        ft.Row([ message_area := ft.Text("a message area") ]),
                # the 9 squares organized in a 3x3 grid
            ft.GridView(controls=[ft.Container(content=squares[i], bgcolor= ft.Colors.INDIGO,alignment=ft.Alignment.CENTER) for i in range(9)], runs_count=3,),
                # the bottom buttons
            ft.Row([
                shuffle_button := ft.IconButton(ft.Icons.SHUFFLE,icon_color= ft.Colors.INDIGO,on_click=lambda e: self.melange(e)),
                start_button := ft.IconButton(
                    ft.Icons.NEXT_PLAN, icon_color=ft.Colors.INDIGO,
                    # a callback that gets called when the button is clicked
                    # we could also have simply said
                    # on_click=self.my_callback
                    on_click=lambda e: self.my_callback(e),
                ),
                resolve_button:=ft.IconButton(ft.Icons.CATCHING_POKEMON,icon_color= ft.Colors.INDIGO, 
                                          on_click=lambda e: self.resoudre(e),),
                reset_button:=ft.IconButton(ft.Icons.BAKERY_DINING,icon_color= ft.Colors.INDIGO,
                                        on_click= lambda e: self.recommence(e),),
                check_button := ft.IconButton(
                    ft.Icons.QUESTION_MARK,
                    icon_color=ft.Colors.INDIGO,
                    on_click=lambda e: self.verifier_solubilite(e)
                )
            ])
            
        ]

                
        super().__init__(children)

        self.message_area = message_area
        self.squares = squares
        self.shuffle_button = shuffle_button
        self.start_button = start_button
        self.resolve_button = resolve_button
        self.reset_button = reset_button

    def my_callback(self, event):
        self.message_area.value = "button clicked"
        self.squares[0].value = "X"
        self.update()

    def melange(self, event):
        liste_nombres = list(range(9))
        random.shuffle(liste_nombres)
        for i in range(9):
            self.squares[i].value = str(liste_nombres[i])
        self.message_area.value = "Grille mélangée aléatoirement"
        self.update()

    def verifier_solubilite(self, event):
        actuelle = [int(s.value) if s.value.isdigit() else 0 for s in self.squares]

        def is_even(lst):
            tiles = [t for t in lst if t != 0]
            inversions = 0
            for i in range(len(tiles)):
                for j in range(i + 1, len(tiles)):
                    if tiles[i] > tiles[j]:
                        inversions += 1
            return inversions % 2 == 0

        permutation_parity = is_even(actuelle)
        ind_zero = actuelle.index(0)
        curr_row, curr_col = divmod(ind_zero, 3)
        dist_manhattan = abs(2 - curr_row) + abs(2 - curr_col)
        empty_cell_parity = (dist_manhattan % 2 == 0)

        if permutation_parity == empty_cell_parity:
            self.message_area.value = "La grille est SOLUBLE ! ✅"
            self.message_area.color = ft.Colors.GREEN
        else:
            self.message_area.value = "La grille est INSOLUBLE ! ❌"
            self.message_area.color = ft.Colors.RED
        self.update()

    def recommence(self, event):
        self.message_area.value = "button clicked"
        self.squares[0].value = "X"
        self.update()

    def resoudre(self, event):
        self.message_area.value = "button clicked"
        self.squares[0].value = "X"
        self.update()


def main(page):
    page.title = "Puzzle 8"
    page.window.width = 400
    page.window.resizable = False
    page.add(Puzzle8())

ft.app(main)
