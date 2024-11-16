import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
# Function to scrape jobs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# List of user agents to rotate
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]


# Function to get a random user agent
def get_random_user_agent():
    return random.choice(user_agents)


# Set up Selenium with random user-agent
def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={get_random_user_agent()}")

    driver_path = "C:\\Windows\\chromedriver.exe"  # Set the correct path to your chromedriver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scrape_jobs(query, location):
    base_url = "https://in.indeed.com/jobs"
    params = {"q": query, "l": location}  # Added location parameter

    driver = init_driver()

    # Scrape all pages
    job_listings = {}  # Dictionary to store unique jobs
    page = 0
    while True:
        params["start"] = page
        url = base_url + "?" + "&".join(f"{key}={value}" for key, value in params.items())
        print(f"Scraping URL: {url}")
        driver.get(url)
        time.sleep(random.uniform(3, 6))  # Throttling between requests

        try:
            # Wait for job listings to load before extracting
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job_seen_beacon")))

            job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
            if not job_cards:
                print(f"No job listings found on page {page}, ending the scrape.")
                break

            for card in job_cards:
                job_info = {}
                try:
                    job_info["title"] = card.find_element(By.CLASS_NAME, "jobTitle").text.strip()
                except:
                    job_info["title"] = None
                try:
                    job_info["company"] = card.find_element(By.CLASS_NAME, "css-1h7lukg").text.strip()
                except:
                    job_info["company"] = None
                try:
                    job_info["location"] = card.find_element(By.CLASS_NAME, "css-1restlb").text.strip()
                except:
                    job_info["location"] = None
                try:
                    job_info["salary"] = card.find_element(By.CLASS_NAME, "css-18z4q2i").text.strip()
                except:
                    job_info["salary"] = None

                # Check if title contains 'python' (case-insensitive)
                if job_info["title"] and "python" in job_info["title"].lower():
                    # Using a combination of title and company as a unique key
                    job_key = (job_info["title"], job_info["company"], job_info["location"], job_info["salary"])

                    # Add to dictionary (ensures no duplicates)
                    if job_key not in job_listings:
                        job_listings[job_key] = job_info

            # Check for next page: Look for a 'Next' button or link
            try:
                next_button = driver.find_element(By.XPATH,
                                                  "//a[contains(@aria-label, 'Next') or contains(text(), 'Next')]")
                if next_button:
                    page += 10  # Move to the next page
                else:
                    print("No more pages, stopping the scrape.")
                    break
            except Exception as e:
                print("No 'Next' button found, ending scrape.")
                break

        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            # break

    driver.quit()

    # Convert dictionary values to a list
    return list(job_listings.values())


# Function to save job listings to CSV
def save_to_csv(job_listings, filename="python_jobs.csv"):
    # Define CSV fieldnames (headers)
    fieldnames = ["title", "company", "location", "salary"]

    # Open the CSV file in write mode
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write each job listing to the CSV file
        for job in job_listings:
            writer.writerow(job)

    print(f"Job listings have been saved to {filename}")
