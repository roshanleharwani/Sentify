from datetime import datetime


date = "2020-01-01"
date = datetime.strptime(date, "%Y-%m-%d")

print(type(date))
print(date)
