#Data from https://hotell.difi.no/?dataset=vegvesen/kjoretoyinfo2

import re
import panda as pd

#Cleanup
with open('kjoretoyinfo2.csv', 'r') as read_stream:
    with open('kjoretoyinfo2_clean2.csv', 'w') as write_stream:        
        regex = re.compile(r'\\"')
        write_stream.write(regex.sub("", read_stream.read()))
   
#Load   
data=pd.read_csv('kjoretoyinfo2_clean2.csv',sep=';')

#Crop to cars (M1 category) registered in 2023|2024
carsRegIn2023=data.query('20230000 <  tekn_reg_f_g < 20240000 and tekn_tknavn == "M1"')
carsRegIn2024=data.query('20240000 <  tekn_reg_f_g < 20250000 and tekn_tknavn == "M1"')

#Print manufacturer numbers for 2023
print(carsRegIn2023['tekn_merkenavn'].value_counts().to_string())
#Print model numbers for 2023|2024
print(carsRegIn2023['tekn_modell'].value_counts().to_string())
print(carsRegIn2024['tekn_modell'].value_counts().to_string())

#Crop to cars (M1 category) registered in 2023|2024, that are not EV (tekn_drivstoff no 5, 5,5 or 5,5,5, possibly one 5 for each electric motor?)
nonEVcarsRegIn2023=data.query('20230000 <  tekn_reg_f_g < 20240000 and tekn_tknavn == "M1" and tekn_drivstoff != "5" and tekn_drivstoff != "5,5" and tekn_drivstoff != "5,5,5"')
nonEVcarsRegIn2024=data.query('20240000 <  tekn_reg_f_g < 20250000 and tekn_tknavn == "M1" and tekn_drivstoff != "5" and tekn_drivstoff != "5,5" and tekn_drivstoff != "5,5,5"')

print(nonEVcarsRegIn2023['tekn_merkenavn'].value_counts().to_string())
print(nonEVcarsRegIn2023['tekn_modell'].value_counts().to_string())

#Export model numbers to csv
models=nonEVcarsRegIn2023['tekn_modell'].value_counts()
models.to_csv('Models2023.csv')

#Check out the Ferarris currently registered
ferarris=data.query('tekn_merkenavn== "FERRARI" and tekn_reg_status == "REGISTRERT"')
print(ferarris['tekn_modell'].value_counts().to_string())

# Check out a specific model
data.query('tekn_modell == "MG MARVEL R ELECTRIC"')