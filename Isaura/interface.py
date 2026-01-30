


"""
same as puzzle8-01.py but we replace the function with a class
"""

import flet as ft
import random
class Puzzle8(ft.Column):
    """
    a Column object suitable for inserting in a Page
    and that has references to the various parts of the game
    """

    def __init__(self):
        """
        build the same widget tree as in v01
        but keep references to the key parts
        as attributes in the object
        """
        squares = [ ft.TextField(str(i)) for i in config[0] ]
        children = [
                # message area
            ft.Row([ message_area := ft.Text("a message area") ]),
                # the 9 squares organized in a 3x3 grid
            ft.GridView(controls=[ft.Container(content=squares[i],bgcolor=ft.Colors.GREEN if content=='0', bgcolor= ft.Colors.INDIGO if content!=0,) for i in range(9)], runs_count=3,),
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
                                        on_click= lambda e: self.recommence(e),)
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
        self.config=config

    # a callback is required to take an event parameter
    def my_callback(self, event):
        """
        an example of a callback that gets called when the start button is clicked
        it just does a few changes as an example
        """
        # with a click the event does not carry much information
        print("in my callback, event=", event)
        # change the message
        self.message_area.value = "button clicked"
        # change the upper-left corner square
        for i in range (9):
            self.squares[i].value = str(next(squares)[i])
        # do not forget to do this otherwise no change will show
        self.update()
    
   

    def melange(self, event):
        """
        an example of a callback that gets called when the start button is clicked
        it just does a few changes as an example
        """
        # with a click the event does not carry much information
        print("in melange , event=", event)
        # change the message
        self.message_area.value = "button clicked"
        # change the upper-left corner square
        for i in range(9):
            self.squares[i].value = str(random.shuffle([0,1,2,3,4,5,6,7,8])[i])
        # do not forget to do this otherwise no change will show
        self.update()
    def recommence(self, event):
        """
        an example of a callback that gets called when the start button is clicked
        it just does a few changes as an example
        """
        # with a click the event does not carry much information
        print("in recommence, event=", event)
        # change the message
        self.message_area.value = "button clicked"
        # change the upper-left corner square
        for i in range(9):
            self.squares[i].value = self.config[0][i]
        # do not forget to do this otherwise no change will show
        self.update()
    def resoudre(self, event):
        """
        an example of a callback that gets called when the start button is clicked
        it just does a few changes as an example
        """
        # with a click the event does not carry much information
        print("in resoudre, event=", event)
        # change the message
        self.message_area.value = "button clicked"
        # change the upper-left corner square
        for i in range(9):
            self.squares[i].value = self.config[-1][i]
        # do not forget to do this otherwise no change will show
        self.update()


def main(page):
    page.title = "Puzzle 8"
    page.window.width = 400
    page.window.resizable = False

    # insert the game widget in the main page
    page.add(Puzzle8())

ft.app(main)