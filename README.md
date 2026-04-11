# Latent_market_structure
Latent Structure of Stock Market Correlations using Linear Algebra


to run the code from a predefines csv file -

remove the the line 

    import kiteconnect as kc

replace the the code


    kite=initiation()
    df1=map_data()
    get_2_year_data(df1,kite)
    df2=merger_Via_Date()
    df2.to_csv("data/unprocessed_price_close.csv")

with 

    df2=pd.read_csv("unprocessed_price_close.csv")

and continue with it 

run the following commands

    python3 -m venv venv
    source venv/bin/activate
    pip install -r dev_requirements.txt
    

the graphs at the end - are sequential in nature - the next one only shows up after the prev is is closed

