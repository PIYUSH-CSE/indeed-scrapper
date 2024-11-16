# Indeed-Scrapper


This project is intended to scrape Jobs for Python Developer role from "https://in.indeed.com/jobs".

scrapper.py is responsible for extracting fields from indeed. Extracted fileds would be: JobTitle, CompanyName, Location and Salary and storing them in python_jobs.csv.

transform.py is responsible for performing transformation on the scrapped data stored in python_jobs.csv and storing them into different file i.e transformed.csv and then to final.csv.

load.py is responsible for loading the data from final.csv into mongodb database.

main.py is responsible for running all the python scripts mentioned above.
