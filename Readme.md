# Google Maps Scraper

**Technologies:** Python, Playwright, FastAPI, Pandas

- This Python script utilizes the Playwright library to perform web scraping and data extraction from Google Maps. It is designed to gather business information such as name, address, website, phone number, and more.
- This web service uses FastAPI to scrape data and return it as JSON or CSV, supporting up to X listings at a time.
- Processed and exported data efficiently with Pandas, handling error scenarios to ensure robust scraping.

## Table of Contents
- [Prerequisite](#prerequisites)
- [Key Features](#key-features)
- [Installation](#installation)
- [How to Use](#how-to-use)
- License

## Prerequisites

- Python version **above 3.11** is required.
- Ensure Playwright is installed and set up with your browser.
- This script uses the FastAPI framework and requires Pandas for organizing data.

## Key Features

- **Data Scraping:** Extracts valuable information like business names, addresses, websites, and contact details from Google Maps listings.
- **Flexible Search:** Provides an option to specify the number of listings (`total`) to scrape.
- **Data Cleansing:** Organizes and cleans the extracted data.
- **Error Handling:** The script has error handling for missing data or elements, ensuring the scraper continues working even if some data is missing.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Abhimanyu-Gaurav/Map_Scraper_Playwright

2. Navigate to the project directory:
   ```bash
   cd Map_Scraper_Playwright
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Ensure Playwright is installed and browsers are ready:
   ```bash
   playwright install
   
## How to Use

1. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload


2. Open your browser (Safari, Chrome, Brave) and enter the URL:
   ```bash
   http://localhost:8000/docs#

3. This should display the Swagger UI for your FastAPI application.

4. Test the /scrape endpoint directly from the Swagger UI to ensure it is working and accessible.

5. Use the POST method (/scrape) and provide a JSON in the body like this:
    - Click on the "Try it out" button.
    - Provide a JSON in the request body:
    ```json
    {
        "search": "Restaurants in Delhi",
        "total": 50
    }

6. Click on the "Execute" button to send the request.

7. You should see the scraped data in the response section if the request is successful.
   

### Send a POST request using API clients:
1. Using Postman:
    - Open Postman and click the "New" button to create a new request.
    - Set the request type to POST from the dropdown menu next to the URL field.
    - Enter the URL in the URL field:
      ```bash
      http://localhost:8000/scrape/

    -  Go to the "Body" tab.
        - Select the "raw" option and choose "JSON" from the dropdown.
        - Paste the following JSON into the body:
        ```json
        {
            "search": "Restaurants in Delhi",
            "total": 10
        }

    - Click the "Send" button to execute the request.
    - You should see the scraped data in the response section if the request is successful. 

2. Using cURL:
- Open your terminal and run:
    ```bash
    curl -X POST "http://localhost:8000/scrape/" -H "Content-Type: application/json" -d '{"search": "Restaurants in Delhi", "total": 5}'
    
- search: The term you want to search (e.g., business name or type).
- total: The number of listings to retrieve (if available).
    

## License

- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
