#!/usr/bin/env python3
import os
import argparse
import string
from collections import Counter

class ChatLogSummarizer:

    def __init__(self):
        
        self.user_messages = []
        self.ai_messages = []
        self.all_messages = []
    
        self.stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
            'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
            'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
            'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
            'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
            'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
            'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
            'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
            'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
            'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
            'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'would',
            'could', 'please', 'like', 'help'
        }

    def parse_chat_log(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            lines = content.split('\n')
            current_speaker = None
            current_message = []

            for line in lines:
                if line.startswith('User:'):
                    if current_speaker and current_message:
                        self._add_message(current_speaker, ' '.join(current_message))
                    current_speaker = 'User'
                    current_message = [line[5:].strip()]
                elif line.startswith('AI:'):
                    if current_speaker and current_message:
                        self._add_message(current_speaker, ' '.join(current_message))
                    current_speaker = 'AI'
                    current_message = [line[3:].strip()]
                elif current_speaker:
                    current_message.append(line.strip())

            if current_speaker and current_message:
                self._add_message(current_speaker, ' '.join(current_message))
            return True
        except Exception as e:
            print(f"Error parsing chat log: {e}")
            return False

    def _add_message(self, speaker, message):
        if speaker == 'User':
            self.user_messages.append(message)
        else:
            self.ai_messages.append(message)
        self.all_messages.append(message)
   
if __name__ == "__main__":
    summarizer = ChatLogSummarizer()
    if summarizer.parse_chat_log("chat_logs/python_chat.txt"):
        print("Chat log parsed successfully!")
        print(f"User messages: {len(summarizer.user_messages)}")
        print(f"AI messages: {len(summarizer.ai_messages)}")

        print("\nFirst few User messages:")
        for msg in summarizer.user_messages[:2]:
            print("-", msg)

        print("\nFirst few AI messages:")
        for msg in summarizer.ai_messages[:2]:
            print("-", msg)
    else:
        print("Failed to parse chat log.")
