# Web Scraping with Selenium, BeautifulSoup and Pandas

This Python code scrapes data from the website "www.olx.ro", which is a Romanian online marketplace. Specifically, it retrieves information about any any category on the sie for example accounting and translation services in Iasi city, which are advertised on this website. 

The code is structured as follows:
- The `scrap_link(at)` function scrapes all the links of the advertisements for accounting and translation services in Iasi city. It returns a list of unique links to the advertisements.
- The `open_browser(at)` function opens a Chrome browser and goes to the given url. It clicks the "Accept" button for the website's cookie policy.
- The `go_to(driver, at)` function navigates the browser to the given url.
- The `show_number(driver)` function checks if the phone number of the advertisement is present and clicks the "Show phone number" button if it exists.
- The `scrap_data(links)` function loops through all the links and scrapes various information about the advertisements, such as tags, location, title, description, author, phone number, about us and images. It uses the above functions to navigate and interact with the website. It returns a Pandas DataFrame with all the scraped data.
- The `save_file(df, at)` function saves the scraped data as a CSV file.

The `main()` function ties all these functions together and executes the web scraping process. It uses the `scrap_link(at)` function to get the links to scrape, then uses the `scrap_data(links)` function to retrieve the data from those links. Finally, it uses the `save_file(df, at)` function to save the scraped data to a CSV file.

Note that this code requires the installation of the following Python packages: selenium, pandas, beautifulsoup4, requests, webdriver_manager. It also requires the installation of the Chrome browser and the ChromeDriver executable.
