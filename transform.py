import pandas as pd
import numpy as np
import re


# Define a function to extract min and max salary along with the period
def extract_salary(salary):
    min_salary = max_salary = np.nan  # Initialize both to NaN

    if pd.notna(salary) and "₹" in salary:
        # Case with range "₹min - ₹max"
        if " - " in salary:
            min_salary, max_salary = salary.split(" - ")
            # Remove commas and allow decimal points
            min_salary = float(re.sub(r"[^\d.]", "", min_salary))
            max_salary = float(re.sub(r"[^\d.]", "", max_salary))

        # Case with "Up to ₹amount"
        elif "Up to" in salary:
            min_salary = np.nan
            max_salary = float(re.sub(r"[^\d.]", "", salary))

        # Case with "From ₹amount"
        elif "From" in salary:
            min_salary = float(re.sub(r"[^\d.]", "", salary))
            max_salary = np.nan

        # Determine the period (month/year)
        if "a month" in salary.lower():
            period = "month"
        elif "a year" in salary.lower():
            period = "year"
        else:
            period = np.nan

        # Return the salaries as floats, and the period
        return min_salary, max_salary, period
    else:
        return np.nan, np.nan, np.nan


def transform():
    # Load the DataFrame
    df = pd.read_csv("python_jobs.csv")
    # Apply the function to extract min_salary, max_salary, and period
    df[['min_salary', 'max_salary', 'salary_period']] = df['salary'].apply(lambda x: pd.Series(extract_salary(x)))

    # Calculate average salary with `mean` handling NaN values correctly
    df['average_salary'] = df[['min_salary', 'max_salary']].mean(axis=1)

    # Calculate yearly average salary based on salary period
    df['yearly_avg_salary'] = np.where(
        df['salary_period'] == 'month',
        df['average_salary'] * 12,
        df['average_salary']
    )
    # Save to CSV if needed
    df.to_csv("transformed.csv", index=False)

    # Drop and save cleaned data
    df1 = df.drop(['min_salary', 'max_salary', 'salary_period', 'average_salary'], axis=1)
    df1.to_csv("final.csv", index=False)
    print('Final csv generated!')
