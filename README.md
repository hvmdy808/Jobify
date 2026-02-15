# Overview
Scrapes job listings from Wuzzuf, cleans and analyzes the data to identify the most in-demand data-related roles and skills. Designed for scalability with planned extensions including multi-country support, NLP-based skill extraction, ML classification, Streamlit dashboards, and database integration.
# Current State
Program is runnable now and the data is around 21k rows.
The data is not saved in csv or cleaned yet but is to be saved soon.
Each row contains a pair of job title and a required skill associated with it, and also some data about the location and employment type.
This way of representing the data provides a normalized-like version of data.
Each job has more than one row, exactly the number of skills.
