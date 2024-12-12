from tkinter import *

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


class GameGUI:
    """
    Class creates a user interface (GUI) which constantly changes based on the
    users actions. The class creates everything the user sees and calls other
    classes.

    Attributes:
    root (tkinter.Tk): The main tkinter window.
    __image (tkinter.PhotoImage): The boat image used in the GUI.
    __resized_image (tkinter.PhotoImage): The resized version of the boat
    image.
    __image_label (tkinter.Label): The label displaying the boat image in
    the GUI.
    __introduction (tkinter.Label): The label displaying the welcome message in
     the main menu.
    __enter_filename (tkinter.Label): The label prompting the user to enter a
    filename.
    __filename_entry (tkinter.Entry): The entry widget for typing the filename.
    __message_label (tkinter.Label): The label displaying messages or error
    notifications.
    __start_game_button (tkinter.Button): The button to start the game with the
     entered filename.
    game (Game): The instance of the Game class associated with the GUI.
    __victory_screen (VictoryScreen): The instance of the VictoryScreen class.

    """
    def __init__(self):
        """Creates user interface without "__" because we need to be able to
         use it in other classes as we play the game."""
        self.root = Tk()
        self.root.title("Battleship Game By Tatu & Alex")  # Title of the GUI.
        self.root.geometry("400x400")  # The size of the GUI on launch.

        # The boat image in folder and resized to fit the menu.
        self.__image = PhotoImage(file="boat.gif")
        self.__resized_image = self.__image.subsample(5, 5)
        self.__image_label = Label(self.root, image=self.__resized_image)
        self.__image_label.grid(row=1, column=4, columnspan=6, sticky="nsew")

        # Introduction text in the main menu.
        self.__introduction = (Label(self.root,
                                     text="Welcome to Battleship!\n"
                                          " (Type \"example.txt\" "
                                          "to play the default version)"))
        self.__introduction.grid(row=2, column=4, columnspan=6, sticky="nsew")

        # Configure row and column
        for i in range(11):  # Increased to 11 for row and column labels
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        # Calls the create_menu method
        self.create_menu()

        # Creates all the necessary texts and entry box for filename and space
        # for an error message.
        self.__enter_filename = Label(self.root, text="Enter a filename:")
        self.__enter_filename.grid(row=10, column=0, columnspan=8,
                                   sticky="nsew")
        self.__filename_entry = Entry(self.root)
        self.__filename_entry.grid(row=11, column=0, columnspan=8,
                                   sticky="nsew")
        self.__message_label = Label(self.root, text="", wraplength=300)
        self.__message_label.grid(row=12, column=0, columnspan=11,
                                  sticky="nsew")

        # Creates a button that calls the method which starts the game.
        self.__start_game_button = Button(self.root, text="Start Game",
                                          command=self.start_game)
        self.__start_game_button.grid(row=11, column=8, columnspan=8,
                                      sticky="nsew")

        # Creates attributes .game and __victory_screen
        self.game = None
        self.__victory_screen = None

        # Puts everything on the display
        self.root.mainloop()

    def create_menu(self):
        """
        Method creates a menu and adds "Quit" and "Restart" buttons to it.
        """
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)

        file_menu = Menu(main_menu)
        main_menu.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="Quit", command=self.root.destroy)
        file_menu.add_command(label="Restart", command=self.restart)

    def restart(self):
        """
        Method destroys the current GUI and creates a new one.
        """
        self.root.destroy()
        GameGUI()

    def start_game(self):
        """
        Method initiates the game based on the entered filename.
        """
        # Get the filename from the entry widget
        filename = self.__filename_entry.get()
        
        if filename:
            if self.game and not self.game.valid_file:
                # Clear previous invalid file message
                self.clear_message()
                # Hide all the buttons in the GUI
            self.__filename_entry.grid_forget()
            self.__start_game_button.grid_forget()
            self.__enter_filename.grid_forget()
            self.__image_label.grid_forget()
            self.__introduction.grid_forget()
            self.game = Game(self, filename)
            
            if self.game.setup():
                # If setup is successful, start the game
                pass
            else:
                # If setup failed, clear the entry slot and create the
                # necessary button, texts and image back
                self.__filename_entry.delete(0, END)
                self.__filename_entry.grid(row=11, column=0, columnspan=8,
                                           sticky="nsew")

                self.__start_game_button.grid(row=11, column=8, columnspan=8,
                                              sticky="nsew")
                self.__resized_image = self.__image.subsample(5, 5)
                self.__image_label = Label(self.root,
                                           image=self.__resized_image)
                self.__image_label.grid(row=1, column=4, columnspan=8,
                                        sticky="nsew")
                self.__enter_filename = Label(self.root,
                                              text="Enter a filename:")
                self.__enter_filename.grid(row=10, column=0, columnspan=8,
                                           sticky="nsew")
                self.__introduction = Label(self.root,
                                            text="Welcome to Battleship!\n"
                                            " (Type \"example.txt\" "
                                            "to play the default version)")
                self.__introduction.grid(row=2, column=4, columnspan=8,
                                         sticky="nsew")
                
        else:
            # If entry slot is empty, it calls for clear message method and
            # gives a new error message
            self.clear_message()
            self.display_message("Please enter a filename!")

    def display_message(self, message):
        """
        Changes the message (error etc.) shown in the GUI.

        :param message, str message to the user.
        """
        self.__message_label.config(text=message)

    def clear_message(self):
        """
        Clears the message
        """
        self.__message_label.config(text="")

    def show_victory_screen(self):
        """
        Shows the victory screen if the user won.
        """
        if not self.__victory_screen:
            self.__victory_screen = VictoryScreen(self)


class Square(Button):
    """
    Represents a square in the Battleship game grid.

    Inherits Button class from the tkinter.

    :param master, tkinter.Tk The master tkinter window
    :param x, int The x-coordinate of the square on the game grid.
    :param y, int The y-coordinate of the square on the game grid.
    :param game, Game The Game instance associated with the square.

    Attributes:
    __x (int): The x-coordinate of the square on the game grid.
    __y (int): The y-coordinate of the square on the game grid
    """
    def __init__(self, master, x, y, game):
        super().__init__(master, text="", width=2, height=1, background='cyan',
                         foreground='black',
                         command=lambda: game.square_clicked(x, y))
        self.__x = x
        self.__y = y


class Game:
    """
    Class representing the game logic and state in the Battleship game.
    This class manages the setup of the game, including reading ship data from
    a file, creating the game board, and handling player moves. It tracks the
    status of each ship, the coordinates that have been hit, and the overall
    game state.

    Attributes:
    gui (GameGUI): The class GameGUI.
    __board_buttons (list): A list representing the game board buttons.
    __ships (list): A list to store Ship objects representing the ships in
    the game.
    __used_coordinates (set): A set to store the coordinates already occupied
    by ships.
    __hit_coordinates (set): A set to store the coordinates where shots have
    been hit.
    __miss_coordinates (set): A set to store the coordinates of misses.
    __ships_up (set): A set to store Ship objects that are still up.
    __filename (str): The name of the file containing ship data.
    valid_file (bool): Flag to check if the file is valid.
    """
    def __init__(self, gui, filename):
        """
        :param gui, the class GameGUI.
        :param filename, str the name of the file.
        """
        self.gui = gui
        self.__board_buttons = []
        self.__ships = []
        self.__used_coordinates = set()
        self.__hit_coordinates = set()
        self.__miss_coordinates = set()
        self.__ships_up = set()
        self.__filename = filename
        self.valid_file = False

    def setup(self):
        """
        Initiates the game setup, including reading the file, creating the
        board, and prints it.
        """
        self.valid_file = self.read_file()
        
        if self.valid_file:
            self.create_board()
            self.print_board()
            
        return self.valid_file

    def read_file(self):
        """
        Reads ship data from a file and initializes Ship objects.
        """
        while True:
            try:
                data_file = open(self.__filename, 'r')
                for row in data_file:
                    marks = row.rstrip().split(";")
                    name = marks[0]
                    coordinates = marks[1:]
                    for coordinate in coordinates:
                        if len(coordinate) != 2 or coordinate[
                            0] not in LETTERS or int(
                                coordinate[1]) not in NUMBERS:
                            raise ValueError
                        elif coordinate in self.__used_coordinates:
                            raise ValueError

                        self.__used_coordinates.add(coordinate)
                    ship = Ship(name, coordinates)
                    self.__ships.append(ship)
                    self.__ships_up.add(ship)
                break  # If the file reading is successful, exit the loop
            except (ValueError, OSError, FileNotFoundError):
                self.gui.display_message("Please enter a valid file.")
                return False  # Indicate a problem with the file reading

        return True

    def create_board(self):
        """
        Creates the game board with labels for rows and columns.
        """
        for x in range(10):
            row_buttons = []

            # Add labels for row numbers (right side)
            label = Label(self.gui.root, text=str(NUMBERS[x]))
            label.grid(row=x, column=11, sticky="nsew")

            # Make buttons fill available space
            for y in range(10):
                square = Square(self.gui.root, x, y, self)
                square.grid(row=x, column=y + 1, sticky="nsew")
                row_buttons.append(square)
            self.__board_buttons.append(row_buttons)

        # Add labels for column letters (bottom side)
        for y in range(10):
            label = Label(self.gui.root, text=LETTERS[y])
            label.grid(row=11, column=y + 1, sticky="nsew")

    def print_board(self):
        """
        Updates the displayed board based on ship status and player moves.
        Uses the method coordinate_to_indices to know where to put the marks
        "X" and "*" and the first letters.
        """
        for ship in self.__ships:
            if ship.is_sunk():
                for coord in ship.get_coordinates():
                    x, y = self.coordinate_to_indices(coord)
                    self.__board_buttons[x][y]['text'] = (
                        ship.get_first_letter())
            else:
                for coord in ship.get_shot_coordinates():
                    x, y = self.coordinate_to_indices(coord)
                    self.__board_buttons[x][y]['text'] = 'X'

        for coord in self.__miss_coordinates:
            x, y = self.coordinate_to_indices(coord)
            self.__board_buttons[x][y]['text'] = '*'

    def square_clicked(self, x, y):
        """
        Handles a player click on a game square, processing hits or misses.

        :param x, x coordinate.
        :param y, y coordinate.
        """
        coord = self.indices_to_coordinate(x, y)
        # Checks if the coordinate has already been shot at.
        if coord in self.__hit_coordinates or coord in self.__miss_coordinates:
            self.gui.display_message("Location has already been shot at!")
        else:
            hit = False
            for ship in self.__ships_up:
                if coord in ship.get_coordinates():
                    self.__hit_coordinates.add(coord)
                    ship.shot_hit(coord)
                    hit = True
                    if ship.is_sunk():
                        self.gui.display_message(
                            f"You sank a {ship.get_name()}!")
                        self.__ships_up.remove(ship)
                        # Check if all ships are sunk
                        if not self.__ships_up:
                            self.print_board()
                            self.gui.display_message(
                                "Congratulations! You sank all enemy ships.")
                            self.gui.show_victory_screen()
                            return
                    break

            if not hit:
                self.__miss_coordinates.add(coord)

            # Updates the game board.
            self.print_board()

    def coordinate_to_indices(self, coord):
        """
        Converts a coordinate to row and column indices.
        :param coord, str coordinates (x,y)
        :return: returns x and y as list indexes.
        """
        letter, number = coord[0], int(coord[1])
        x = NUMBERS.index(number)
        y = LETTERS.index(letter)
        return x, y

    def indices_to_coordinate(self, x, y):
        """
        Converts row and column indices to a coordinate.
        :param x, x coordinate.
        :param y, y coordinate.
        :return: returns coordinates.
        """
        letter = LETTERS[y]
        number = NUMBERS[x]
        return f"{letter}{number}"


class Ship:
    """
    Class creates an own object for every ship. This class represents a ship
    in the battleship game.

     Attributes:
     __name: (str) The name of the ship.
     __coordinates: (list) List of coordinates occupied by the ship
     __shot_coordinates: (list) List of coordinates where the ship has
     been shot.
    """
    def __init__(self, name, coordinates):
        """
        :param name, str name of the ship.
        :param coordinates, str coordinates of the ship.
        """
        self.__name = name
        self.__coordinates = coordinates
        self.__shot_coordinates = []

    def get_name(self):
        """
        :return: the name(str) of the ship.
        """
        return self.__name

    def get_first_letter(self):
        """
        :return: the first letter(str) of the ship's name.
        """
        return self.__name[0].upper()

    def shot_hit(self, shot):
        """
        Checks if the shot's coordinates are in the ship's coordinates.
        If it is, it adds it to the __shot.coordinates list.
        :param shot, str player's coordinate guess.
        """
        if shot in self.__coordinates:
            self.__shot_coordinates.append(shot)

    def is_sunk(self):
        """
        Checks if the ship is sunk using "set" command so that the order does
        not matter.
        :return: True or False.
        """
        return set(self.__shot_coordinates) == set(self.__coordinates)

    def get_coordinates(self):
        """
        :return: the coordinates(list) of the ship.
        """
        return self.__coordinates

    def get_shot_coordinates(self):
        """
        :return: the coordinates(list) where the ship has been shot.
        """
        return self.__shot_coordinates


class VictoryScreen:
    """
        Class representing the victory screen displayed when the player wins
        the game. This class creates a pop-up window (Toplevel) with a
        winning message, options to quit or play again, and a chance to restart
        the game.

        Attributes:
        gui (GameGUI): The class GameGUI.
        root (tkinter.Toplevel): Pop-up window.
        __label (tkinter.Label): The label displaying the winning message.
        __quit (tkinter.Button): The button to quit the game.
        __restart (tkinter.Button): The button to restart the game.
        """
    def __init__(self, gui):
        """
        :param gui, the class GameGUI.
        """
        self.gui = gui
        self.root = Toplevel(gui.root)
        self.root.title("Victory!")

        self.__label = Label(self.root,
                             text="Congratulations! You sank all enemy ships.",
                             font=16)
        self.__label.pack(pady=20)

        self.__quit = Button(self.root, text="Quit",
                             command=self.gui.root.destroy)
        self.__quit.pack(pady=10)
        self.__restart = Button(self.root, text="Play again?",
                                command=self.restart)
        self.__restart.pack(pady=5)

        self.root.mainloop()

    def restart(self):
        """
        Destroys the previous GUI and starts again.
        """
        self.gui.root.destroy()
        GameGUI()


def main():
    """
    Calls the GameGUI class.
    """
    GameGUI()


if __name__ == "__main__":
    main()
