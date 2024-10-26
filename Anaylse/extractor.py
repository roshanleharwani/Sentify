import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.5paisa.com/stocks/all"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36"
}

response = requests.get(url, headers=headers)


soup = BeautifulSoup(response.content, "html.parser")

stock_div = soup.findAll("div", class_="stock-directory__listname")
print("Extracting Stocks....")
stock_list = []

if stock_div:
    stock_items = stock_div[0].find_all("li")

    for item in stock_items:
        stock_name = item.find("a").text.strip()
        stock_list.append(stock_name)

with open("indian_stocks.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Stock Name"])

    for stock in stock_list:
        writer.writerow([stock])

print(f"Successfully extracted {len(stock_list)} stocks and saved to indian_stocks.csv")
