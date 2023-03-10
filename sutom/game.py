import random
from spellchecker import SpellChecker
from os import system, name

MAXTURNNUMBER: int = 6
LANGUAGE: str = "fr"

from sutom.dictionnary import  words
class Game:
    _word_to_find: str
    word_length: int
    tested_words: list[list[str]]
    tested_letters: list[str]
    _letters_hidden_word_not_found: list[bool]
    _letters_user_word_not_used: list[bool]
    word_is_not_complete: bool
    number_of_turn_passed: int
    dictionary: SpellChecker

    def __init__(self):
        pass

    def initialize(self):
        """Initialize the game"""
        self._word_to_find = words[random.randint(0, len(words) - 1)]
        self.word_length = len(self._word_to_find)
        self.number_of_turn_passed = 0
        self._set_first_try()
        self.word_is_not_complete = True
        self.dictionary = SpellChecker(language=LANGUAGE)


    def _set_first_try(self):
        """Create a list based on letter number"""
        self.tested_words = [[self._word_to_find[0]]]
        for i in range(0, self.word_length - 1):
            self.tested_words[0].append("_")

    def launch_game(self):
        """Launch game"""
        self._loop()
        self._finish_end_game()

    def _loop(self):
        """Game loop"""
        while self.word_is_not_complete and \
                self.number_of_turn_passed < MAXTURNNUMBER :
            print(f"Turn lefts: {MAXTURNNUMBER-self.number_of_turn_passed}")
            self.print_tries()
            user_word: str = self._get_word_from_user()
            self.tested_words.append(self._test_word(user_word))
            self.clear()
            self.number_of_turn_passed += 1

    def _get_word_from_user(self) -> str:
        """Try to get a correct new word from user"""
        result_word: str = "a"
        while len(result_word) != self.word_length \
                or len(self.dictionary.known([result_word])) == 0:
            result_word = input("Entrez un mot : \n")
            if len(self.dictionary.known([result_word])) == 0:
                print("Ce n'est pas un mot fran??ais")
                continue
            if len(result_word) != self.word_length :
                print("Ce n'est pas un mot de la bonne longueur")
        return result_word

    def _finish_end_game(self):
        """Shows the infos of the end of the game"""
        self.print_tries()
        if self.word_is_not_complete :
            print(f"\033[91mRat??, le mot ??tait : {self._word_to_find}\033[00m")
        else:
            print(f"\033[92mBravo, r??ussi en {self.number_of_turn_passed} "
                  f"coups sur {MAXTURNNUMBER}\033[00m")

    def print_tries(self):
        """Prints all the tries made by user"""
        for i in range(0, len(self.tested_words)):
            print(" ".join(self.tested_words[i]))

    def clear(self):
        """clears the console"""
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def _test_word(self, user_word: str) -> list[str]:
        """Test the word to find correspondances"""
        result : list[str] = list(user_word)
        self._letters_hidden_word_not_found: list[bool] = self._get_test_list()
        self._letters_user_word_not_used: list[bool] = self._get_test_list()
        self._find_all_matches_same_index(user_word, result)
        if any(self._letters_hidden_word_not_found):
            self._find_lesser_matches(user_word, result)
        else:
            self.word_is_not_complete = False
        return result


    def _find_all_matches_same_index(self, user_word:str, result: list[str]):
        """Find all same index matches and show it"""
        for i in range(0, self.word_length):
            if user_word[i] == self._word_to_find[i]:
                self._letters_hidden_word_not_found[i] = False
                self._letters_user_word_not_used[i] = False
                result[i] = f"\033[92m{result[i]}\033[00m"

    def _find_lesser_matches(self, user_word: str, result: list[str]):
        """Find other matches that don't have same index"""
        for i in range(0, self.word_length):
            if not self._letters_user_word_not_used[i]:
                continue
            for j in range(0, self.word_length):
                if self._letters_hidden_word_not_found[j] and \
                        user_word[i] == self._word_to_find[j]:
                    self._letters_hidden_word_not_found[j] = False
                    self._letters_user_word_not_used[i] = False
                    result[i] = f"\033[93m{result[i]}\033[00m"
                    break

    def _get_test_list(self) -> list[bool]:
        """Return list of bool to test word given by user """

        result_list: list[bool] = []
        for i in range(0, self.word_length):
            result_list.append(True)

        return result_list




