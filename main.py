import datetime as dt
import random
import os
import pandas
import smtplib

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

data= pandas.read_csv(r"./birthdays.csv")
bday_dic= {(data_row.day,data_row.month):data_row for (index,data_row) in data.iterrows()}
now=dt.datetime.now()
celebrant_bday= (now.day,now.month)
store_message=[]

if celebrant_bday in bday_dic:
    rand_template=random.choice(os.listdir(r"./letter_templates"))
    with open(rf"./letter_templates/{rand_template}") as bday_file:
        bday_message=bday_file.read()
        new_bday_message= bday_message.replace("[NAME]", bday_dic[celebrant_bday]["name"])
        store_message.append(new_bday_message)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL,password=MY_PASSWORD)
        bday_messages= "".join(store_message)
        connection.sendmail(from_addr=MY_EMAIL,to_addrs=bday_dic[celebrant_bday]["email"],msg=f"Subject:HURRAY!!!\n\n{bday_messages}")
