# #################################################################
# import lib's from plugins\import.py - imports all plugins
# #################################################################
from plugin import *
# #################################################################
# define global variables
mines_no = 0
grid_size_x = 0 # colums
grid_size_y = 0
game_state = 0 # 1 = lost
define_kind_of_field = [0 for i in range(1000)] # Array max 1000 entrys predefined 
# -1 = bomb,  + 1, + 2, + 3 -> neighbour fields of mines
image_folder = ""
config_file = ""
covererd_fields = 0
hidden_mines = 0
variable = ""
level = 0
# #################################################################
# Class - Program Code 
# #################################################################
class Program_Code:

    # set randomly mines on the field
    def create_mines():
        global mines_no
        global grid_size_x
        global grid_size_y
        global define_kind_of_field

        # reset all fields after restart
        for i in range(grid_size_x * grid_size_y):
            define_kind_of_field[i] = 0

        count = 0
        i = 1
        while count < mines_no:
            # repeat the this until all mines will be randomly set
            if i > (grid_size_x * grid_size_y):
                i = 1
            else:
                i = i + 1
            # Random number from all possible grid positions 
            val = random.randint(0, (grid_size_x*grid_size_x)-1)

            # Place the mine, if it doesn't already have one
            if define_kind_of_field[i] != -1 and define_kind_of_field[i] == val:
                count = count + 1
                define_kind_of_field[i] = -1

    # check mine and increase number for neighbour fields if valid 
    def check_neighbours():
        global grid_size_x
        global grid_size_y
        global define_kind_of_field
        for y in range(0, grid_size_y, 1):
            for x in range (1, grid_size_x + 1, 1):
                if define_kind_of_field[(x + (y * grid_size_x))] == -1:
                    #check left
                    if x > 1 and define_kind_of_field[(x - 1  + (y * grid_size_x))] != -1:
                        define_kind_of_field[(x - 1  + (y * grid_size_x))] = define_kind_of_field[(x - 1 + (y * grid_size_x))] + 1
                    #check right
                    if x < grid_size_x and define_kind_of_field[(x + 1 + (y * grid_size_x))] != -1:
                        define_kind_of_field[(x + 1 + (y * grid_size_x))] = define_kind_of_field[(x + 1 + (y * grid_size_x))] + 1
                    #top
                    if y > 0 and define_kind_of_field[(x + ((y - 1)  * grid_size_x))] != -1:
                        define_kind_of_field[(x + ((y - 1)  * grid_size_x))] = define_kind_of_field[(x + ((y - 1) * grid_size_x))] + 1
                    #top-left
                    if y > 0 and x > 1 and define_kind_of_field[(x - 1 + ((y - 1)  * grid_size_x))] != -1:
                        define_kind_of_field[(x - 1 + ((y - 1)  * grid_size_x))] = define_kind_of_field[(x - 1 + ((y - 1) * grid_size_x))] + 1
                    #top-right
                    if y > 0 and x < grid_size_x and define_kind_of_field[(x + 1 + ((y - 1)  * grid_size_x))] != -1:
                        define_kind_of_field[(x + 1 + ((y - 1)  * grid_size_x))] = define_kind_of_field[(x + 1 + ((y - 1) * grid_size_x))] + 1
                    #down
                    if y < (grid_size_y - 1) and define_kind_of_field[x + ((y + 1)  * grid_size_x)] != -1:
                        define_kind_of_field[(x + ((y + 1)  * grid_size_x))] = define_kind_of_field[(x + ((y + 1) * grid_size_x))] + 1
                    #down-left
                    if y < (grid_size_y - 1) and x > 1 and define_kind_of_field[(x - 1 + ((y + 1)  * grid_size_x))] != -1:
                        define_kind_of_field[(x - 1 + ((y + 1)  * grid_size_x))] = define_kind_of_field[(x - 1 + ((y + 1)  * grid_size_x))] + 1
                    #down-right
                    if y < (grid_size_y - 1) and x < grid_size_x and define_kind_of_field[(x + 1 + ((y + 1)  * grid_size_x))] != -1:
                        define_kind_of_field[(x + 1 + ((y + 1)  * grid_size_x))] = define_kind_of_field[(x + 1 + ((y + 1)  * grid_size_x))] + 1

# #################################################################
# Class - Create playground with tkinter
# #################################################################
class Application(tk.Frame, Program_Code): # Extend class Program_Code 

    # Frame inside the Application - for better positioning
    def control_area(self):
        self.frame = tk.Frame(self)
        self.frame.config(width = ((grid_size_x * 25) + 15), height = ((grid_size_y * 25) + 185))
        self.frame.pack(padx=0, pady=5, side="left")
        self.frame["bg"] = "#b47d49"

    # Button - New Game button
    def button_new(self):
        self.new_game = tk.Button(self)
        self.new_game["bg"]= "#c7cbcb"
        self.new_game["fg"]="black"
        self.new_game["text"] = "NEW GAME"
        self.new_game["command"] = self.create_new
        self.new_game.config(font=("Helvetica", 9, "bold"))
        self.new_game.config(width = 10, height = 2)
        self.new_game.place(x = (((grid_size_x * 25) / 2) - 80), y = ((grid_size_y * 25) + 130)) 

    # Button - Game close button
    def button_close(self):
        self.quit = tk.Button(self)
        self.quit["bg"]= "#c7cbcb"
        self.quit["fg"]="red"
        self.quit["text"] = "QUIT"
        self.quit["command"] = self.master.destroy
        self.quit.config(font=("Helvetica", 9, "bold"))                     
        self.quit.config(width = 10, height = 2)                     
        self.quit.place(x = (((grid_size_x * 25) / 2) + 10), y = ((grid_size_y * 25) + 130))

    # Button - Create Play Buttons according to class Program_Code
    def mine_fields(self, bomb_image, bomb_image_exploded):
        global grid_size_x
        global grid_size_y
        global define_kind_of_field
        global game_state
        start_position_x = 8 # left start point for game button in x
        start_position_y = 112 # left start point for game button in y
        Number = 1
        Program_Code.create_mines()
        Program_Code.check_neighbours()
        self.game_button =  [tk.Button(self) for n in range((grid_size_x + 1) * (grid_size_y + 1))]
        for y in range(start_position_y, start_position_y + (grid_size_y * 25), 25):
            for x in range (start_position_x, start_position_x + (grid_size_x * 25), 25):                   
                self.game_button[Number] = tk.Button(self)
                self.game_button[Number]["fg"] = "#c7cbcb"
                self.game_button[Number].bind("<Button-1>", lambda event, Number = Number: self.change_button_state_click(event, Number, bomb_image, bomb_image_exploded))
                self.game_button[Number].bind("<Button-3>", lambda event, Number = Number: self.change_button_state_mark(event, Number))
                self.game_button[Number].config(font=("Helvetica", 9, "bold"))
                self.game_button[Number].config(width = 2, height = 1)
                self.game_button[Number].place(x = x, y = y)
                Number = Number + 1
        self.set_game_button_color()

    def option_menu_levels(self, level):
        # Option list for pull down menu
        OptionList = [
            "Level1",
            "Level2",
            "Level3",
        ]
        global variable            
        variable = tk.StringVar(self)
        variable.set(OptionList[level])
        level_option = tk.OptionMenu(self, variable, *OptionList)
        level_option["bg"] = "white"
        level_option["fg"] = "black"
        level_option.config(font=("Helvetica", 9, "bold"))
        level_option.config(width = 5, height = 1)
        level_option.config(anchor="ne")
        level_option.place(x = 10, y = 15)
        variable.trace('w', self.option_menu_clicked)

    # Option Menu for changing levels
    def option_menu_clicked(self, name, index, mode):
        # read from file
        config_game_modi = ConfigParser()
        config_game_modi.read(config_file)

        # get the section
        start_level = config_game_modi["start_level"]

        # update the level
        start_level["level"] = ("{}".format(variable.get()))

        # write changes back to file
        with open(config_file, 'w') as conf:
            config_game_modi.write(conf)

        # restart minesweeper
        os.startfile("minesweeper.py")

        # close the old application
        self.master.destroy()

    # Label - Head design - with Shovel image
    def head_design(self, shovel_image):
        self.label_lower = tk.Label(self)
        self.label_lower.config(font=("Helvetica", 1, "bold"))
        self.label_lower.config(width = str((grid_size_x * 25) + 15), height = 45)
        self.label_lower.config(anchor="nw")
        self.label_lower.place(x = 0, y = 5)
        self.label_lower["text"] = "text"
        self.label_lower["bg"] = "#7cfc00"

        self.label_image = tk.Label(self)
        self.label_image["image"] = shovel_image
        self.label_image["bg"] = "#2e9afe"
        self.label_image["fg"] = "#2e9afe"
        self.label_image.bind("<Button-1>", lambda event: self.head_design_image(event, shovel_image))
        self.label_image.config(font=("Helvetica", 9, "bold"))
        self.label_image.config(width = str((grid_size_x * 25) + 15), height = 80)
        self.label_image.config(anchor="ne")
        self.label_image.place(x = 0, y = 5)

    # Label - Show number of covered fields
    def covered_fields(self, count_direction):
        global covererd_fields
        if count_direction == "=":
            covererd_fields = (grid_size_x * grid_size_y)
            self.label_fields = tk.Label(self)
            self.label_fields["borderwidth"] = 1
            self.label_fields["text"] = str(covererd_fields)
            self.label_fields["bg"] = "white"
            self.label_fields["fg"] = "black"
            self.label_fields.config(font=("Helvetica", 12, "bold"))
            self.label_fields.config(width = 5, height = 1)
            self.label_fields.config(anchor="nw")
            self.label_fields.place(x = 10, y = 55)
            covererd_fields = (grid_size_x * grid_size_y)
        elif count_direction == "+" or count_direction == "-":
            covererd_fields = covererd_fields - 1
            self.label_fields["text"] = str(covererd_fields) 
        else:
            covererd_fields = (grid_size_x * grid_size_y)
            self.label_fields["text"] = str(covererd_fields)

    # Label - Show number of unmarked bombs
    def number_unmarked_bombs(self, count_direction):
        global hidden_mines
        if count_direction == "=":
            hidden_mines = mines_no
            self.label_bombs = tk.Label(self)
            self.label_bombs["borderwidth"] = 1
            self.label_bombs["text"] = str(hidden_mines)
            self.label_bombs["bg"] = "white"
            self.label_bombs["fg"] = "black"
            self.label_bombs.config(font=("Helvetica", 12, "bold"))
            self.label_bombs.config(width = 5, height = 1)
            self.label_bombs.config(anchor="nw")
            self.label_bombs.place(x = 80, y = 55)
        elif count_direction == "+" or count_direction == "-":
            if count_direction == "-":
                hidden_mines = hidden_mines - 1
            elif count_direction == "+":
                hidden_mines = hidden_mines + 1
            self.label_bombs["text"] = str(hidden_mines) 
        else:
            hidden_mines = mines_no
            self.label_bombs["text"] = str(hidden_mines)       

    # Label - simple information label above the game frame 
    # - call from def check_for_all_bombs_marked and def change_button_state_click
    def information_text(self, text):
        if text == "":
            self.label.destroy()
        else:
            self.label = tk.Label(self)
            self.label.config(font=("Helvetica", 16, "bold"))
            self.label.config(anchor="center")
            self.label.place(x = (((grid_size_x / 2) * 25) - 93), y = (((grid_size_y / 2) * 25) + 97), width = 200, height = 30) 
            self.label["text"] = str(text)
            self.label["bg"] = "#2e9afe"

    # Function to show image - for a reason I don't know tkinter needs an event to show images
    def head_design_image(self, event, shovel_image):
        pass

    # Funktion - Set game button color
    def set_game_button_color(self):
        global grid_size_x
        global grid_size_y
        Number = 1
        color_toggle = 0
        for y in range(1, grid_size_y + 1, 1):
            for x in range(1, grid_size_x + 1, 1):
            # check for grid_size_x is even or uneven
                if x == 1:
                    num = int(grid_size_x)
                    if (num % 2) == 0 and color_toggle == 1:
                        color_toggle = 0
                    elif (num % 2) == 0 and color_toggle == 0:
                        color_toggle = 1
                            
                if color_toggle == 0:
                    self.game_button[Number]["bg"]="#caff70"
                    color_toggle = 1
                else:
                    self.game_button[Number]["bg"]="#7cfc00"
                    color_toggle = 0
                Number = Number + 1

    # Funktion - New Game - call from def button_new
    def create_new(self):
        global grid_size_x
        global grid_size_y
        global game_state
        self.information_text("")
        for n in range((grid_size_x * grid_size_y) + 1):
            self.game_button[n]["bg"]="#c7cbcb"
            self.game_button[n]["fg"]="#c7cbcb"
            self.game_button[n]["text"]=""
            self.game_button[n]["relief"]="raised"
            self.game_button[n]["image"] = ""
            self.game_button[n].config(width = 2, height = 1)
        self.set_game_button_color()
                
        Program_Code.create_mines()
        Program_Code.check_neighbours()
        game_state = 0
        self.covered_fields(" ")
        self.number_unmarked_bombs(" ")

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
                self.number_unmarked_bombs("+")
            else:
                self.game_button[Number]["fg"]="red"
                self.game_button[Number]["text"]="X"
                self.number_unmarked_bombs("-")
                self.check_for_all_bombs_marked()

    # Funktion - Set Play Buttons to relief ="sunken" - call from def change_button_state_click
    # - this is because sometimes the relief isn't working after button event funtion call
    def change_button_state(self, Number):
        self.game_button[Number]["relief"]="sunken"

    # Funktion - Check neighbours fields for O value - call from def change_button_state_click
    # - self recall funktion
    # - this funktion will every time start to check in all directions as long as the field is zero
    def check_neighbours(self, Number):
        global grid_size_x
        global grid_size_y
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
            self.covered_fields("-")
            if define_kind_of_field[Number] == 0 and Number <= (grid_size_x * grid_size_y):
                # recall this funktion self in all diections from the current field

                # define row position
                i = 1
                row = 0 # array pos
                while Number > grid_size_x * i:
                    i   = i   + 1
                    row = row + 1                
                # check left
                if Number - 1 - (row * grid_size_x) > 0:
                    self.check_neighbours(Number - 1)
                # check right
                if Number - (row * grid_size_x) < grid_size_x: 
                    self.check_neighbours(Number + 1)
                # check top
                if row - 1 > -1:
                    self.check_neighbours(Number - grid_size_x)
                # check top-left
                if row - 1 > -1:
                    if Number - 1 - (row * grid_size_x) > 0:
                        self.check_neighbours(Number - 1 - grid_size_x)
                # check top-right
                if row - 1 > -1:
                    if Number - (row * grid_size_x) < grid_size_x:
                        self.check_neighbours(Number + 1 - grid_size_x)                
                # check down
                if row < grid_size_y:
                    self.check_neighbours(Number + grid_size_x)
                # check down-left
                if row < grid_size_y:
                    if Number - 1 - (row * grid_size_x) > 0:
                        self.check_neighbours(Number - 1 + grid_size_x)
                # check down-right
                if row < grid_size_y:
                    if Number - (row * grid_size_x) < grid_size_x:
                        self.check_neighbours(Number + 1 + grid_size_x)

    # Funktion - to all other hidden bombs after user clicked on a bomb - call from def change_button_state_click
    def show_hidden_bombs(self, Number, bomb_image):
        global grid_size_x
        global grid_size_y
        for n in range((grid_size_x * grid_size_y) + 1):
            if define_kind_of_field[n] == -1 and Number != n:
                self.game_button[n]["bg"]="white"
                self.game_button[n]["fg"]="red"
                self.game_button[n]["image"]= bomb_image
                self.game_button[n].config(width = 19, height = 19)
                self.game_button[n]["relief"]="sunken"

    # Funktion - check for user marked all bombs - call from def change_button_state_mark
    def check_for_all_bombs_marked(self):
        global mines_no
        global grid_size_x
        global grid_size_y
        global define_kind_of_field
        global game_state
        count = 0
        for n in range(grid_size_x * grid_size_y):
            self.button_text = self.game_button[n]["text"]
            if self.button_text == "X" and define_kind_of_field[n] == -1:
                count = count + 1
        if count == mines_no:
            self.information_text("You win!")
            game_state = 1

    # Funktion - self init - start all necessary funktions
    def __init__(self, master=None):
        global image_folder
        super().__init__(master)

        # define game images
        bomb_image = ImageTk.PhotoImage(Image.open(str(image_folder) + "\Bomb.png").resize((19, 19), Image.ANTIALIAS))
        bomb_image_exploded = ImageTk.PhotoImage(Image.open(str(image_folder) + "\Bomb_Exploded.png").resize((19, 19), Image.ANTIALIAS))
        shovel_image = ImageTk.PhotoImage(Image.open(str(image_folder) + "\Shovel.png").resize((171, 95), Image.ANTIALIAS))
        self.master = master
        self.pack()
        self.control_area()
        self.head_design(shovel_image)
        self.option_menu_levels(level)
        self.covered_fields("=")
        self.number_unmarked_bombs("=")
        self.button_new()
        self.button_close()
        self.mine_fields(bomb_image, bomb_image_exploded)

# #################################################################
# Class - Show application with tkinter
# #################################################################
# - this call is used to call all from anther python file
class Application_Show(Application):
    # Funktion - self init - calls class Application
    def __init__(self):
        global image_folder

        root = tk.Tk()
        root.iconbitmap(str(image_folder) + "\Bomb.ico") 
        root.title("Minesweeper")
        Geometry = str((grid_size_x * 25) + 15) + "x" + str((grid_size_y * 25) + 185)
        root.geometry(Geometry)
        root.resizable(width=0, height=0)
        app = Application(master=root)
        app.mainloop()

    # Funktion - called from another python to send parameter
    def parameter(number_of_mines, size_of_grid_x, size_of_grid_y, folder_of_images, file_of_config, start_level):
        global mines_no
        global grid_size_x
        global grid_size_y
        global image_folder
        global config_file
        global level
        mines_no     = number_of_mines
        grid_size_x  = size_of_grid_x
        grid_size_y  = size_of_grid_y
        image_folder = folder_of_images
        config_file = file_of_config
        level = start_level - 1

