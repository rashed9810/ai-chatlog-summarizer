# AI Chat Log Summarizer

A Python-based tool that reads .txt chat logs between a user and an AI, parses the conversation, and produces a simple summary including message counts and frequently used keywords.

## Features

- **Chat Log Parsing**: Separates messages by speaker (User and AI)
- **Message Statistics**: Counts total messages and messages from each speaker
- **Keyword Analysis**: Extracts the top 5 most frequently used words, excluding common stop words
- **Summary Generation**: Outputs a clear summary of the conversation
- **Advanced Keyword Extraction**: Uses TF-IDF for better keyword extraction (optional)
- **Batch Processing**: Supports summarization of multiple chat logs from a folder

## Installation

No installation required beyond Python itself. This project uses only the Python standard library, making it easy to run on any system with Python installed.

### Prerequisites

- Python 3.6 or higher

## Usage

### Basic Usage

Process a single chat log file:

```bash
python summarizer.py sample_chat.txt
```

This will display output similar to:

```text
Summary:
- The conversation had 12 messages (6 from User, 6 from AI).
- The user asked mainly about learning and machine.
- Most common keywords: learning, machine, someone, thank, explain.
```

### Advanced Options

- Use simple frequency-based keyword extraction instead of TF-IDF:

  ```bash
  python summarizer.py sample_chat.txt --simple
  ```

- Save the summary to a file:

  ```bash
  python summarizer.py sample_chat.txt --output summary.txt
  ```

- Process all .txt files in a directory:

  ```bash
  python summarizer.py chat_logs/
  ```

- Process multiple chat logs and save to a file:

  ```bash
  python summarizer.py chat_logs/ --output summary.txt
  ```

## Command-Line Arguments

- `input`: Path to a chat log file or directory (required)
- `--simple`: Use simple frequency-based keyword extraction instead of TF-IDF
- `--output`: Output file to save the summary

## Example Chat Log Format

The script expects chat logs in the following format:

```text
User: Hello!
AI: Hi! How can I assist you today?
User: Can you explain what machine learning is?
AI: Certainly! Machine learning is a field of AI that allows systems to learn from data.
```

## Sample Output

```text
Summary:
- The conversation had 12 messages (6 from User, 6 from AI).
- The user asked mainly about learning and machine.
- Most common keywords: learning, machine, someone, thank, explain.
```

## Project Structure

- `summarizer.py`: Main script with all the functionality
- `sample_chat.txt`: Sample chat log for testing
- `chat_logs/`: Directory containing multiple chat logs for testing
- `README.md`: Documentation for the project

## Implementation Details

### Chat Log Parsing

The script parses chat logs by identifying lines that start with "User:" or "AI:" and groups consecutive lines as part of the same message.

### Keyword Extraction

Two methods are implemented for keyword extraction:

1. **Simple Frequency-Based**: Counts word occurrences and returns the most frequent words
2. **TF-IDF (Term Frequency-Inverse Document Frequency)**: Weighs words based on their importance in the conversation

### Stop Words

Common English words (like "the", "is", "and") are excluded from keyword analysis to focus on meaningful content words.

## Troubleshooting

- If you get a "file not found" error, make sure you're in the correct directory and the file path is correct.
- If you're processing a directory, make sure it contains .txt files in the expected format.
- If the summary doesn't look right, check that your chat log follows the expected format with "User:" and "AI:" prefixes.

## Author

Rashed

## Acknowledgments

- This project was created as part of a coding assessment
