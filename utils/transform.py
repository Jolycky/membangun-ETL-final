import pandas as pd

def transform_data(df):
    try:
        df = df.copy()

        df = df[~df['Title'].str.contains("Unknown Product", na=False)]

        # Clean Price
        df['Price'] = (
            df['Price']
            .fillna("0")
            .str.replace("Price Unavailable", "0", regex=False)
            .str.replace(r"[\$,]", "", regex=True)
            .astype(float) * 16000
        )

        # Clean Rating
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.?\d*)').astype(float)

        # Clean Colors
        df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(int)

        # Clean Size
        df['Size'] = df['Size'].str.replace("Size: ", "").str.strip()

        # Clean Gender
        df['Gender'] = df['Gender'].str.replace("Gender: ", "").str.strip()

        # Drop NaNs and duplicates
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        return df

    except Exception as e:
        print(f"Error during transformation: {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika gagal
