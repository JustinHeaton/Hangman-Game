from ipywidgets import widgets
import time
from IPython.display import clear_output

class App:
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
        self.hangman_image = widgets.Image(value=self.image.get_encoded_image())
        
    def get_name_field(self):
        self.name_field = widgets.Text(placeholder="Enter Your Name")
        self.start_button = widgets.Button(description="Start Game", disabled=True)
        self.name_field.observe(self.enable_start_game_, names=['value'])
        self.name_box = widgets.HBox([self.name_field, self.start_button])
        
    def enable_start_game_(self, _):
        if self.name_field.value != '':
            self.player_name = self.name_field.value
            self.enable_start_game()
            
    def enable_start_game(self):
        self.start_button.disabled=False
        
    def get_letter_buttons(self):
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
        button.disabled = True
        button.tooltip = ""
        
    def enable_all_letter_buttons(self):
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
        self.guess_word = widgets.Text(placeholder = "Guess the mystery word")
        self.guess_word.layout.width = "260px"
        self.guess_word.layout.margin = "5px 0px 0px 250px"
        self.guess_word.observe(self.enable_guess_word, names=['value'])
        
    def enable_guess_word(self, _):
        if len(self.guess_word.value) == len(self.game.target_word): # Guess must have same length as target word
            self.guess_word.on_submit(self.guess)
            #self.guess_word.on_submit(self.add_guessed_word)
            self.guess_word.on_submit(self.get_app)
        else:
            self.guess_word.on_submit(self.guess, remove=True)
            #self.guess_word.on_submit(self.add_guessed_word, remove=True)
            self.guess_word.on_submit(self.get_app, remove=True)
    
    def add_guessed_word(self, word):
        """If a player guesses a word, the word gets added to a list and displayed."""
        if not hasattr(self, "guessed_words"):
            self.guessed_words = []
        self.guessed_words.append(word.value)
        
    def get_guess_list(self):
        self.guess_list = [widgets.HTML(f"<h4>{word}</h4>") for word in self.guessed_words]
        self.guess_list = widgets.VBox([widgets.HTML("<h3><u>Guessed Words:</u></h3>")] + self.guess_list)
        self.guess_list.layout.margin = "0px 0px 0px -140px"
        
    def get_word_length_setter(self):
        self.word_length_setter = widgets.Dropdown(description = "Word Length",
                                            options = list(range(4, 11))+['Random'],
                                            value=self.word_length,
                                            layout=widgets.Layout(height="auto",width='180px'))
#         if not hasattr(self, "word_length"):
#             self.word_length_setter.value = self.game.word_length
#         else:
#             self.word_length = self.word_length_setter.value
        self.word_length_setter.observe(self.set_word_length, names=['value'])
        
    def set_word_length(self, _):
        self.word_length = self.word_length_setter.value
        self.reset()
        
    def get_difficulty_setter(self):
        self.difficulty_setter = widgets.Dropdown(description = "Difficulty",
                                       options = list(range(1,11))+['Random'],
                                       value = self.difficulty,
                                       layout=widgets.Layout(height="auto",width='180px'))
#         if not hasattr(self, "difficulty"):
#             self.difficulty_setter.value = self.game.difficulty
#         else:
#             self.difficulty = self.difficulty_setter.value
        self.difficulty_setter.observe(self.set_difficulty, names=['value'])
        
    def set_difficulty(self, _):
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
        text = "You Win!" if self.game.status == 1 else "You Lose"
        return widgets.HTML(f"<h1><font color='blue'> {text} </h1>",
                               layout=widgets.Layout(height='auto'))
    
    def get_play_again(self):
        """
        Creates a button allowing the player to play again.
        Button only becomes active after the game has ended.
        """
        play_again = widgets.Button(description="Play Again",
                                         button_style="success")
        play_again.on_click(self.reset)
        return play_again
        
    def get_left_sidebar(self):
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
        footer_text = widgets.HTML("<h3>Click on a letter to guess it or try to guess the full word.</h3>",
                                   layout = widgets.Layout(margin="0px 0px 0px 70px")) 
        self.footer =  widgets.VBox([footer_text, self.letter_button_box, self.guess_word])
        self.footer.layout.margin = "-60px 0px 0px 0px"
        
    def get_app(self, *args):
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
        if hasattr(self, "guessed_words"):
            del self.guessed_words
        self.image.__init__()
        self.game.__init__(self.word_length, self.difficulty)
        self.get_letter_buttons()
        self.get_app()
        #self.__init__(self.game, self.image, self.history, False)
