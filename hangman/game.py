from collections import defaultdict
import requests
import json
import random

class HangmanGame:
    """
    Class containing the Hangman game play logic.
    
    Attributes:
        word_length (int or str): The length of the target word.
        difficulty (int or str): The difficulty level of the target word.
    """
    def __init__(self, word_length = 'Random', difficulty = 'Random'):
        self.word_length = word_length
        self.difficulty = difficulty
        self.status = 0 # 0 = in progress, 1 = win, -1 = lose
        self.get_counts()
        self.get_target_word()
        self.remaining_guesses = 6
        self.build_letter_dict()
        self.word = list("_"*len(self.target_word))
    
    def get_counts(self):
        """
        Builds a 2d matrix containing the total number of available words for each
        combination of difficulty and word length. This allows the program to only
        request a single word from the API each time a new game is started.
        """
        if not hasattr(self, "counts"):
            try: 
                with open('counts.json','rb') as f:
                    self.counts = json.load(f)
            except:
                self.counts = [[0 for _ in range(11)] for _ in range(11)]
                for dif in range(1,11):
                    for length in range(2, 11):
                        params = {'minLength':length,
                                'maxLength':length+1,
                                'difficulty':dif}
                        response = requests.get('http://app.linkedin-reach.io/words',
                                             params=params).text
                        if response: 
                            self.counts[dif][length] = len(response.split('\n'))
                with open('counts.json','w') as f:
                    json.dump(self.counts, f)
                    
    def get_word_length_and_difficulty(self):
        """Determines word length and difficulty of target word from player speifications."""
        if self.word_length == "Random":
            min_length = 2
            max_length = 11
        else:
            length_map = {'Short':(2,5),
                          'Medium':(5,8),
                          'Long':(8,11)}
            min_length, max_length = length_map[self.word_length]
        difficulty_map = {'Easy':[1,2,3],
                          'Medium':[4,5,6,7],
                          'Hard':[8,9,10]}
        difficulty_options = difficulty_map[self.difficulty] if self.difficulty != "Random" else list(range(1,11))
        difficulty = random.choice(difficulty_options)
        return min_length, max_length, difficulty
                    
    def get_target_word(self):
        """
        Requests a single word from the API passing the specified difficulty
        and word length as parameters.
        """
        min_length, max_length, difficulty = self.get_word_length_and_difficulty()
        self.current_difficulty = difficulty
        num_available = sum([self.counts[difficulty][length] for length in range(min_length,max_length)])
        start = random.randint(0,num_available-1)
        params = {'minLength':min_length,
                  'maxLength':max_length,
                  'difficulty':difficulty,
                  'start':start,
                  'count':1}
        self.target_word = requests.get('http://app.linkedin-reach.io/words',
                             params=params).text
        self.current_word_length = len(self.target_word)
        
    def build_letter_dict(self):
        """
        Builds a dictionary mapping the letters of the target word to a list 
        of all indices where that letter exists in target word.
        """
        self.letters = defaultdict(list)
        for idx, letter in enumerate(self.target_word):
            self.letters[letter.lower()].append(idx)
            
    def guess(self, guess):
        """
        Verifies the guessed letter or word against the target word.
        
        Decrements self.remaining guesses following an incorrect guess.
        Adjusts self.status when either all letter has been revealed or
        if the player runs out of guesses indicating whether or not the
        player has won or lost the game.
        
        Parameters:
            guess: The letter of word that was guessed by the player.
            
        Returns:
            correct_guess (bool): Indicates whether or not the guess was correct.
        """
        correct_guess = False
        guess = guess.description if guess.description else guess.value
        if len(guess) == 1:
            if guess in self.letters:
                for idx in self.letters[guess]:
                    self.word[idx] = guess
                del self.letters[guess]
                correct_guess = True
            else:
                self.remaining_guesses -= 1
                if self.remaining_guesses == 0:
                    self.status = -1
            if not self.letters:
                self.status = 1
        if len(guess) == len(self.target_word):
            if guess == self.target_word:
                self.status=1
                self.correct_guess = True
            else:
                self.remaining_guesses -= 1
                if self.remaining_guesses == 0:
                    self.status = -1
        return correct_guess
    
    def calculate_score(self):
        """Arbitrary method for calculating the score achieved in a completed game."""
        if self.status == 1:
            score = self.current_difficulty * self.current_word_length * self.remaining_guesses
        else:
            score = 0
        return score
