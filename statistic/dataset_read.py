import pandas as pd
from pymongo import MongoClient
import openpyxl

db_name = 'data-science-database'
collection_name= 'Tweets'
url=["mongodb://fotercim:212427123a1@ds121349.mlab.com:21349/data-science-database","mongodb://localhost:27017/data-science-database"]

def normalize(class_name):
    if(class_name.upper() == 'YAS'):
        return 1
    if(class_name.upper() == 'ILETISIM'):
        return 2
    if(class_name.upper() == 'TARIH'):
        return 3
    if(class_name.upper() == 'ID'):
        return 4
    if(class_name.upper() == 'ADDRESS'):
        return 5
    if(class_name.upper() == 'MESLEK'):
        return 6
    if(class_name.upper() == 'FIRMA'):
        return 7
    if(class_name.upper() == 'MEKAN'):
        return 8
    if(class_name.upper() == 'OLAY'):
        return 9
    if(class_name.upper() == 'ISIM'):
        return 10
    if(class_name.upper() == 'TRASH'):
        return 11



def read_mongo(flag=0):
    
    mongo_uri = url[flag]
    conn = MongoClient(mongo_uri)
    db = conn[db_name]
    collection = db[collection_name]
    cursor = collection.find({'done' : 1})
    df =  pd.DataFrame(list(cursor))
    return df.drop(['_id','done','tweetID'],axis=1)



df=read_mongo(0)
df1=read_mongo(1)
df=df.append(df1)

documents=df['tweet']
document_token_pure=df['wordsoftweets']

column_names= ['doc_id','token_id','token_text','c_id']
document_token = pd.DataFrame(columns=column_names)

for index_outher, row in document_token_pure.iteritems():
    for index_ineer, (key, value) in enumerate(row.items()):
        document_token=document_token.append({'doc_id': index_outher+1,
                               'token_id':index_ineer+1,
                               'token_text':key,
                               'c_id': normalize(str(value)),
                               },ignore_index=True)



writer = pd.ExcelWriter('document.xlsx')
documents.to_excel(writer)
writer.save()

writer = pd.ExcelWriter('document_token.xlsx')
document_token.to_excel(writer)
writer.save()