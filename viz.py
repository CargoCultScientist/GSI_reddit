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

# Plotting the daily aggregated VADER scores
plt.figure(figsize=(15, 7))
sns.lineplot(data=daily_agg, x='date', y='vader.comment', hue='subreddit')
plt.title('Daily Aggregated VADER Scores by Subreddit - Minimalist Style')
plt.xlabel('Date')
plt.ylabel('Average VADER Score')
plt.xticks(rotation=45)
plt.legend(title='Subreddit')
plt.tight_layout()
plt.show()
