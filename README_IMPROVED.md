# Improved Wordle Solver

A robust, feature-rich Wordle solver with better error handling, caching, and user experience.

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

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the improved solver:
```bash
python improved_wordle_solver.py
```

## Usage

### Basic Usage
1. Enter your 5-letter guess
2. Enter the feedback from Wordle:
   - `g` = green (correct letter, correct position)
   - `y` = yellow (correct letter, wrong position)
   - `.` = gray (letter not in word)

### Example Session
```
=== Improved Wordle Solver ===
Loading word list...
Loaded 12947 words successfully!

Instructions:
- Enter your 5-letter guess
- Enter feedback using: g (green), y (yellow), . (gray)
- Example: 'g.y.g' means first letter green, third yellow, fifth green
- Type 'quit' to exit, 'reset' to start over, 'stats' for statistics

Enter your guess (or command): slate
Enter feedback (gy.): ..y.g

Words remaining: 47
💡 Suggested next guesses: crate, trace, grace, brace, place
📝 First 10 remaining words: crate, trace, grace, brace, place, space, face, pace, race, ace
```

### Commands
- `quit` - Exit the solver
- `reset` - Start over with a new puzzle
- `stats` - Show current solving statistics

## Key Improvements Over Original

### 1. **Error Handling & Robustness**
- Multiple word list sources with fallback
- Network timeout handling
- Graceful degradation when sources are unavailable
- Comprehensive input validation

### 2. **Performance & Efficiency**
- Local caching of word lists
- More efficient constraint checking
- Batch processing for large word lists

### 3. **User Experience**
- Smart word suggestions based on information theory
- Real-time statistics
- Better feedback and error messages
- Interactive commands

### 4. **Code Quality**
- Type hints throughout
- Proper separation of concerns
- Comprehensive documentation
- Logging for debugging

### 5. **Additional Features**
- Word scoring based on letter frequency
- Guess history tracking
- Multiple constraint types (green, yellow, gray)
- Statistics and analytics

## Architecture

The improved solver uses a more modular approach:

- `WordleFeedback` - Data class for representing guess feedback
- `WordleSolver` - Main solver class with constraint management
- `main()` - Interactive user interface

### Constraint Management
- **Green positions**: Exact letter positions
- **Yellow positions**: Letters in word but wrong positions
- **Gray letters**: Letters not in the word

## Algorithm

1. **Word List Loading**: Try cache first, then fetch from web
2. **Constraint Processing**: Update constraints based on feedback
3. **Word Filtering**: Remove words that don't match constraints
4. **Suggestion Generation**: Score remaining words by letter frequency
5. **Statistics Tracking**: Monitor solving progress

## Future Enhancements

- **Machine learning integration** for better word scoring
- **Web interface** with GUI
- **Solver performance analytics**
- **Custom word lists** support
- **Multi-language support**
- **Automated solving** with web scraping

## Troubleshooting

### Common Issues

1. **"Could not load word list"**
   - Check internet connection
   - Verify the word list sources are accessible
   - Check if cache file is corrupted

2. **"No words match the constraints"**
   - Double-check your feedback input
   - Ensure you're using the correct format (g, y, .)
   - Try resetting the solver

3. **Performance issues**
   - The solver caches word lists locally
   - First run may be slower due to web fetching
   - Subsequent runs will be faster

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 