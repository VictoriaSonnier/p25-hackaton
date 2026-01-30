


"""
same as puzzle8-01.py but we replace the function with a class
"""

import flet as ft
import random
import numpy as np
from collections import deque

class Puzzle8(ft.Column):
    """
    a Column object suitable for inserting in a Page
    and that has references to the various parts of the game
    """

    def __init__(self):
        origine=[0,1,2,3,4,5,6,7,8]
        random.shuffle(origine)
        squares = [ ft.TextField(str(i),text_align=ft.TextAlign.CENTER,border_color=ft.Colors.INDIGO,color=ft.Colors.WHITE,text_size=20) for i in origine ]
        board_resolu=[1,2,3,4,5,6,7,8,0]
        children = [
                # message area
            ft.Row([ message_area := ft.Text("a message area") ]),
                # the 9 squares organized in a 3x3 grid
            ft.GridView(controls=[ft.Container(content=squares[i], bgcolor= ft.Colors.INDIGO,alignment=ft.Alignment.CENTER) for i in range(9)],
                                  
                                  runs_count=3,),
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
        # initialize as a Column
        # i.e. call the superclass constructor
        super().__init__(children)

        # keep the references for further use in the methods
        self.message_area = message_area
        self.squares = squares
        self.shuffle_button = shuffle_button
        self.start_button = start_button
        self.resolve_button = resolve_button
        self.reset_button =reset_button
        self.board_resolu=board_resolu
        
        self.origine=origine

    def adjacence(self,i): #cases adjacentes à la case i dans [0,8]
        if i==0:
            return [1,3]
        elif i==1:
            return [0,2,4]
        elif i==2:
            return [1,5]
        elif i==3:
            return [0,4,6]
        elif i==4:
            return [1,3,5,7]
        elif i==5:
            return [2,4,8]
        elif i==6:
            return [3,7]
        elif i==7:
            return [4,6,8]
        elif i==8:
            return [5,7]

    def case_vide(self,board): #renvoie la case vide du board
        print("board", board)
        for i in range(9):
            if board[i]==0:
                return i

    def echange_cases(self,board,i,j): #i et j sont deux cases adjacentes
        new_board = board.copy()
        new_board[i], new_board[j] = new_board[j], new_board[i]
        return new_board

    

    def board_to_string(self,board):
        s=""
        for elt in board:
            s+=str(elt)
        return s


    def Dijkstra(self,init):
        distance_a_init={}
        origine={}
        tinit=tuple(init)
        distance_a_init[tinit]=0
        liste_boards = deque([init])
        while len(liste_boards)!=0:
            board = liste_boards.popleft()
            vide=self.case_vide(board)
            print(vide)
            adj=self.adjacence(vide)
            t=tuple(board)
            for i in range(len(adj)):
                board1=self.echange_cases(board,vide,adj[i])
                t1=tuple(board1)
                if board1==self.board_resolu:
                    distance_a_init[t1]=distance_a_init[t]+1
                    origine[t1]=tuple(board)
                    return origine
                longueur=distance_a_init[t]+1
                if t1 not in distance_a_init:
                    liste_boards.append(board1)
                    distance_a_init[t1]=longueur
                    origine[t1]=tuple(board)
        return None

        self.config=self.findsequence(self.origine)[0]

    def findsequence(self,board_init): #renvoie la liste des mouvements à effectuer pour résoudre le taquin
        Liste_etapes=[self.board_resolu]
        origine=self.Dijkstra(board_init)
        tresolu=tuple(self.board_resolu)
        if not origine :
            return "Pas de solution"
        else:
            while Liste_etapes[0]!=board_init:
                t0=tuple(Liste_etapes[0])
                t=tuple(origine[t0])
                Liste_etapes.insert(0,list(t))
            return Liste_etapes,len(Liste_etapes)
    
    
    def next_move(self, board):
            board1=[int(text.value)for text in board]
            solve=self.findsequence(board)[0][0]
            return solve[1]
        
    # a callback is required to take an event parameter
    def my_callback(self, event):
       
        for i in range (9):
            self.squares[i].value = str(self.next_move(self.squares)[i])
        # do not forget to do this otherwise no change will show
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

    def melange(self, event):
        lst=[i for i in range (9)]
        random.shuffle(lst)
        for i in range(9):
            self.squares[i].value = str(lst[i])
        # do not forget to do this otherwise no change will show
        self.update()
    def recommence(self, event):
        
        for i in range(9):
            self.squares[i].value = self.origine[i]
        # do not forget to do this otherwise no change will show
        self.update()
    def resoudre(self, event):
       
       
        for i in range(9):
            self.squares[i].value = self.config[-1][i]
   
        self.update()


def main(page):
    page.title = "Puzzle 8"
    page.window.width = 400
    page.window.resizable = False

    # insert the game widget in the main page
    page.add(Puzzle8())

ft.app(main)