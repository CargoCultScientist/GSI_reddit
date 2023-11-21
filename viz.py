# comprehensive script for analyzing and visualizing sentiment data from a dataset, here: containing comments and posts from specific subreddits 
# This script can be instrumental in sentiment analysis projects, especially those focusing on social media or forum data,
# to understand public opinion, track sentiment trends over time, and identify influential authors or contributors in online discussions. 
# It's particularly relevant for analyzing discussions around polarizing topics, as shown by the focus on climate change-related subreddits in this case.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# Load the dataset
df = pd.read_csv('path_to_your_file.csv')

# Convert 'comm_date' to datetime and extract date for daily aggregation
df['comm_date'] = pd.to_datetime(df['comm_date'])
df['date'] = df['comm_date'].dt.date

# Aggregate the VADER scores by day and subreddit
daily_agg = df.groupby(['subreddit', 'date'])[['vader.title', 'vader.comment']].mean().reset_index()

# Setting a minimalist style for the plot
sns.set(style="whitegrid", palette="pastel")

# Line Plot for Daily Aggregated VADER Scores
# Aggregates the VADER sentiment scores ('vader.title', 'vader.comment') by day and subreddit.
# Visualizes these aggregated scores using a line plot with a minimalist style, differentiating subreddits by color.
plt.figure(figsize=(15, 7))
sns.lineplot(data=daily_agg, x='date', y='vader.comment', hue='subreddit')
plt.title('Daily Aggregated VADER Scores by Subreddit - Minimalist Style')
plt.xlabel('Date')
plt.ylabel('Average VADER Score')
plt.xticks(rotation=45)
plt.legend(title='Subreddit')
plt.tight_layout()
plt.show()

#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from pandas.plotting import register_matplotlib_converters

# Load the dataset
df = pd.read_csv('path_to_your_file.csv')

# Convert 'comm_date' to datetime and extract date for daily aggregation
df['comm_date'] = pd.to_datetime(df['comm_date'])
df['date'] = df['comm_date'].dt.date

# Aggregate the VADER scores by day and subreddit
daily_agg = df.groupby(['subreddit', 'date'])[['vader.title', 'vader.comment']].mean().reset_index()

# Bar Plots for Specific Subreddits
# Filters data for specific subreddits ('climatechange' and 'climateskeptics').
# Adjusts for the date range to ensure comparability.
# Saves and displays bar charts showing daily aggregated VADER scores for these subreddits.

# Filter data for specific subreddits and adjust the date range
climatechange_data = daily_agg[daily_agg['subreddit'] == 'climatechange']
climateskeptics_data = daily_agg[daily_agg['subreddit'] == 'climateskeptics']
date_range = climatechange_data['date'].unique()
climateskeptics_data = climateskeptics_data[climateskeptics_data['date'].isin(date_range)]

# Save and plot bar charts for each subreddit
def save_plot(data, title, color, file_path):
    plt.figure(figsize=(15, 7))
    sns.barplot(data=data, x='date', y='vader.comment', color=color)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Average VADER Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.show()

save_plot(climatechange_data, 'Daily Aggregated VADER Scores in r/climatechange', 'skyblue', 'climatechange_bar_plot.png')
save_plot(climateskeptics_data, 'Daily Aggregated VADER Scores in r/climateskeptics - Adjusted Date Range', 'coral', 'climateskeptics_bar_plot.png')


# Word Cloud Generation
# Generates word clouds for positive and negative comments from the top 30 authors by comment count.
# Custom stopwords are used to filter out common but uninformative words.
# Two word clouds are generated, one for positive and one for negative sentiment, and are saved as image files.

# Filtering the top 30 authors by number of comments
# Aggregates and saves data about these authors, including the count of comments and average VADER score.
top_authors = df['author'].value_counts().head(30).index
top_authors_data = df[df['author'].isin(top_authors)]

# Word Cloud Generation
custom_stopwords = set(STOPWORDS).update({"people", "will", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"})
def generate_wordcloud(text, file_path, color):
    wordcloud = WordCloud(stopwords=custom_stopwords, background_color="white", contour_width=3, contour_color=color, width=800, height=800, colormap="spring").generate(text)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(file_path)
    plt.show()

positive_text = " ".join(comment for comment in top_authors_data[top_authors_data['vader.comment'] > 0]['comment'])
negative_text = " ".join(comment for comment in top_authors_data[top_authors_data['vader.comment'] < 0]['comment'])

generate_wordcloud(positive_text, 'positive_comments_wordcloud.png', 'steelblue')
generate_wordcloud(negative_text, 'negative_comments_wordcloud.png', 'firebrick')

# Aggregating and saving top authors data
def aggregate_and_save(data, sentiment, file_path):
    data.groupby('author').agg(
        count=('vader.comment', 'count'),
        avg_vader=('vader.comment', 'mean')
    ).sort_values(by=f'avg_vader', ascending=(sentiment == 'negative')).head(30).to_csv(file_path)

aggregate_and_save(top_authors_data[top_authors_data['vader.comment'] > 0], 'positive', 'top_positive_authors.csv')
aggregate_and_save(top_authors_data[top_authors_data['vader.comment'] < 0], 'negative', 'top_negative_authors.csv')
