import kiteconnect as kc
import pandas as pd
from src.connection import *
from src.data_pipeline import *


def main():
    print("running project")
    kite=initiation()
    df1=map_data()
    get_2_year_data(df1,kite)
    df2=merger_Via_Date()
    df2.to_csv("data/unprocessed_price_close.csv")


    


 



if __name__ == "__main__":
    main()