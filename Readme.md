# Project Title
---

<font size = 5>Webscraping Real Estate Websites for Housing Market Analysis</font>

**<font color = 'green' size=4>Project Summary</font>**

In this project we will scrape the **REMAX** website (https://www.remax.ca/) to get information of the housing properties up for sale in different cities across different provinces in Canada. We will be using **Selenium** to assist in scraping the **REMAX** for both the basic and detailed information of each listing across different pages. We will use this scraped data do the following:

- Map these listings to quickly identify regions based on their price
    
- Plot distributions of housing prices across different regions for comparison

- Visualize housing price distribution based on housing type (condos, single family etc.)

- Find average price of listing across different cities and identify most and least expensive cities

- Identify top 10 most expensive and top 10 least expensive listings

- Analyze *Price* vs *Square Footage* trend for each region and identify any similarities or discrepancies

**<font color = 'green' size=4>List of steps followed:</font>**
- **Step 1**: Gather basic and details data from **REMAX** website for various cities and save them locally
- **Step 2**: Append all the saved scraped data as one pandas dataframe
- **Step 3**: Merge basic and details data on unique #MLS key, perform EDA and treat missing data
- **Step 4**: Correct data types , extract new features and remove redundant or misleading data
- **Step 5**: Use geopy library to extract latitude and longitude coordinates using the address of each listings and add it to dataframe
- **Step 6**: Create a dashboard using **Plotly** and **Dash** to answer all the questions
- **Step 7**: Deploy the dashboard on **heroku** (https://housingmarketanalysis.herokuapp.com/)
