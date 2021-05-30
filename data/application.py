# #################################################################
# import lib's from plugins\import.py - imports all plugins
# #################################################################
from plugin import *
# #################################################################
# define global variables
mines_no = 0
grid_size = 0 # number x number
game_state = 0 # 1 = lost
define_kind_of_field = [0 for i in range(1000)] # Array max 1000 entrys predefined 
# -1 = bomb,  + 1, + 2, + 3 -> neighbour fields of mines

# #################################################################
# Class - Program Code 
# #################################################################
class Program_Code:

    # set randomly mines on the field
    def create_mines():
        global mines_no
        global grid_size
        global define_kind_of_field

        # reset all fields after restart
        for i in range(grid_size * grid_size):
            define_kind_of_field[i] = 0

        count = 0
        i = 1
        while count < mines_no:
            # repeat the this until all mines will be randomly set
            if i > (grid_size * grid_size):
                i = 1
            else:
                i = i + 1
            # Random number from all possible grid positions 
            val = random.randint(0, grid_size*grid_size-1)

            # Place the mine, if it doesn't already have one
            if define_kind_of_field[i] != -1 and define_kind_of_field[i] == val:
                count = count + 1
                define_kind_of_field[i] = -1

    # check mine and increase number for neighbour fields if valid 
    def check_neighbours():
        global grid_size
        global define_kind_of_field
        for y in range(0, grid_size, 1):
            for x in range (1, grid_size + 1, 1):
                if define_kind_of_field[(x + (y * grid_size))] == -1:
                    #check left
                    if x > 1 and define_kind_of_field[(x - 1  + (y * grid_size))] != -1:
                        define_kind_of_field[(x - 1  + (y * grid_size))] = define_kind_of_field[(x - 1 + (y * grid_size))] + 1
                    #check right
                    if x < grid_size and define_kind_of_field[(x + 1 + (y * grid_size))] != -1:
                        define_kind_of_field[(x + 1 + (y * grid_size))] = define_kind_of_field[(x + 1 + (y * grid_size))] + 1
                    #top
                    if y > 0 and define_kind_of_field[(x + ((y - 1)  * grid_size))] != -1:
                        define_kind_of_field[(x + ((y - 1)  * grid_size))] = define_kind_of_field[(x + ((y - 1) * grid_size))] + 1
                    #top-left
                    if y > 0 and x > 1 and define_kind_of_field[(x - 1 + ((y - 1)  * grid_size))] != -1:
                        define_kind_of_field[(x - 1 + ((y - 1)  * grid_size))] = define_kind_of_field[(x - 1 + ((y - 1) * grid_size))] + 1
                    #top-right
                    if y > 0 and x < grid_size and define_kind_of_field[(x + 1 + ((y - 1)  * grid_size))] != -1:
                        define_kind_of_field[(x + 1 + ((y - 1)  * grid_size))] = define_kind_of_field[(x + 1 + ((y - 1) * grid_size))] + 1
                    #down
                    if y < (grid_size - 1) and define_kind_of_field[x + ((y + 1)  * grid_size)] != -1:
                        define_kind_of_field[(x + ((y + 1)  * grid_size))] = define_kind_of_field[(x + ((y + 1) * grid_size))] + 1
                    #down-left
                    if y < (grid_size - 1) and x > 1 and define_kind_of_field[(x - 1 + ((y + 1)  * grid_size))] != -1:
                        define_kind_of_field[(x - 1 + ((y + 1)  * grid_size))] = define_kind_of_field[(x - 1 + ((y + 1)  * grid_size))] + 1
                    #down-right
                    if y < (grid_size - 1) and x < grid_size and define_kind_of_field[(x + 1 + ((y + 1)  * grid_size))] != -1:
                        define_kind_of_field[(x + 1 + ((y + 1)  * grid_size))] = define_kind_of_field[(x + 1 + ((y + 1)  * grid_size))] + 1

# #################################################################
# Class - Create playground with tkinter
# #################################################################
class Application(tk.Frame, Program_Code): # Extend class Program_Code 

    # Frame inside the Application - for better positioning
    def control_area(self):
        self.frame = tk.Frame(self)
        self.frame.config(width = 390, height = 530)
        self.frame.pack(padx=0, pady=5, side="left")

    # Frame - Area with mines
    def game_area(self):
        self.subframe = tk.Frame(self)
        self.subframe.config(width = 380, height = 382)
        self.subframe.place(x=5, y=55)
        self.subframe["bg"] = "#808880"

    # Button - New Game button
    def button_new(self):
        self.new_game = tk.Button(self)
        self.new_game["bg"]= "#c7cbcb"
        self.new_game["fg"]="black"
        self.new_game["text"] = "NEW GAME"
        self.new_game.config(width = 10, height = 2)
        self.new_game.place(x=110, y=470) 
        self.new_game["command"] = self.create_new

    # Button - Game close button
    def button_close(self):
        self.quit = tk.Button(self, text="QUIT", bg="#c7cbcb", fg="red",
                              command=self.master.destroy)
        self.quit.config(width = 10, height = 2)                     
        self.quit.place(x=198, y=470)

    # Button - Create Play Buttons according to class Program_Code
    def mine_fields(self, bomb_image, bomb_image_exploded):
        global grid_size
        global number
        global define_kind_of_field
        global game_state
        Number = 1
        Program_Code.create_mines()
        Program_Code.check_neighbours()
        self.game_button =  [tk.Button(self) for n in range(256)]
        for y in range(58, 58 + (grid_size * 25), 25):
            for x in range (8, 8 + (grid_size * 25), 25):
                self.game_button[Number] = tk.Button(self)
                self.game_button[Number]["bg"]="#c7cbcb"
                self.game_button[Number]["fg"]="#c7cbcb"
                self.game_button[Number].bind("<Button-1>", lambda event, Number = Number: self.change_button_state_click(event, Number, bomb_image, bomb_image_exploded))
                self.game_button[Number].bind("<Button-3>", lambda event, Number = Number: self.change_button_state_mark(event, Number))
                #self.game_button[Number]["command"] = lambda Number = Number: self.change_button_state(Number)
                self.game_button[Number].config(font=("Helvetica", 9, "bold"))
                self.game_button[Number].config(width = 2, height = 1)
                self.game_button[Number].place(x = x, y = y)
                Number = Number + 1

    # Label - simple information label above the game frame 
    # - call from def check_for_all_bombs_marked and def change_button_state_click
    def information_text(self, text):
        self.label = tk.Label(self)
        self.label.config(font=("Arial", 15))
        self.label.config(anchor="center")
        self.label.place(x = 50, y = 10, width = 300, height = 30) 
        self.label["text"] = str(text)

    # Funktion - New Game - call from def button_new
    def create_new(self):
        global grid_size
        global game_state
        self.information_text("")
        for n in range((grid_size * grid_size) + 1):
            self.game_button[n]["bg"]="#c7cbcb"
            self.game_button[n]["fg"]="#c7cbcb"
            self.game_button[n]["text"]=""
            self.game_button[n]["relief"]="raised"
            self.game_button[n]["image"] = ""
            self.game_button[n].config(width = 2, height = 1)
                
        Program_Code.create_mines()
        Program_Code.check_neighbours()
        game_state = 0

    # Funktion - Change Play Buttons after left mouse click - call from def mine_fields
    def change_button_state_click(self, event, Number, bomb_image, bomb_image_exploded):
        global define_kind_of_field
        global game_state
        # disable game buttons after win or game over
        if game_state == 1:
            self.game_button[Number]["state"] = "disabled"
        else:
            self.game_button[Number]["state"] = "normal"
            self.game_button[Number]["bg"]="white"
            if define_kind_of_field[Number] == -1: 
                self.game_button[Number]["image"] = bomb_image_exploded
                self.game_button[Number].config(width = 19, height = 19)
                self.game_button[Number]["command"] = lambda Number = Number: self.change_button_state(Number)
                self.information_text("Game over!")
                self.show_hidden_bombs(Number, bomb_image)
                game_state = 1
            else:
                self.check_neighbours(Number)

    # Funktion - Change Play Buttons after right mouse click - call from def mine_fields
    def change_button_state_mark(self, event, Number):
        self.button_state = self.game_button[Number]["relief"]
        if self.button_state != "sunken":
            self.button_text = self.game_button[Number]["text"]
            if self.button_text == "X":
                self.game_button[Number]["fg"]="#c7cbcb"
                self.game_button[Number]["text"]=""
            else:
                self.game_button[Number]["fg"]="red"
                self.game_button[Number]["text"]="X"
                self.check_for_all_bombs_marked()

    # Funktion - Set Play Buttons to relief ="sunken" - call from def change_button_state_click
    # - this is because sometimes the relief isn't working after button event funtion call
    def change_button_state(self, Number):
        self.game_button[Number]["relief"]="sunken"

    # Funktion - Check neighbours fields for O value - call from def change_button_state_click
    # - self recall funktion
    # - this funktion will every time start to check in all directions as long as the field is zero
    def check_neighbours(self, Number):
        global grid_size
        global define_kind_of_field
        button_state = self.game_button[Number]["relief"]
        if button_state != "sunken":
            self.game_button[Number]["bg"]="white"
            if define_kind_of_field[Number] == 0:
                self.game_button[Number]["fg"]="green"
            else:
                self.game_button[Number]["fg"]="orange"
            self.game_button[Number]["text"]= str(define_kind_of_field[Number])
            self.game_button[Number]["relief"]="sunken"
            self.game_button[Number]["command"] = lambda Number = Number: self.change_button_state(Number)
            if define_kind_of_field[Number] == 0 and Number <= (grid_size * grid_size):
                # recall this funktion self in all diections from the current field

                # define row position
                i = 1
                row = 0 # array pos
                while Number > grid_size * i:
                    i   = i   + 1
                    row = row + 1                
                # check left
                if Number - 1 - (row * grid_size) > 0:
                    self.check_neighbours(Number - 1)
                # check right
                if Number - (row * grid_size) < grid_size: 
                    self.check_neighbours(Number + 1)
                # check top
                if row - 1 > -1:
                    self.check_neighbours(Number - grid_size)
                # check top-left
                if row - 1 > -1:
                    if Number - 1 - (row * grid_size) > 0:
                        self.check_neighbours(Number - 1 - grid_size)
                # check top-right
                if row - 1 > -1:
                    if Number - (row * grid_size) < grid_size:
                        self.check_neighbours(Number + 1 - grid_size)                
                # check down
                if row < grid_size:
                    self.check_neighbours(Number + grid_size)
                # check down-left
                if row < grid_size:
                    if Number - 1 - (row * grid_size) > 0:
                        self.check_neighbours(Number - 1 + grid_size)
                # check down-right
                if row < grid_size:
                    if Number - (row * grid_size) < grid_size:
                        self.check_neighbours(Number + 1 + grid_size)

    # Funktion - to all other hidden bombs after user clicked on a bomb - call from def change_button_state_click
    def show_hidden_bombs(self, Number, bomb_image):
        global grid_size
        for n in range(grid_size * grid_size):
            if define_kind_of_field[n] == -1 and Number != n:
                self.game_button[n]["bg"]="white"
                self.game_button[n]["fg"]="red"
                self.game_button[n]["image"]= bomb_image
                self.game_button[n].config(width = 19, height = 19)
                self.game_button[n]["relief"]="sunken"

    # Funktion - check for user marked all bombs - call from def change_button_state_mark
    def check_for_all_bombs_marked(self):
        global  mines_no
        global grid_size
        global define_kind_of_field
        global game_state
        count = 0
        for n in range(grid_size * grid_size):
            self.button_text = self.game_button[n]["text"]
            if self.button_text == "X" and define_kind_of_field[n] == -1:
                count = count + 1
        if count == mines_no:
            self.information_text("You win!")
            game_state = 1

    # Funktion - self init - start all necessary funktions
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.control_area()
        self.button_new()
        self.button_close()
        self.game_area()
        bomb_image = ImageTk.PhotoImage(Image.open(str(image_folder) + "\Bomb.png").resize((19, 19), Image.ANTIALIAS))
        bomb_image_exploded = ImageTk.PhotoImage(Image.open(str(image_folder) + "\Bomb_Exploded.png").resize((19, 19), Image.ANTIALIAS))
        #bomb_image.convert("RGBA")
        self.mine_fields(bomb_image, bomb_image_exploded)

# #################################################################
# Class - Show application with tkinter
# #################################################################
# - this call is used to call all from anther python file
class Application_Show(Application):
    # Funktion - self init - calls class Application
    def __init__(self):
        root = tk.Tk()
        root.title("Minesweeper")
        root.geometry('400x550')
        root.resizable(width=0, height=0)
        app = Application(master=root)
        app.mainloop()

    # Funktion - called from another python to send parameter
    def parameter(number_of_mines, size_of_grid, folder_of_images):
        global mines_no
        global grid_size
        global image_folder
        mines_no = number_of_mines
        grid_size = size_of_grid
        image_folder = folder_of_images

