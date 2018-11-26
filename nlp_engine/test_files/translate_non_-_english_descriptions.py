import pandas as pd ## Read and manipulate csv
from langdetect import detect ## Detect Language
from googletrans import Translator ## Translate Language

path = 'C:\\Users\\shrke\\Desktop\\272 Project\\Dataset\\'
data_full = pd.read_csv(path + "AppleStore.csv")
## Show top 5 rows in dataset
#data_full.head()

path = 'C:\\Users\\shrke\\Desktop\\272 Project\\Dataset\\'
data_desc = pd.read_csv(path + "appleStore_description.csv")

description_array = []
for i in range(len(data_full)):
    description_array.append(data_desc.iloc[i]['app_desc'])

## Check Non-English data    
#print (description_array[403])

## Detect all Non-English:
## Count and print all Non-Enlish Data with index
count = 0
for i in range(len(description_array)):
    if detect(description_array[i]) != 'en':
        ## print (detect(description_array[i]), i, count)
        index = description_array[i].index(' ')
        #store string till index(' ') is found
        first_sentence = description_array[i][:index]
        #print (first_sentence)
        count = count+1

## Translate        
## Google Translate Python API        
## Refer - https://py-googletrans.readthedocs.io/en/latest/    
#translator = Translator()        
#translator.translate('안녕하세요. ', dest='en', src='zh-cn')
