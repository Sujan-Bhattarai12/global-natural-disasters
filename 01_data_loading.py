"""
NASA EONET Natural Events Analysis - Data Loading and Cleaning
Perfect match for CSV: ID,Title,Description,Category_title,Date,Time,Year,Longitude,Latitude
"""

import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data(filepath):
    """Load and clean the EONET dataset"""
    print("="*70)
    print("LOADING NASA EONET DATA")
    print("="*70)
    
    # Load data
    df = pd.read_csv(filepath)
    
    print(f"\n✓ Loaded {len(df)} events")
    print(f"\nColumns: {', '.join(df.columns.tolist())}")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower()
    
    # Create datetime from Date and Time
    print("\nCreating datetime features...")
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'].fillna('00:00:00'))
    
    # Extract temporal features
    df['month'] = df['datetime'].dt.month
    df['month_name'] = df['datetime'].dt.month_name()
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['quarter'] = df['datetime'].dt.quarter
    
    # Handle descriptions
    df['description'] = df['description'].fillna('No description')
    
    # Simplified categories
    def simplify_category(cat):
        if pd.isna(cat):
            return 'Other'
        cat = str(cat).lower()
        if 'wildfire' in cat:
            return 'Wildfire'
        elif 'storm' in cat:
            return 'Storm'
        elif 'flood' in cat:
            return 'Flood'
        elif 'volcano' in cat:
            return 'Volcano'
        elif 'ice' in cat:
            return 'Ice'
        return 'Other'
    
    df['category_simple'] = df['category_title'].apply(simplify_category)
    
    print("✓ Features created")
    print(f"\nDate range: {df['datetime'].min()} to {df['datetime'].max()}")
    print(f"Total events: {len(df):,}")
    print(f"\nTop categories:")
    for cat, count in df['category_title'].value_counts().head(3).items():
        print(f"  • {cat}: {count:,}")
    
    return df

if __name__ == "__main__":
    print("\nNASA EONET - DATA LOADING\n")
    
    try:
        df = load_and_clean_data('eonet_data.csv')
        df.to_csv('eonet_cleaned.csv', index=False)
        
        print("\n" + "="*70)
        print("✓ SUCCESS! Cleaned data saved to: eonet_cleaned.csv")
        print("="*70)
        print("\nSample data:")
        print(df[['title', 'category_title', 'latitude', 'longitude', 'date']].head())
        print("\nNext: Run python 02_exploratory_analysis.py")
        
    except FileNotFoundError:
        print("\nERROR: eonet_data.csv not found!")
        print("Make sure the CSV file is in the current directory.")
    except Exception as e:
        print(f"\nERROR: {e}")