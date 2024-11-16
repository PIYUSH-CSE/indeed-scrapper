from scrapper import *
from transform import *
from load import *

# Example usage
jobs = scrape_jobs("Python+developer", "")  # Passing both query and location
print(f"Total jobs found: {len(jobs)}")
for job in jobs[:5]:  # Print first 5 job listings
    print(job)

# Save the filtered data to a CSV file
save_to_csv(jobs)

# Transforms the raw data
transform()

# loads data into mongodb
load()
