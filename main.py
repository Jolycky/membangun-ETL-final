from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql

def main():
    df_raw = scrape_main()
    df_clean = transform_data(df_raw)
    save_to_csv(df_clean)
    save_to_google_sheets(df_clean)
    save_to_postgresql(df_clean)

if __name__ == "__main__":
    main()