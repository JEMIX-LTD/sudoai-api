#%%
from pysondb import db
import pandas as pd
import os

def data_helper(database = db.getDb("db.json"),data_path='data'):
    ttd = []
    sa = []
    nsfw = []
    for data in database.getAll():
        ttd += list(zip(data['ttd'].split(),data['src'].split())) 
        sa.append((data['ttd'],data['sa'])) 
        nsfw += list(data['nsfw'].items())

    data_ttd = pd.DataFrame(ttd)
    data_sa = pd.DataFrame(sa)
    data_nsfw = pd.DataFrame(nsfw)

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    data_ttd.to_excel(f'{data_path}/ttd.xlsx',header=None,index=None)
    data_sa.to_excel(f'{data_path}/sa.xlsx',header=None,index=None)
    data_nsfw.to_excel(f'{data_path}/nsfw.xlsx',header=None,index=None)


if __name__ == '__main__':
    data_helper()
