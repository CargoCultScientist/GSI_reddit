#%% 
import pandas as pd
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
import sqlite3
# from bertopic import BERTopic

#%% 
# Load the CSV file
file_path = 'climatenews_subreddit.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Load the English tokenizer, tagger, parser, NER, and word vectors from spacy
nlp = spacy.load("en_core_web_trf")

# Function to extract noun phrases
def extract_noun_phrases(text):
    doc = nlp(text)
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    return ", ".join(noun_phrases)

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to calculate VADER sentiment score
def get_vader_sentiment(text):
    return sia.polarity_scores(text)['compound']

# Apply the functions to the title and comment columns
data['noun_phrase.title'] = data['title'].astype(str).apply(extract_noun_phrases)
data['noun_phrase.comment'] = data['comment'].astype(str).apply(extract_noun_phrases)
data['vader.title'] = data['title'].astype(str).apply(get_vader_sentiment)
data['vader.comment'] = data['comment'].astype(str).apply(get_vader_sentiment)

# Save the modified dataframe
output_file_path = 'processed_climatenews_subreddit.csv'  # Replace with your desired output file path
data.to_csv(output_file_path, index=False)

print("Processing complete. The output is saved to:", output_file_path)



#%% 
#Co-occurrence 
import pandas as pd
# Load the CSV file

file_path = 'climatenews_subreddit.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Ensure the necessary columns are present
required_columns = ['user', 'author', 'comment', 'title', 'post_text', 'comm_date']
if not all(column in data.columns for column in required_columns):
    raise ValueError("One or more required columns are missing from the dataset.")

# Create a new DataFrame for the co-occurrence table
co_occurrence = pd.DataFrame()

# Fill the new DataFrame with the required data
co_occurrence['user'] = data['user']
co_occurrence['author'] = data['author']
co_occurrence['comment'] = data['comment']
co_occurrence['title'] = data['title']
co_occurrence['post_text'] = data['post_text']
co_occurrence['comm_date'] = data['comm_date']

# Handle missing values if necessary (e.g., with empty strings)
co_occurrence.fillna('', inplace=True)

# Save the co-occurrence table to a new CSV file
output_file_path = 'co_occurrence_table.csv'  # Replace with your desired output file path
co_occurrence.to_csv(output_file_path, index=False)

print("Co-occurrence table created and saved to:", output_file_path)


#%% 
# Combine analysis and networking 
import pandas as pd
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer

# Load the CSV file
file_path = 'climatenews_subreddit.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Load the English tokenizer, tagger, parser, NER, and word vectors from spacy
nlp = spacy.load("en_core_web_trf")  # Using the transformer-based model

# Function to extract noun phrases
def extract_noun_phrases(text):
    doc = nlp(text)
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    return ", ".join(noun_phrases)

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to calculate VADER sentiment score
def get_vader_sentiment(text):
    return sia.polarity_scores(text)['compound']

# Create a new DataFrame for the co-occurrence table
co_occurrence = pd.DataFrame()

# Fill the new DataFrame with the required data
co_occurrence['user'] = data['user']
co_occurrence['author'] = data['author']
co_occurrence['comment'] = data['comment']
co_occurrence['title'] = data['title']
co_occurrence['post_text'] = data['post_text']
co_occurrence['comm_date'] = data['comm_date']
co_occurrence['subreddit'] = data['url'].apply(lambda url: url.split('/')[4] if len(url.split('/')) > 4 else 'Unknown')

# Adding noun phrases and sentiment analysis results
co_occurrence['noun_phrase.title'] = co_occurrence['title'].astype(str).apply(extract_noun_phrases)
co_occurrence['noun_phrase.comment'] = co_occurrence['comment'].astype(str).apply(extract_noun_phrases)
co_occurrence['vader.title'] = co_occurrence['title'].astype(str).apply(get_vader_sentiment)
co_occurrence['vader.comment'] = co_occurrence['comment'].astype(str).apply(get_vader_sentiment)

# Handle missing values if necessary (e.g., with empty strings)
co_occurrence.fillna('', inplace=True)

# Save the co-occurrence table with additional data to a new CSV file
output_file_path = 'enhanced_co_occurrence_table.csv'  # Replace with your desired output file path
co_occurrence.to_csv(output_file_path, index=False)

print("Enhanced co-occurrence table created and saved to:", output_file_path)

#%% 
import pandas as pd
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.util import ngrams
from nltk.corpus import stopwords
import nltk

# Download stopwords from nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load the CSV file
file_path = 'climatenews_subreddit.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to calculate VADER sentiment score
def get_vader_sentiment(text):
    return sia.polarity_scores(text)['compound']

# Function to generate and filter n-grams
def generate_filtered_ngrams(text, n=2):
    words = nltk.word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    generated_ngrams = ngrams(filtered_words, n)
    return ', '.join([' '.join(gram) for gram in generated_ngrams])

# Create a new DataFrame for the co-occurrence table
co_occurrence = pd.DataFrame()

# Fill the new DataFrame with the required data
co_occurrence['user'] = data['user']
co_occurrence['author'] = data['author']
co_occurrence['comment'] = data['comment']
co_occurrence['title'] = data['title']
co_occurrence['post_text'] = data['post_text']
co_occurrence['comm_date'] = data['comm_date']
co_occurrence['subreddit'] = data['url'].apply(lambda url: url.split('/')[4] if len(url.split('/')) > 4 else 'Unknown')

# Adding N-grams and sentiment analysis results
co_occurrence['ngrams.title'] = co_occurrence['title'].astype(str).apply(lambda x: generate_filtered_ngrams(x, 2))
co_occurrence['ngrams.comment'] = co_occurrence['comment'].astype(str).apply(lambda x: generate_filtered_ngrams(x, 2))
co_occurrence['vader.title'] = co_occurrence['title'].astype(str).apply(get_vader_sentiment)
co_occurrence['vader.comment'] = co_occurrence['comment'].astype(str).apply(get_vader_sentiment)

# Handle missing values if necessary (e.g., with empty strings)
co_occurrence.fillna('', inplace=True)

# Save the co-occurrence table with additional data to a new CSV file
output_file_path = 'enhanced_co_occurrence_table_with_ngrams.csv'  # Replace with your desired output file path
co_occurrence.to_csv(output_file_path, index=False)

print("Enhanced co-occurrence table with N-grams created and saved to:", output_file_path)



