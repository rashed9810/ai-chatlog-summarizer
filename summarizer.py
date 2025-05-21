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
   
    def get_message_stats(self):
       return {
           'total_messages': len(self.user_messages) + len(self.ai_messages),
           'user_messages': len(self.user_messages),
           'ai_messages': len(self.ai_messages),
           'exchanges': min(len(self.user_messages), len(self.ai_messages))
           
       }
    
    def extract_keywords_simple(self, top_n=5):
        text = ' '.join(self.all_messages).lower()
        text = text.translate(str.maketrans(", ", string.punctuation))
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words and len(word) > 2]
        word_counts = Counter(filtered_words)
        return [word for word, _ in word_counts.most_common(top_n)]
    
    def extract_keywords_tfidf(self, top_n=5):
        user_text = ' '.join(self.user_messages).lower()
        ai_text = ' '.join(self.ai_messages).lower()
        
        # remove punctuation
        user_text = user_text.translate(str.maketrans('', '', string.punctuation))
        ai_text = ai_text.translate(str.maketrans('', '', string.punctuation))

        
        # tokenize
        user_words = user_text.split()
        ai_words = ai_text.split()
        
         # Remove stop words and short words
        user_words = [word for word in user_words if word not in self.stop_words and len(word) > 2]
        ai_words = [word for word in ai_words if word not in self.stop_words and len(word) > 2]
        
        
        user_word_counts = Counter(user_words)
        ai_word_counts = Counter(ai_words)
        
        # Get all unique words
        all_words = set(user_word_counts.keys()) | set(ai_word_counts.keys()) 
        tfidf_scores = {}
        n_docs = 2
        
        for word in all_words:
            tf_user = user_word_counts.get(word, 0) / max(len(user_words), 1)
            tf_ai = ai_word_counts.get(word, 0) / max(len(ai_words), 1)
            
            df = (1 if word in user_word_counts else 0) + (1 if word in ai_word_counts else 0 )
            idf = 1 + (n_docs / df if df > 0 else 0)
            tfidf_scores[word] = ((tf_user + tf_ai) / 2) * idf 
            
        sorted_words = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:top_n]]

        
    def generate_summary(self, use_tfidf=True):
        stats = self.get_message_stats()

        if use_tfidf:
            keywords = self.extract_keywords_tfidf()
        else:
            keywords = self.extract_keywords_simple()
        nature = self._determine_conversation_nature(keywords)

        summary = "Summary:\n"
        summary += f"- The conversation had {stats['total_messages']} messages "
        summary += f"({stats['user_messages']} from User, {stats['ai_messages']} from AI).\n"
        summary += f"- The user asked mainly about {nature}.\n"
        summary += f"- Most common keywords: {', '.join(keywords)}.\n"

        return summary

    def _determine_conversation_nature(self, keywords):
        return " and ".join(keywords[:2])

    def process_directory(self, directory_path, use_tfidf=True):
        results = {}

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)

                
                self.__init__()

                
                if self.parse_chat_log(file_path):
                   
                    summary = self.generate_summary(use_tfidf)
                    results[filename] = summary

        return results


def main():
    parser = argparse.ArgumentParser(description='AI Chat Log Summarizer')
    parser.add_argument('input', help='Path to chat log file or directory')
    parser.add_argument('--simple', action='store_true',
                        help='Use simple frequency-based keyword extraction instead of TF-IDF')
    parser.add_argument('--output', help='Output file to save the summary')

    args = parser.parse_args()
    summarizer = ChatLogSummarizer()

    if os.path.isdir(args.input):
        results = summarizer.process_directory(args.input, not args.simple)
        output_text = ""
        for filename, summary in results.items():
            output_text += f"\n=== {filename} ===\n{summary}\n"

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_text)
        else:
            print(output_text)
    else:
        if summarizer.parse_chat_log(args.input):
            summary = summarizer.generate_summary(not args.simple)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(summary)
            else:
                print(summary)


if __name__ == "__main__":
    main()
        
        
   
   
   
   
