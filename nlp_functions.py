# a Python script for performing natural language processing (NLP) tasks on text data using the spaCy library. 
# It focuses on extracting various types of entities (countries, individuals, organizations, and locations) from a given text and demonstrates the process on specific item data read from a CSV file.

# Load the spaCy English model
import spacy 
import pandas as pd 

nlp = spacy.load("en_core_web_trf")

# Specify the path to the CSV file containing the data
path = "output.csv"

# Read the data
data = pd.read_csv(path)

# Select specific item data
# Extract specific columns ('Title', 'Summary', 'Tags') from the DataFrame for a particular row (row 10) and store it in the item_data variable.
item_data = data.loc[10, ['Title', 'Summary', 'Tags']]


# ENTITY EXTRACTION FUNCTIONS
# Define four functions (extract_countries, extract_individuals, extract_organizations, and extract_locations) that take an input article (text) and use spaCy to extract entities of specific types (GPE for countries, PERSON for individuals, ORG for organizations, and LOC for locations). 
# These functions return a list of unique entities of the specified type found in the article.

# Extract countries
def extract_countries(article):
    doc = nlp(article)
    countries = []
    
    for ent in doc.ents:
        if ent.label_ == "GPE":
            countries.append(ent.text)
    
    return list(set(countries))

# Extract individuals
def extract_individuals(article):
    doc = nlp(article)
    individuals = []
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            individuals.append(ent.text)
    
    return list(set(individuals))

# Extract organizations
def extract_organizations(article):
    doc = nlp(article)
    organizations = []
    
    for ent in doc.ents:
        if ent.label_ == "ORG":
            organizations.append(ent.text)
    
    return list(set(organizations))

# Extract locations
def extract_locations(article):
    doc = nlp(article)
    locations = []
    
    for ent in doc.ents:
        if ent.label_ == "LOC":
            locations.append(ent.text)
    
    return list(set(locations))

# Extract individual elements from the Series 
# Convert the individual elements of the item_data DataFrame (Title, Summary, and Tags) to string format and store them in separate variables (title, summary, tags))
title = str(item_data['Title'])
summary = str(item_data['Summary'])
tags = str(item_data['Tags'])

# Print the item data and extracted information
print("Title:", title)
print("Summary:", summary)
print("Tags:", tags)

# Combine the text from title, summary, and tags
combined_text = title + " " + summary + " " + tags

# Extract and print the entities
# Call the entity extraction functions (extract_countries, extract_individuals, extract_organizations, and extract_locations) on the combined_text and print the extracted entities for each type.
print("Countries:", extract_countries(combined_text))
print("Individuals:", extract_individuals(combined_text))
print("Organizations:", extract_organizations(combined_text))
print("Locations:", extract_locations(combined_text))
