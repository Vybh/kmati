import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

path = r"C:\Users\vybha\OneDrive\Desktop\Internship_Project\combined_products_cleaned.csv"
df = pd.read_csv(path)

df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')
df['no_of_ratings'] = pd.to_numeric(df['no_of_ratings'], errors='coerce')

df['discount_price'] = (
    df['discount_price']
    .astype(str)
    .str.replace(r'[^\d.]', '', regex=True)
    .replace('', np.nan)
    .astype(float)
)

df['actual_price'] = (
    df['actual_price']
    .astype(str)
    .str.replace(r'[^\d.]', '', regex=True)
    .replace('', np.nan)
    .astype(float)
)

mask_both_missing = df['discount_price'].isna() & df['actual_price'].isna()

subcategory_discount_median = df.groupby('sub_category')['discount_price'].transform('median')
subcategory_actual_median = df.groupby('sub_category')['actual_price'].transform('median')

df.loc[mask_both_missing, 'discount_price'] = subcategory_discount_median[mask_both_missing]
df.loc[mask_both_missing, 'actual_price'] = subcategory_actual_median[mask_both_missing]

df.insert(0, 'product_id', range(1, len(df) + 1))

df.loc[df['discount_price'].isna() & df['actual_price'].notna(), 'discount_price'] = df['actual_price']

clean_path = r"C:\Users\vybha\OneDrive\Desktop\Internship_Project\combined_products_cleaned2.csv"
df.to_csv(clean_path, index=False)




