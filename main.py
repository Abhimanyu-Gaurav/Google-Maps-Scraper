from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from playwright.sync_api import sync_playwright

app = FastAPI()

class SearchRequest(BaseModel):
    search: str
    total: int = 1

def extract_data(xpath, data_list, page):
    try:
        if page.locator(xpath).count() > 0:
            data = page.locator(xpath).inner_text(timeout=5000)  # Set a 5-second timeout for each locator
        else:
            data = ""
        data_list.append(data)
    except Exception as e:
        data_list.append("")  # If there's an error, append an empty string
        print(f"Error extracting data for xpath {xpath}: {str(e)}")


def scrape_google_maps(search_for: str, total: int):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(2000)

        # Fill the search term
        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.keyboard.press("Enter")
        page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]', timeout=10000)

        # Initialize scrolling variables
        previously_counted = 0
        scroll_attempts = 0
        listings = []

        # Enhanced scrolling mechanism to load more results
        while len(listings) < total:
            # Scroll down the page to load more results
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)  # Wait for results to load
            
            # Get the number of current results
            current_count = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()

            # Break if we've scrolled enough but new results are not loading
            if current_count == previously_counted:
                scroll_attempts += 1
                if scroll_attempts > 5:  # Max 5 attempts to avoid infinite scrolling
                    break
            else:
                scroll_attempts = 0  # Reset attempts when new results load

            previously_counted = current_count

            # Get the new listings found after scrolling
            if current_count > 0:
                new_listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                listings.extend([listing.locator("xpath=..") for listing in new_listings])
                listings = listings[:total]  # Limit to the total number required

        if len(listings) == 0:  # If no listings were found, raise an exception
            raise HTTPException(status_code=404, detail="No listings found")

        # Initialize lists for scraped data
        names_list, address_list, website_list, phones_list = [], [], [], []

        # Scraping the required data
        for listing in listings[:total]:  # Limit to the required number of listings
            listing.click()
            page.wait_for_selector('//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]')

            name_xpath = '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'

            extract_data(name_xpath, names_list, page)
            extract_data(address_xpath, address_list, page)
            extract_data(website_xpath, website_list, page)
            extract_data(phone_number_xpath, phones_list, page)

        # Close the browser
        browser.close()

        # Return data as dictionary
        return pd.DataFrame(list(zip(names_list, address_list, website_list, phones_list)),
                            columns=['Name', 'Address', 'Website', 'Phone Number']).to_dict(orient="records")

@app.post("/scrape/")
def scrape_data(request: SearchRequest):
    try:
        results = scrape_google_maps(request.search, request.total)
        return {"data": results}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
