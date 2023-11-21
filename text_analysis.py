# Word Co-occurrence:
# In text analysis, this typically refers to how often certain words or phrases appear together within a text. 
# For example, in a dataset of news articles, you might analyze how often the word "climate" appears near words like "change," "crisis," or "hoax."

# User and Author Co-occurrence: 
# If your dataset includes user comments and author posts, co-occurrence analysis might look at how often certain users interact with specific authors, or how certain topics bring specific users and authors together.

# Purposes in Misinformation Analysis
#  - Identifying Common Themes: By analyzing word co-occurrence, you can identify common themes or talking points within the dataset. This is particularly useful in understanding the framing of climate news.
#  - Detecting Misinformation Trends: If certain misleading or false phrases frequently co-occur, it could indicate trends in how misinformation is spread.
#  - Understanding User Engagement: Co-occurrence data involving users and authors can reveal patterns in how audiences engage with different types of content or authors, which can be insightful in understanding the spread of information or misinformation.
#  - Network Analysis: Co-occurrence can be used to build network graphs, showing how different elements (like words or users) connect within your dataset. This can visually represent the relationships and clusters within the data.

# Sentiment Correlation: 
# By combining co-occurrence analysis with sentiment analysis (as our code does), you can explore how the sentiment around certain topics or phrases varies and correlates with the occurrence of specific words or themes.


#SECTION 1 - PREPROCESSING

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

# Function to extract noun phrases from text using spaCy
def extract_noun_phrases(text):
    doc = nlp(text)
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    return ", ".join(noun_phrases)

# Initialize VADER sentiment analyzer
# and defines a function (get_vader_sentiment) to calculate sentiment scores using VADER.
sia = SentimentIntensityAnalyzer()

# Function to calculate VADER sentiment score
def get_vader_sentiment(text):
    return sia.polarity_scores(text)['compound']

# Apply the functionsto extract noun phrases and calculate sentiment scores for the 'title' and 'comment' columns in the DataFrame.
data['noun_phrase.title'] = data['title'].astype(str).apply(extract_noun_phrases)
data['noun_phrase.comment'] = data['comment'].astype(str).apply(extract_noun_phrases)
data['vader.title'] = data['title'].astype(str).apply(get_vader_sentiment)
data['vader.comment'] = data['comment'].astype(str).apply(get_vader_sentiment)

# Save the modified dataframe to CSV file
output_file_path = 'processed_climatenews_subreddit.csv'  # Replace with your desired output file path
data.to_csv(output_file_path, index=False)

print("Processing complete. The output is saved to:", output_file_path)


# SECTION 2: Co-occurrence Analysis
#%% 
import pandas as pd

# Load the CSV file - reloads the original data from the CSV file.
file_path = 'climatenews_subreddit.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Ensure the necessary columns are present in the dataset
required_columns = ['user', 'author', 'comment', 'title', 'post_text', 'comm_date']
if not all(column in data.columns for column in required_columns):
    raise ValueError("One or more required columns are missing from the dataset.")

# Create a new DataFrame called co_occurrence to store co-occurrence table.
co_occurrence = pd.DataFrame()

# Fill the new DataFrame with the required data from original data
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
# SECTION 3 - COMBINE ANALYSIS AND NETWORKING
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

#enhanced co-occurrence table now includes noun phrases and sentiment analysis results
print("Enhanced co-occurrence table created and saved to:", output_file_path)


#SECTION 4 - N-GRAMS and further analysis
#%% 
import pandas as pd
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.util import ngrams # NLTK is used to generate and filter n-grams (word pairs) from the text.
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



