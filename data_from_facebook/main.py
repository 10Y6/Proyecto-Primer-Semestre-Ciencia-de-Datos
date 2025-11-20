import models as md

while True:
    #date == -1 break the cicle
    date = input("date: ")
    data = md.create_data(date)
    breaker = md.add_data(data)
    if breaker == -1:break