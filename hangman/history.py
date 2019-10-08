import pandas as pd
from ipywidgets import widgets

class History:
    """Provides functionality for saving stats visualizing leaderboard."""
    def __init__(self):
        self.load_history()
        self.get_scoreboard()
    
    def load_history(self):
        """Loads the history from a saved json file"""
        if not hasattr(self, "history"):
            try:
                self.history = pd.read_json('history.json')
            except:
                self.history = pd.DataFrame(columns=['Player','Games Played','Games Won','Total Score'])
                
    def add_game(self, user, score):
        """Update the history with the result of a completed game and save results to json file."""
        if user in self.history.Player.values:
            idx = self.history[self.history.Player == user].index
            self.history.loc[idx, 'Games Played'] += 1
            self.history.loc[idx, 'Games Won'] += int(score>0)
            self.history.loc[idx, 'Total Score'] += score
        else:
            self.history.loc[len(self.history)]=[user, 1, int(score>0), score]
        self.get_scoreboard()
        self.history.to_json('history.json')
    
    def display_table(self):
        display(self.history)
        
    def get_scoreboard(self):
        """Generate a scoreboard with statistics for each player"""
        self.scoreboard = self.history.copy()
        self.scoreboard['Win Percentage'] = ((self.scoreboard['Games Won']/self.scoreboard['Games Played'])*100)
        self.scoreboard['Win Percentage'] = [f"{win_percentage:.2f}%" for win_percentage\
                                             in self.scoreboard['Win Percentage']]
        
    def get_player_stats(self, player):
        """Get the historical stats for a particular player"""
        try:
            idx = self.scoreboard[self.scoreboard.Player == player].index
            win_percentage = self.scoreboard.loc[idx, "Win Percentage"] 
            score = self.scoreboard.loc[idx, "Total Score"] 
            return win_percentage.values[0], score.values[0]
        except:
            return '0%', 0
        
    def display_scoreboard(self):
        display(self.scoreboard.sort_values(by="Total Score",ascending=False).iloc[:10].style.hide_index())
