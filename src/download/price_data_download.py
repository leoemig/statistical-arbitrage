# Import necessary modules
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
from pathlib import Path
from src.utils.utils_os import check_directory, remove_files
from src.config.download import YEARS, FX, FILE, TICKERCOL, FXCOL

# Main Directories
BASE_DIR = Path(__file__).parent.parent.parent.resolve()
DOWNLOAD_DIR = BASE_DIR / "data" / "download"
RAW_DATA_DIR = DOWNLOAD_DIR / "raw_price_data"
FX_DIR = DOWNLOAD_DIR / "fx_rates"
TICKERS_FILE = DOWNLOAD_DIR / FILE

# Ensure directories exist
DIRS = [DOWNLOAD_DIR,
        RAW_DATA_DIR,
        FX_DIR]

for DIR in DIRS:
    check_directory(DIR)

# Define functions
def yf_download(stock, years):
    start_date = (datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=years*365))
    start_date_str = start_date.strftime("%Y-%m-%d")
    data_yf = yf.download(stock, start = start_date_str, auto_adjust = True, interval="1d", progress=False)["Close"]
    return data_yf
 
def main():
    # Remove all old files in raw_price_data
    remove_files(RAW_DATA_DIR)
    remove_files(FX_DIR)

    ticker_df = pd.read_excel(TICKERS_FILE)
    ticker = ticker_df[TICKERCOL].str.strip().dropna().tolist()
    faulty_tickers = []
    
    for t in ticker:
        # Files cannot be named CON under Windows
        if t == "CON":
            t = "CON_"

        try:
            data = yf_download(t, YEARS)
            if data is not None and len(data) > 0:
                data.to_parquet(RAW_DATA_DIR / f"{t}.parquet")
                print(f"Downloaded {t}")
            else:
                faulty_tickers.append(t)
        except Exception as e:
            print(f"Error downloading {t}: {e}")
            faulty_tickers.append(t)
    
    if faulty_tickers:
        faulty_tickers_df = pd.DataFrame({"Failed_Ticker": faulty_tickers})
        faulty_tickers_df.to_excel(DOWNLOAD_DIR / "faulty_tickers.xlsx", index=False)
        print(f"Faulty tickers saved: {len(faulty_tickers)} stocks")

if __name__ == "__main__":
    main()