import os
import json
import pandas
from seeding.seeder import seed_packages
 
def read_csv(inventory_name:str) -> dict:
    """Konverterar innehållet i en csv-fil till en dictionary"""
    if not os.path.exists("inventory/"+inventory_name):
        seed_packages()
    data = json.loads(pandas.read_csv("inventory/"+inventory_name).to_json())
    return data
