# Overview
Scrapes job listings from Wuzzuf, cleans and analyzes the data to identify the most in-demand data-related roles and skills. Designed for scalability with planned extensions including multi-country support, NLP-based skill extraction, ML classification, Streamlit dashboards, and database integration.
# Current State
Program is runnable now and the data is around 21k rows.
The data is saved to a csv file named initial.csv in the folder named data.
Cleaning scripts for data are in the notebook and are to be added soon to the src package.
A better doc for the cleaning in the notebook is to be added also ISA.
Each row contains a pair of job title and a required skill associated with it, and also some data about the location and employment type.
This way of representing the data provides a normalized-like version of data.
Each job has more than one row, exactly the number of skills.
