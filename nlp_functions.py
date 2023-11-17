# Load the spaCy English model
import spacy 
import pandas as pd 

nlp = spacy.load("en_core_web_trf")

# Set CSV path
path = "output.csv"

# Read the data
data = pd.read_csv(path)

# Select specific item data
item_data = data.loc[10, ['Title', 'Summary', 'Tags']]

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
print("Countries:", extract_countries(combined_text))
print("Individuals:", extract_individuals(combined_text))
print("Organizations:", extract_organizations(combined_text))
print("Locations:", extract_locations(combined_text))