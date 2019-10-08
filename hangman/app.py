from ipywidgets import widgets
import time
from IPython.display import clear_output

class App:
    """
    Contains all of the UI elements for interacting with the game.
    
    Attributes:
        game (HangmanGame): A class containing the Hangman gameplay logic.
        image (HangmanImage): A class which creates the image of the hanging man,
                             one body part at a time following incorrect guesses.
        history (History): A class which stores statistics on completed games to track 
                          player's scores and win percentages.
        start (bool): A flag indicating whether or not to display the start screen.
    """
    def __init__(self, game, image, history, start = False):
        self.game = game
        self.image = image
        self.history = history
        self.word_length = self.game.word_length
        self.difficulty = self.game.difficulty
        self.get_word_length_setter()
        self.get_difficulty_setter()
        self.get_letter_buttons()
        if start:
            self.get_open_screen()
        else:
            self.get_app()
            
    def guess(self, guess):
        """
        Sends the guessed letter or word to the game class and receives a response
        indicating whether or not the guess was correct.
        """
        correct_guess = self.game.guess(guess)
        if not correct_guess:
            self.image.draw_next()
        if self.game.status != 0:
            self.disable_all_letters()
            self.history.add_game(self.player_name, self.game.calculate_score())
        if hasattr(guess, "value"):
            self.add_guessed_word(guess) 
        
    def get_open_screen(self, *args):
        """Displays the opening screen where player enters their name."""
        header = widgets.HTML(f"<h1><font color='black'>Welcome To Hangman!</h1>",
                                                    layout=widgets.Layout(height='auto'))
        self.get_name_field()
        center = self.name_box
        self.name_field.on_submit(self.get_app)
        self.start_button.on_click(self.get_app)
        app = widgets.AppLayout(header=header,center=center)
        clear_output()
        display(app)
        
    def get_hangman_image(self):
        """Builds a widget to display the hangman image."""
        self.hangman_image = widgets.Image(value=self.image.get_encoded_image())
        
    def get_name_field(self):
        """Builds a text field widget for players to enter their name."""
        self.name_field = widgets.Text(placeholder="Enter Your Name")
        self.start_button = widgets.Button(description="Start Game", disabled=True)
        self.name_field.observe(self.enable_start_game_, names=['value'])
        self.name_box = widgets.HBox([self.name_field, self.start_button])
        
    def enable_start_game_(self, _):
        """Checks to see if a name has been entered in the name field."""
        if self.name_field.value != '':
            self.player_name = self.name_field.value
            self.enable_start_game()
            
    def enable_start_game(self):
        """Enables the start game button when a name has been entered."""
        self.start_button.disabled=False
        
    def get_letter_buttons(self):
        """Builds buttons enabling the player to guess each letter of the alphabet"""
        self.letter_buttons = [widgets.Button(description = chr(n),
                                              layout = widgets.Layout(height='25px',
                                                                      width='25px'),
                                              button_style="primary",
                                              tooltip=f"Click to guess {chr(n)}.")\
                               for n in range(97, 97+26)]
        for button in self.letter_buttons:
            button.on_click(self.letter_button_handler)
            button.on_click(self.guess)
            button.on_click(self.get_app)
        self.letter_button_box = widgets.HBox(self.letter_buttons)
        
    def letter_button_handler(self, button):
        """Disables the letter buttons after they have been clicked on."""
        button.disabled = True
        button.tooltip = ""
        
    def enable_all_letter_buttons(self):
        """Reset all letter buttons when a new game is started."""
        for button in self.letter_buttons:
            button.disabled = False
            button.on_click(self.guess)
            button.on_click(self.get_app)
            
    def disable_all_letters(self):
        """Disables all of the letter buttons when the game is over."""
        for button in self.letter_buttons:
            button.disabled = True
            button.tooltip = ""
            
    def get_guess_word(self):
        """Builds a text field widget enabling players to guess the full word."""
        self.guess_word = widgets.Text(placeholder = "Guess the mystery word")
        self.guess_word.layout.width = "260px"
        self.guess_word.layout.margin = "5px 0px 0px 250px"
        self.guess_word.observe(self.enable_guess_word, names=['value'])
        
    def enable_guess_word(self, _):
        """Enforces that the player can only guess a word if it has the same length as the target word."""
        if len(self.guess_word.value) == len(self.game.target_word):
            self.guess_word.on_submit(self.guess)
            self.guess_word.on_submit(self.get_app)
        else:
            self.guess_word.on_submit(self.guess, remove=True)
            self.guess_word.on_submit(self.get_app, remove=True)
    
    def add_guessed_word(self, word):
        """If a player guesses a word, the word gets added to a list and displayed."""
        if not hasattr(self, "guessed_words"):
            self.guessed_words = []
        self.guessed_words.append(word.value)
        
    def get_guess_list(self):
        """Displays a list of words that have been guessed."""
        self.guess_list = [widgets.HTML(f"<h4>{word}</h4>") for word in self.guessed_words]
        self.guess_list = widgets.VBox([widgets.HTML("<h3><u>Guessed Words:</u></h3>")] + self.guess_list)
        self.guess_list.layout.margin = "0px 0px 0px -140px"
        
    def get_word_length_setter(self):
        """Builds a dropdown widget enabling player to set the length of the target word."""
        self.word_length_setter = widgets.Dropdown(description = "Word Length",
                                            options = list(range(4, 11))+['Random'],
                                            value=self.word_length,
                                            layout=widgets.Layout(height="auto",width='180px'))
        self.word_length_setter.observe(self.set_word_length, names=['value'])
        
    def set_word_length(self, _):
        """Sets the value of word length and resets the game."""
        self.word_length = self.word_length_setter.value
        self.reset()
        
    def get_difficulty_setter(self):
        """Builds a dropdown widget enabling player to set the length of the target word."""
        self.difficulty_setter = widgets.Dropdown(description = "Difficulty",
                                       options = list(range(1,11))+['Random'],
                                       value = self.difficulty,
                                       layout=widgets.Layout(height="auto",width='180px'))
        self.difficulty_setter.observe(self.set_difficulty, names=['value'])
        
    def set_difficulty(self, _):
        """Sets the difficulty level and resets the game."""
        self.difficulty = self.difficulty_setter.value
        self.reset()
        
    def get_player_info(self):
        """Gets player info/stats to be displayed in the app."""
        player_name = widgets.HTML(f"<h3> Player: {self.player_name} </h3>",
                                                    layout = widgets.Layout(margin="0px 0px 0px 100px"))
        win_percentage, score = self.history.get_player_stats(self.player_name)
        player_score = widgets.HTML(f"<h4> Total Score: {score} </h4>",
                                                    layout = widgets.Layout(margin="0px 0px 0px 100px"))
        player_win_percentage = widgets.HTML(f"<h4> Win Percentage: {win_percentage} </h4>",
                                                    layout = widgets.Layout(margin="0px 0px 0px 100px"))
        return widgets.VBox([player_name, player_score, player_win_percentage])
    
    def get_scoreboard(self):
        """Creates a button allowing the player to view the historical leaderboard."""
        self.scoreboard = widgets.Button(description="View Scoreboard")
        self.scoreboard.on_click(self.show_scoreboard)
        self.scoreboard.layout.margin = "20px 0px 0px 20px"
        
    def show_scoreboard(self, _):
        """Displays the leaderboard for 4 seconds then returns to the game screen."""
        clear_output()
        self.history.display_scoreboard()
        time.sleep(4)
        clear_output()
        display(self.app)
        
    def get_change_player(self):
        """Creates a button for switching players."""
        self.change_player = widgets.Button(description="Switch Players")
        self.change_player.on_click(self.change_players)
        self.change_player.layout = self.scoreboard.layout
        
    def change_players(self, _):
        """Returns to the home screen and resets the app."""
        self.reset()
        self.get_open_screen()
    
    def get_header(self):
        """
        Builds the header section for the Hangman app.
        
        Contains:
            Mystery Word: A blank word representing the word to be guessed.
                          Letters are revealed following correct guesses.
            Remaining Guesses: The number of guesses remaining before the player loses the game.
            Player Info: The current players' name, score and win percentage.
            
        The appearence of the header section is dependent on the status of the current game.
        """
        info = {-1:['red', self.game.target_word],
                0:['black',' '.join(self.game.word)],
                1:['green', self.game.target_word]}
        mystery_word = widgets.HTML(f"<h1><font color={info[self.game.status][0]}>Mystery Word:\
                                    {info[self.game.status][1]}</h1>",
                                    layout=widgets.Layout(height='auto'))
        remaining_guesses = widgets.HTML(f"<h2><font color='black'>Remaining Guesses:\
                                         {str(self.game.remaining_guesses)}</h2>",
                                         layout=widgets.Layout(height='auto'))
        player_info = self.get_player_info()
        self.header = widgets.HBox([widgets.VBox([mystery_word, remaining_guesses]),player_info])
        
    def get_message(self):
        """A message that is displayed after the game is finished (win/lose)."""
        text = "You Win!" if self.game.status == 1 else "You Lose"
        return widgets.HTML(f"<h1><font color='blue'> {text} </h1>",
                               layout=widgets.Layout(height='auto'))
    
    def get_play_again(self):
        """
        Creates a button allowing the player to play again.
        
        Button only becomes active after the game has ended.
        Clicking the button resets the app.
        """
        play_again = widgets.Button(description="Play Again",
                                         button_style="success")
        play_again.on_click(self.reset)
        return play_again
        
    def get_left_sidebar(self):
        """
        Builds the left sidebar section of the app.
        
        Contains:
            Difficulty Setter
            Word Length Setter
            View Scoreboard Button
            Win/Lose Message (Only after game has ended)
            Play Again Button (Only after game has ended)
        """
        self.get_scoreboard()
        self.get_change_player()
        self.get_guess_word()
        if self.game.status == 0:
            self.left_sidebar = widgets.VBox([self.difficulty_setter,
                                              self.word_length_setter,
                                              self.scoreboard,
                                              self.change_player])
        else:
            message = self.get_message()
            play_again = self.get_play_again()
            self.left_sidebar = widgets.VBox([self.difficulty_setter,
                                              self.word_length_setter,
                                              self.scoreboard,
                                              self.change_player,
                                              message,
                                              play_again])
    
    def get_footer(self):
        """
        Builds the footer section of the app.
        
        Contains:
            Letter Buttons
            Guess Word Field
        """
        footer_text = widgets.HTML("<h3>Click on a letter to guess it or try to guess the full word.</h3>",
                                   layout = widgets.Layout(margin="0px 0px 0px 70px")) 
        self.footer =  widgets.VBox([footer_text, self.letter_button_box, self.guess_word])
        self.footer.layout.margin = "-60px 0px 0px 0px"
        
    def get_app(self, *args):
        """Builds and displays the app using the widgets.AppLayout template."""
        self.get_header()
        self.get_left_sidebar()
        self.get_hangman_image()
        self.get_footer()
        self.app = widgets.AppLayout(header=self.header,
                                     left_sidebar=self.left_sidebar,
                                     center=self.hangman_image,
                                     footer=self.footer)
        if hasattr(self, "guessed_words"):
            self.get_guess_list()
            self.app.right_sidebar = self.guess_list
        clear_output(wait=True)
        display(self.app)
        
    def reset(self, *args):
        """Resets the app to start a new game."""
        if hasattr(self, "guessed_words"):
            del self.guessed_words
        self.image.__init__()
        self.game.__init__(self.word_length, self.difficulty)
        self.get_letter_buttons()
        self.get_app()
