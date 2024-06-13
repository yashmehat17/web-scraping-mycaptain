import requests
from bs4 import BeautifulSoup
import pandas

oyo_url = "https://www.oyorooms.com/hotels-in-surat/?checkin=30%2F09%2F2023&checkout=01%2F10%2F2023&filters%5Bcity_id%5D=60&guests=1&roomConfig=1&roomConfig%5B%5D=1&rooms=1"

req = requests.get(oyo_url)
content = req.content

soup = BeautifulSoup(content, "html.parser")

all_hotels = soup.find_all("div", {"class": "hotelCardListing"})
scraped_info_list = []

for hotel in all_hotels:
    hotel_dict = {}
    hotel_dict["name"] = hotel.find("h3", {"class": "listingHotelDescription__hotelName"}).text
    hotel_dict["address"] = hotel.find("span", {"itemprop": "streetAddress"}).text
    hotel_dict["price"]= hotel.find("span", {"class": "listingPrice__finalPrice"}).text
    try: 
        hotel_dict["rating"]= hotel.find("span", {"class": "hotelRating__ratingSummary"}).text
    except AttributeError:
        pass 

    parent_amenities_element = hotel.find("div", {"class": "amenityWrapper"})

    amenities_list = []
    for amenity in  parent_amenities_element.find_all("div", {"class": "amenityWrapper__amenity"}):
        amenities_list.append(amenity.find("span", {"class": "d-body-smd-textEllipsis"}).text.strip())

    hotel_dict["amenities"] = ', '.join( amenities_list[:-1])   

    scraped_info_list.append(hotel_dict)


    #print(hotel_name, hotel_address, hotel_price, hotel_rating, amenities_list)

dataFrame = pandas.DataFrame( scraped_info_list)   
dataFrame.to_csv("Oyo.csv")
