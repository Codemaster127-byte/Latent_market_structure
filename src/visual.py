import numpy as np
import matplotlib.pyplot as plt

# --- STOCK ORDER (MUST MATCH YOUR MATRIX EXACTLY) ---
stocks = [
    "RELIANCE","HDFCBANK","ICICIBANK","SBIN","AXISBANK","KOTAKBANK","BANKBARODA","PNB","CANBK",
    "INFY","TCS","WIPRO","HCLTECH","TECHM",
    "ITC","HINDUNILVR","NESTLEIND","BRITANNIA","DABUR","MARICO","GODREJCP","COLPAL",
    "MARUTI","TMCV","M&M","HEROMOTOCO","BAJAJ-AUTO","TVSMOTOR",
    "LT","SIEMENS","ABB","BHEL",
    "ONGC","NTPC","POWERGRID","GAIL","BPCL","HINDPETRO",
    "TATASTEEL","JSWSTEEL","HINDALCO","SAIL",
    "ULTRACEMCO","GRASIM","SHREECEM","ACC","AMBUJACEM",
    "SUNPHARMA","DRREDDY","CIPLA","LUPIN"
]

# --- SECTOR MAP ---
sector_map = {
    "RELIANCE": "Energy",

    "HDFCBANK": "Banking","ICICIBANK": "Banking","SBIN": "Banking",
    "AXISBANK": "Banking","KOTAKBANK": "Banking","BANKBARODA": "Banking",
    "PNB": "Banking","CANBK": "Banking",

    "INFY": "IT","TCS": "IT","WIPRO": "IT","HCLTECH": "IT","TECHM": "IT",

    "ITC": "FMCG","HINDUNILVR": "FMCG","NESTLEIND": "FMCG",
    "BRITANNIA": "FMCG","DABUR": "FMCG","MARICO": "FMCG",
    "GODREJCP": "FMCG","COLPAL": "FMCG",

    "MARUTI": "Auto","TMCV": "Auto","M&M": "Auto",
    "HEROMOTOCO": "Auto","BAJAJ-AUTO": "Auto","TVSMOTOR": "Auto",

    "LT": "Industrial","SIEMENS": "Industrial","ABB": "Industrial","BHEL": "Industrial",

    "ONGC": "Energy","NTPC": "Energy","POWERGRID": "Energy",
    "GAIL": "Energy","BPCL": "Energy","HINDPETRO": "Energy",

    "TATASTEEL": "Metals","JSWSTEEL": "Metals","HINDALCO": "Metals","SAIL": "Metals",

    "ULTRACEMCO": "Cement","GRASIM": "Cement","SHREECEM": "Cement",
    "ACC": "Cement","AMBUJACEM": "Cement",

    "SUNPHARMA": "Pharma","DRREDDY": "Pharma","CIPLA": "Pharma","LUPIN": "Pharma"
}


# --- CORE: SIGNED SECTOR CONTRIBUTION ---
def _sector_contribution_signed(eigvec):
    sector_weights = {}
    sector_counts = {}

    for i, stock in enumerate(stocks):
        sector = sector_map[stock]

        sector_weights[sector] = sector_weights.get(sector, 0) + eigvec[i]
        sector_counts[sector] = sector_counts.get(sector, 0) + 1

    # average (prevents sector size bias)
    for s in sector_weights:
        sector_weights[s] /= sector_counts[s]

    return sector_weights


# --- MAIN FUNCTION ---
def visualize_eigenvectors(eigvecs, top_k=7):
    """
    eigvecs: numpy array (n_stocks x n_components)
    """

    for i in range(top_k):
        eigvec = eigvecs[:, i]   # IMPORTANT: column = eigenvector

        sector_weights = _sector_contribution_signed(eigvec)

        sectors = list(sector_weights.keys())
        values = list(sector_weights.values())

        plt.figure()
        plt.bar(sectors, values)

        plt.axhline(0)  # zero line → shows + vs -

        plt.xticks(rotation=45)
        plt.title(f"Eigenvector {i+1} - Sector Direction Split")
        plt.ylabel("Signed Contribution")

        plt.tight_layout()
        plt.show()