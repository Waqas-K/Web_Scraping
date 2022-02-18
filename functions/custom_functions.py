#-----------------------------------------------------------------
# Import Libraries
#-----------------------------------------------------------------
from time import sleep # To prevent overwhelming the server between connections
import pandas as pd # For converting results to a dataframe and bar chart plots
import numpy as np
import random # For using it to generate random time intervals
import re     # For regular expressions searches within strings
from selenium import webdriver

# Geocoding Libraries to get Lat Long from address
from geopy.geocoders import Nominatim # For converting address to Lat Long
geolocator = Nominatim(user_agent="remax_app")


#-----------------------------------------------------------------
# Web Scraping Function
#-----------------------------------------------------------------
def web_scrape(province,city,num_pages, chrome_driver_path):
    '''

    This function scrapes the listing information of real estate properties from
    REMAX website and store the into two seperate lists basic_info and detail_info lists.

    INPUTS:
    province : Name of province in Canada such as (on, bc, ab, sk, ns, mb)
    city     : Name of city in Canada such as (toronto, vancouver, ottawa, calgary, halifax,
    saskatoon, edmonton, winnipeg, hamilton, surrey)
    num_pages : Number of webpages to scrape information from.

    Note: Make sure that the city names are consitent with the province names and that maximum
    num_pages should not exceed the actual pages on REMAX website for each city.

    OUTPUTS:
    basic_info : List which stores basic information of houses
    detail_info : List which stores detailed information of houses

    '''

    #-----------------------------------------------------------------
    # Initialize Empty Lists to Store Data as Retrived from each page
    #-----------------------------------------------------------------

    # Opens and Initializes the Selenium browser
    driver = webdriver.Chrome(chrome_driver_path)

    # Initialize empty lists to store basic information
    basic_info = []

    # Initialize empty list to store detailed information data
    detail_info = []

    # Start a counter to keep track of number of units scraped
    counter = 0

    #-----------------------------------------------------------------
    # Loop over number of pages
    #-----------------------------------------------------------------
    for page in range(1, num_pages+1):

        # Get the url path based on province, city and page
        url_path = f'https://www.remax.ca/{province}/{city}-real-estate?pageNumber={page}'
        print(f'Scraping this url now => {url_path}')

        # Go to the webpage using Selenium driver
        driver.get(url_path)

        # Add random sleep to prevent being blocked by website
        sleep(random.randint(2,10))

        # Find all card tags on web page using class name
        # card_tags = driver.find_elements_by_class_name('listing-card_listingCard__3SoUb')
        card_tags = driver.find_elements_by_class_name('listing-card_listingCard__G6M8g')

        #-----------------------------------------------------------------
        # Loop over all card_tags
        #-----------------------------------------------------------------
        for tag in card_tags:

            # Extract text from basic information tags and append them together
            basic_info.append(tag.text)

            # Get details information by clicking on each tag (opens a new window in a new tab)
            #-----------------------------------------------------------------

            # Click on each listings
            tag.click()

            # Add random sleep to prevent being blocked by website
            sleep(random.randint(2,10))

            # Obtain parent window handle
            parent = driver.window_handles[0]

            # Obtain browser tab window handle
            tab = driver.window_handles[1]

            # Switch to tab browser
            driver.switch_to.window(tab)


            try:
               # Find details button using xpath and click on it
                driver.find_element(by='xpath',
                                    value = '//*[@id="details"]/div[2]/button/span').click()

                # Sleep for a few seconds before extracting details information
                sleep(2)

                # Find detail section using id, extract details and append them as text
                detail_info.append(driver.find_element(by = 'id', value='details').text)

                # Update counter for a succesfull scrape
                counter += 1
                print(f'Scraped {counter} homes')

            except:
                # If details page is missing print
                print('Details missing')

            # Add random sleep to prevent being blocked by website
            sleep(random.randint(2,10))

            # Close tab browser before opening the next one
            driver.close()

            # Switch to parent window and repeat the process for all tags
            driver.switch_to.window(parent)

    return basic_info, detail_info


#-------------------------------------------------------------------------------------------
# Function to rename duplicated attributes/column names with a number sequence to distinguish
#-------------------------------------------------------------------------------------------
def rename(df, column):
    '''
    Renames duplicated column names and adds a sequnce of numbers after to distinguish it
    from others
    INPUTS
    df: dataframe
    column: column name which has duplicates to be renamed

    OUTPUT
    dataframe column with renamed columns
    '''
    appendents = (df.groupby(column).cumcount().astype(str).replace('0',''))
    return (df[column] + appendents)

#-------------------------------------------------------------------------------------------
# Function to convert scraped lists into pandas DataFrames
#-------------------------------------------------------------------------------------------
def listtodataframe(basic_info, detail_info):
    '''
    Function to convert scraped list of basic_info and detail_info in to respective dataframes
    INPUTS
    basic_info: basic information list generated from web_scrape function
    detail_info: detailed information list generated from web_scrape function

    OUTPUTS
    basic_df: dataframe of basic information
    details_df: dataframe of details information
    '''
    #---------------------------------------------------------------------------------------
    # Create Basic Dataframe using basic_info
    #---------------------------------------------------------------------------------------
    # Few tags have an extra attribute of sqft area, remove it to enure consistency of
    # column names before merging together as dataframe. For this we will be using
    # regex

    # Identify pattern for extra sqft area attribute and replace by ''
    pattern = '(\d+.*)(sqft)\n'
    replace = ''
    basic_df =  pd.DataFrame(re.sub(pattern, replace, txt).split('\n') for txt in basic_info)

    # Rename columns of basic df
    column_names = ['Price', 'Beds', 'Baths', 'Address', 'MLS#', 'Tag1', 'Tag2']
    basic_df.columns = column_names

    # Split mls# column to keep on the number part
    basic_df['MLS#'] = basic_df['MLS#'].apply(lambda x:x.split(':')[1])

    #---------------------------------------------------------------------------------------
    # Create Details Dataframe using detail_info
    #---------------------------------------------------------------------------------------
    details_df = pd.DataFrame()

    for txt in detail_info:
        # Create a dummy dataframe for each listings and appedn together to create one
        # unified details_df data frame

        # First split on new line
        dummy = pd.DataFrame(txt.split('\n'))

        # Split on ':' and get length of list after split
        dummy['Null_Attributes_Flag'] = (dummy[0].apply(lambda x:len(x.split(':'))))

        # Remove all attributes where attribute values are missing
        dummy = dummy[dummy['Null_Attributes_Flag']>1]

        # Extract Attributes and Values and store as seperate columns
        dummy['Attributes'] = dummy[0].apply(lambda x:x.split(':')[0])
        dummy['Values'] = dummy[0].apply(lambda x:x.split(':')[1])

        # Drop irrelevant columns
        dummy = dummy.drop(columns=[0,'Null_Attributes_Flag'], axis=1)

        # Run rename function to rename duplicated entries
        dummy['Attributes'] = rename(dummy, 'Attributes')

        # Transpose the dataframe
        dummy = dummy.set_index('Attributes').transpose()

        # Append to details_df and repeat for all entries in detail_info
        details_df = details_df.append(dummy)

    # drop the redundant index in the end
    details_df.reset_index(drop=True, inplace=True)

    return basic_df, details_df


#-------------------------------------------------------------------------------------------
# Function to Generate Data Statistics of a DataFrame
#-------------------------------------------------------------------------------------------

def missing_data_stats(df):
    '''
    Reads a dataframe and generates its statistics and missing value tables
    INPUTS:
    df = pandas dataframe

    OUTPUTS:
    data_stats = basic data statistics of dataframe
    sorted_missing_data_stats = sorted missing values statistics table
    similar_missing_value_cols = missing values grouped by similar missing percentages
    nan_count_rows = count of miising values per row
    '''
    #---------------------------------------------------------------------------
    # Dataframe Statistics
    #---------------------------------------------------------------------------
    data_stats = df.describe(include='all').transpose()

    #---------------------------------------------------------------------------
    # Count Missing Values
    #---------------------------------------------------------------------------
    missing_data_stats=pd.DataFrame(df.isnull().sum(),columns=['Missing_Values'])

    #---------------------------------------------------------------------------
    # Perform an assessment of how much missing data there is in each column of the dataset
    #---------------------------------------------------------------------------
    missing_data_stats['Missing_Percentage']=(missing_data_stats['Missing_Values']/len(df))*100
    sorted_missing_data_stats=missing_data_stats.sort_values(by='Missing_Percentage',ascending=False)

    #---------------------------------------------------------------------------
    # Calculate the count of columns missing similar percentage of data
    #---------------------------------------------------------------------------
    sorted_missing_data_stats['Missing_Percentage_Rounded']=sorted_missing_data_stats['Missing_Percentage'].round()
    sorted_missing_data_stats.index.name = 'Feature'
    similar_missing_value_cols = (sorted_missing_data_stats.drop('Missing_Percentage',axis=1).groupby(
                                                                            by='Missing_Percentage_Rounded').count())

    #---------------------------------------------------------------------------
    # How much data is missing in each row of the dataset?
    # Sum all the missing values by rows
    #---------------------------------------------------------------------------
    nan_count_rows=df.isnull().sum(axis=1).sort_values(ascending=False)

    return data_stats, sorted_missing_data_stats,\
           similar_missing_value_cols,nan_count_rows

#---------------------------------------------------------------------------
# Function convert total area strings into values
#---------------------------------------------------------------------------
def sqft_area(dataframe, sqft_column):
    '''
    Takes square footage column as an input and extracts numbers from it
    where a range is reported like 600-700 an average of these numbers is taken'''

    total_sqft = []
    for rows in dataframe[sqft_column]:
        try:
            value1 = float(re.findall('\d+.\d+', rows)[0])

            try:
                value2 = 0.5*(float((value1.split('-')[0]))+float((value1.split('-')[1])))
                total_sqft.append(value2)
            except:
                total_sqft.append(value1)

        except:
            total_sqft.append(np.NaN)
    return total_sqft

#---------------------------------------------------------------------------
# Function to flatten lists
#---------------------------------------------------------------------------
def flatten(t):
    return [item for sublist in t for item in sublist]

#---------------------------------------------------------------------------
# Function generate area from room dimension tables
#---------------------------------------------------------------------------
def area_from_dims(table, column):
    length = []
    width = []

    for rows in table[column]:

        # Identify pattern for area dimensions and extract values to get the area
        dim1 = '(\d+.*)[xX]'
        dim2 = '[xX](.\d+.*)'

        dim11 = '(\d.*)[\w]'
        dim22 = '(\d.*)[\w]'

        le = re.findall(dim11, str(re.findall(dim1, rows)))
        wi = re.findall(dim22, str(re.findall(dim2, rows)))

        if len(le)>0 and len(wi)>0:
            length.append(le)
            width.append(wi)
        else:
            length.append([0])
            width.append([0])


    length = flatten(length)
    width = flatten(width)

    area = []

    for l,w in zip(length,width):
        try:
            area.append(round(float(l.replace("'",''))*float(w.replace("'",'')), 2))
        except:
            area.append(0)

    return area


#---------------------------------------------------------------------------
# Function to convert address to lat long coordinates
#---------------------------------------------------------------------------
def latlong(address):
    '''
    Function to convert address to lat long coordinates
    '''
    try:
        location = geolocator.geocode(address)
        lat  = location.latitude
        lon = location.longitude
    except:
        # print(f'Missing or Wrong Address: {address}')
        lat = np.NaN
        lon = np.NaN

    return lat, lon
