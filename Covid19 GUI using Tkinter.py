from tkinter import *
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

root = Tk()

root.title('Covid 19 Details Of India')
root.iconbitmap('icon.ico')

root.geometry('800x550+225+50')
root.config(bg='dark blue')

logoimage=PhotoImage(file='stayhome.png')

logoLabel=Label(root,image=logoimage,bg='dark blue')
logoLabel.pack()
root.title("Covid-19 Tracker - By Country")

URL = " https://www.worldometers.info/coronavirus/#countries"
html_page = requests.get(URL).text
soup = BeautifulSoup(html_page, 'html.parser')
get_table = soup.find("table", id="main_table_countries_today")
get_table_data = get_table.tbody.find_all("tr")
dic = {}
for i in range(len(get_table_data)):
    try:
        key = get_table_data[i].find_all("a", href=True)[0].string
    except:
        key = get_table_data[i].find_all("td")[0].string

    values = [j.string for j in get_table_data[i].find_all('td')]
    dic[key] = values

df = pd.DataFrame(dic).iloc[1:, :].T.iloc[:, :9]
df.index_name = "country"
newdf = pd.DataFrame(df.values,
                     columns=['Country', 'Total Cases', "New Cases", "Total Deaths", "New Deaths", "Total Recovered",
                              'New Recovered', "Active", "Serious Critical"])

newdf = newdf.drop(columns=['New Cases', 'New Deaths', 'New Recovered', 'Serious Critical'])
newdf.replace(np.nan, 0)
newdf = newdf.iloc[1:]

list_of_countries = newdf['Country'].to_list()



def pieDisplayData():
    from covid import Covid
    from matplotlib import pyplot as plt


    covid = Covid(source='worldometers')
    cases = []
    active = []
    deaths = []
    recovered = []
    try:
        root.update()
        countries = clicked.get()
        country_names = countries.strip()
        country_names = country_names.replace(" ", ",")
        country_names = country_names.split(",")
        for country in country_names:
            cases.append(covid.get_status_by_country_name(country))
            root.update()

        for case in cases:
            active.append(case['active'])
            deaths.append(case['deaths'])
            recovered.append(case['recovered'])
        parameters = [sum(active),sum(deaths),sum(recovered)]
        parameters2 = ["active cases","deaths","Recovered"]
        cl=["blue","green","orange"]
        plt.pie(parameters,labels = parameters2, explode = (0.1,0.1,0),colors=cl,autopct= "%1.2f%%")
        plt.axis('equal')
        plt.show()
    except Exception as e:
        print(f"Enter correct details country. \n {e}")


label1=Label(root, text="Select country name for whom you want to get COVID information !", font="Consolas 15").pack()


label2=Label(root, text="Country : ").pack()


clicked = StringVar()

clicked.set("Select Country From the List")

drop = OptionMenu(root, clicked, *list_of_countries).pack()
Button( root , text = "Show Live Status" , command = pieDisplayData ).place(x=350, y=380)

root.mainloop()

