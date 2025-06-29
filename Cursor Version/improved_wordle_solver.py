"""
Improved Wordle Solver
A more robust and feature-rich implementation for solving Wordle puzzles.

Code by: Matthew Vaerewyck
AI Assistant: Cursor
Date: 2025-06-29

## Features

- **Robust word list fetching** with multiple fallback sources
- **Local caching** to avoid repeated web requests
- **Smart suggestions** based on letter frequency analysis
- **Comprehensive error handling** and validation
- **Statistics tracking** for solving performance
- **Interactive commands** (reset, stats, quit)
- **Type hints** and proper documentation
- **Logging** for debugging and monitoring

## Installation

"""

import re
import requests
import json
import os
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from collections import Counter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WordleFeedback:
    """Represents feedback from a Wordle guess."""
    guess: str
    feedback: str  # 'g' for green, 'y' for yellow, '.' for gray
    
    def validate(self) -> bool:
        """Validate that the feedback is properly formatted."""
        if len(self.guess) != 5 or len(self.feedback) != 5:
            return False
        if not self.guess.isalpha():
            return False
        if not all(c in 'gy.' for c in self.feedback):
            return False
        return True

class WordleSolver:
    """An improved Wordle solver with better error handling and features."""
    
    def __init__(self, cache_file: str = "wordle_words.json"):
        self.cache_file = cache_file
        self.wordlist: List[str] = []
        self.green_positions: Dict[int, str] = {}  # position -> letter
        self.yellow_positions: List[Tuple[int, str]] = []  # (position, letter)
        self.gray_letters: set = set()
        self.guess_history: List[WordleFeedback] = []
        
    def load_wordlist(self) -> bool:
        """Load word list from cache or fetch from web."""
        try:
            # Try to load from cache first
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.wordlist = json.load(f)
                logger.info(f"Loaded {len(self.wordlist)} words from cache")
                return True
        except Exception as e:
            logger.warning(f"Failed to load from cache: {e}")
        
        # Fetch from web if cache doesn't exist or is invalid
        return self._fetch_wordlist()
    
    def _fetch_wordlist(self) -> bool:
        """Fetch word list from the web."""
        try:
            logger.info("Fetching word list from web...")
            
            # Try multiple sources for robustness
            sources = [
                "https://meaningpedia.com/5-letter-words?show=all",
                "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
            ]
            
            for source in sources:
                try:
                    response = requests.get(source, timeout=10)
                    response.raise_for_status()
                    
                    if "meaningpedia.com" in source:
                        # Parse meaningpedia format
                        pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
                        words = pattern.findall(response.text)
                    else:
                        # Parse simple word list
                        words = [word.strip().lower() for word in response.text.split('\n') 
                               if len(word.strip()) == 5 and word.strip().isalpha()]
                    
                    # Filter for 5-letter words and normalize
                    self.wordlist = [word.lower() for word in words if len(word) == 5 and word.isalpha()]
                    
                    if self.wordlist:
                        # Cache the word list
                        with open(self.cache_file, 'w') as f:
                            json.dump(self.wordlist, f)
                        
                        logger.info(f"Successfully fetched {len(self.wordlist)} words from {source}")
                        return True
                        
                except Exception as e:
                    logger.warning(f"Failed to fetch from {source}: {e}")
                    continue
            
            logger.error("Failed to fetch word list from all sources")
            return False
            
        except Exception as e:
            logger.error(f"Error fetching word list: {e}")
            return False
    
    def process_feedback(self, feedback: WordleFeedback) -> None:
        """Process feedback from a Wordle guess."""
        self.guess_history.append(feedback)
        
        # Update constraints based on feedback
        for i, (guess_char, feedback_char) in enumerate(zip(feedback.guess, feedback.feedback)):
            if feedback_char == 'g':
                self.green_positions[i] = guess_char
            elif feedback_char == 'y':
                self.yellow_positions.append((i, guess_char))
            else:  # feedback_char == '.'
                self.gray_letters.add(guess_char)
        
        # Filter word list based on new constraints
        self._filter_wordlist()
    
    def _filter_wordlist(self) -> None:
        """Filter the word list based on current constraints."""
        filtered_words = []
        
        for word in self.wordlist:
            if self._word_matches_constraints(word):
                filtered_words.append(word)
        
        self.wordlist = filtered_words
    
    def _word_matches_constraints(self, word: str) -> bool:
        """Check if a word matches all current constraints."""
        # Check green positions
        for pos, letter in self.green_positions.items():
            if word[pos] != letter:
                return False
        
        # Check gray letters (letters not in word)
        for letter in self.gray_letters:
            if letter in word:
                return False
        
        # Check yellow positions (letters in word but not in specific positions)
        yellow_letters = set()
        for pos, letter in self.yellow_positions:
            if word[pos] == letter:  # Yellow letter in wrong position
                return False
            yellow_letters.add(letter)
        
        # Check that all yellow letters are present
        for letter in yellow_letters:
            if letter not in word:
                return False
        
        return True
    
    def get_suggestions(self, count: int = 10) -> List[str]:
        """Get suggested next guesses based on information theory."""
        if not self.wordlist:
            return []
        
        if len(self.wordlist) <= count:
            return self.wordlist
        
        # Simple scoring: prefer words with common letters
        letter_freq = Counter()
        for word in self.wordlist:
            letter_freq.update(word)
        
        def score_word(word: str) -> float:
            return sum(letter_freq[letter] for letter in set(word))
        
        scored_words = [(word, score_word(word)) for word in self.wordlist]
        scored_words.sort(key=lambda x: x[1], reverse=True)
        
        return [word for word, _ in scored_words[:count]]
    
    def get_stats(self) -> Dict:
        """Get solving statistics."""
        return {
            'words_remaining': len(self.wordlist),
            'guesses_made': len(self.guess_history),
            'green_letters': len(self.green_positions),
            'yellow_letters': len(self.yellow_positions),
            'gray_letters': len(self.gray_letters)
        }
    
    def reset(self) -> None:
        """Reset the solver for a new puzzle."""
        self.green_positions.clear()
        self.yellow_positions.clear()
        self.gray_letters.clear()
        self.guess_history.clear()
        self.load_wordlist()

def main():
    """Main interactive loop for the Wordle solver."""
    solver = WordleSolver()
    
    print("=== Improved Wordle Solver ===")
    print("Loading word list...")
    
    if not solver.load_wordlist():
        print("Error: Could not load word list. Please check your internet connection.")
        return
    
    print(f"Loaded {len(solver.wordlist)} words successfully!")
    print("\nInstructions:")
    print("- Enter your 5-letter guess")
    print("- Enter feedback using: g (green), y (yellow), . (gray)")
    print("- Example: 'g.y.g' means first letter green, third yellow, fifth green")
    print("- Type 'quit' to exit, 'reset' to start over, 'stats' for statistics")
    
    while True:
        try:
            # Get user's guess
            guess_input = input("\nEnter your guess (or command): ").strip().lower()
            
            if guess_input == 'quit':
                break
            elif guess_input == 'reset':
                solver.reset()
                print("Solver reset for new puzzle!")
                continue
            elif guess_input == 'stats':
                stats = solver.get_stats()
                print(f"\nStatistics:")
                print(f"- Words remaining: {stats['words_remaining']}")
                print(f"- Guesses made: {stats['guesses_made']}")
                print(f"- Green letters found: {stats['green_letters']}")
                print(f"- Yellow letters found: {stats['yellow_letters']}")
                print(f"- Gray letters found: {stats['gray_letters']}")
                continue
            
            # Validate guess
            if len(guess_input) != 5 or not guess_input.isalpha():
                print("Error: Guess must be a 5-letter word")
                continue
            
            # Get feedback
            feedback_input = input("Enter feedback (gy.): ").strip().lower()
            
            if len(feedback_input) != 5 or not all(c in 'gy.' for c in feedback_input):
                print("Error: Feedback must be 5 characters using g, y, or .")
                continue
            
            # Process feedback
            feedback = WordleFeedback(guess_input, feedback_input)
            
            # Validate feedback before processing
            if not feedback.validate():
                print("Error: Invalid feedback format. Please ensure:")
                print("- Feedback is exactly 5 characters long")
                print("- Feedback only contains: g (green), y (yellow), . (gray)")
                print("- Guess is exactly 5 letters")
                continue
            
            solver.process_feedback(feedback)
            
            # Check for win
            if feedback_input == 'ggggg':
                print("🎉 Congratulations! You solved it!")
                break
            
            # Show results
            stats = solver.get_stats()
            print(f"\nWords remaining: {stats['words_remaining']}")
            
            if stats['words_remaining'] == 0:
                print("❌ No words match the constraints. Check your feedback!")
                break
            elif stats['words_remaining'] == 1:
                print(f"🎯 The answer is: {solver.wordlist[0]}")
                break
            else:
                suggestions = solver.get_suggestions(5)
                print(f"💡 Suggested next guesses: {', '.join(suggestions)}")
                
                # Show some remaining words
                if stats['words_remaining'] <= 20:
                    print(f"📝 All remaining words: {', '.join(solver.wordlist)}")
                else:
                    print(f"📝 First 10 remaining words: {', '.join(solver.wordlist[:10])}")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main() 