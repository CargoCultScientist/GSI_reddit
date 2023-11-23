# Climate Disinformation Analysis Tool on Reddit

## Overview

This tool is designed to analyze the sources of climate disinformation on Reddit, focusing on popular subreddits related to climate topics. It constructs a bi-directional network of conversations between commenters and posters, enabling comprehensive social network analysis.

## Features

- **Social Network Analysis**: Identifies influential users through PageRank scoring and metrics such as degree and betweenness centrality.
- **Content Analysis**: Combines manual efforts with natural language processing to validate users as sources of misinformation.

## Installation

1. Clone the repository: `git clone [repository URL]`.
2. Navigate to the project directory: `cd [project folder]`.
3. Install the required dependencies: `pip install -r requirements.txt`.

#### Expected Data Structure

1. **Columns**:
   - The script expects specific columns in the data, which include:
     - `user`: Identifier for the user who made a comment or post.
     - `author`: Identifier for the author of a post.
     - `comment`: The text of the user's comment.
     - `title`: Title of the post.
     - `post_text`: The text content of the post.
     - `comm_date`: The date of the comment or post. 

2. **Data Types**:
   - `user` and `author` are expected to be string identifiers (e.g., usernames).
   - `comment`, `title`, and `post_text` are expected to be text fields, containing the written content of the comments and posts.
   - `comm_date` should be a date field or a string that can be converted into a date. This is used for organizing and possibly time-stamping the analysis.

3. **Content**:
   - The text fields (`comment`, `title`, and `post_text`) are essential for co-occurrence analysis, as they will be used to identify which words or phrases often appear together.
   - The `user` and `author` fields are important for understanding the interaction dynamics and network analysis, which involves seeing how users are connected based on their comments and posts.

4. **Format**:
   - The data is expected to be in a tabular (CSV) format.
   - Each row in this DataFrame would represent an individual comment or post, with the relevant information spread across the columns mentioned above.

- The script will use this data to perform co-occurrence analysis, which involves calculating how often specific words are used together in `comment` and `title` columns, or how often certain users (`user` column) interact with specific authors (`author` column).
- Additionally, by including `comm_date`, the script could analyze how these co-occurrence patterns evolve over time.


## Usage

To use the tool, follow these steps:

1. Use your own generated text data or try our dataset. 
2. Execute `text_analysis.py` for content analysis and misinformation detection: `python text_analysis.py`.
3. Run the `viz.py` script to generate network visualizations: `python viz.py`.

## File Descriptions

- `load_data.py`: Fetches and stores data from the Newscatcher API for multiple search terms related to disinformation, saving it as JSON files. It adds a unique ID to each entry and then loads and stores the data in an SQLite database.
- `nlp_functions.py`: Performs natural language processing tasks on text data using the spaCy library, focusing on extracting various entities from texts and demonstrating the process on item data from a CSV file.
- `stuff.py` (not used): Defines a text and uses the KeyBERT library to extract keywords from it, storing the results in a variable.
- `text_analysis.py`: Analyzes word and author co-occurrence in a dataset, identifying common themes, detecting misinformation trends, and understanding user engagement. It combines co-occurrence analysis with sentiment analysis for comprehensive insight.
- `tocsv.py`: Converts `.zst` files to `.csv` format, tailored for handling large datasets. It manages JSON decoding issues and missing keys, making it ideal for data analysis scenarios with large, compressed datasets.
- `viz.py`: Analyzes and visualizes sentiment data from a dataset containing comments and posts from specific subreddits. Essential for sentiment analysis projects, especially for understanding public opinion and tracking sentiment trends.

## Contributing

We welcome contributions to this project! If you're interested in helping, please:

1. Fork the repository.
2. Create a feature branch: `git checkout -b new-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin new-feature`.
5. Submit a pull request.

Please ensure your code adheres to the project's coding standards and include any necessary tests.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.

The GNU General Public License is a free, copyleft license for software and other kinds of works, ensuring that all modified versions of the project are also free and open source. By using this license, we guarantee the user's freedom to share and change the software, and that all versions of the software are protected in the same way.

