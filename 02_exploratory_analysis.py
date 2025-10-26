"""
NASA EONET Natural Events - Exploratory Data Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

def create_temporal_analysis(df):
    """Create temporal visualizations"""
    print("Creating temporal analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Events over time (monthly)
    monthly = df.groupby(df['datetime'].dt.to_period('M')).size()
    axes[0, 0].plot(monthly.index.astype(str), monthly.values, color='steelblue', linewidth=2)
    axes[0, 0].set_title('Events Over Time (Monthly)', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Number of Events')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Events by year
    yearly = df['year'].value_counts().sort_index()
    axes[0, 1].bar(yearly.index, yearly.values, color='coral', edgecolor='black')
    axes[0, 1].set_title('Events by Year', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Year')
    axes[0, 1].set_ylabel('Number of Events')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Events by month
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_counts = df['month_name'].value_counts().reindex(month_order)
    axes[1, 0].bar(range(12), monthly_counts.values, color='seagreen', edgecolor='black')
    axes[1, 0].set_xticks(range(12))
    axes[1, 0].set_xticklabels([m[:3] for m in month_order], rotation=45)
    axes[1, 0].set_title('Events by Month (All Years)', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Number of Events')
    
    # Events by day of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = df['day_of_week'].value_counts().reindex(day_order)
    axes[1, 1].bar(range(7), day_counts.values, color='mediumpurple', edgecolor='black')
    axes[1, 1].set_xticks(range(7))
    axes[1, 1].set_xticklabels([d[:3] for d in day_order], rotation=45)
    axes[1, 1].set_title('Events by Day of Week', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('Number of Events')
    
    plt.tight_layout()
    plt.savefig('analysis_outputs/temporal_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: temporal_analysis.png")

def create_category_analysis(df):
    """Create category visualizations"""
    print("Creating category analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Category distribution
    cat_counts = df['category_title'].value_counts().head(10)
    axes[0].barh(range(len(cat_counts)), cat_counts.values, color='teal', edgecolor='black')
    axes[0].set_yticks(range(len(cat_counts)))
    axes[0].set_yticklabels(cat_counts.index, fontsize=10)
    axes[0].set_title('Top 10 Event Categories', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Number of Events')
    axes[0].invert_yaxis()
    
    # Category trends over time
    top_cats = df['category_title'].value_counts().head(5).index
    for cat in top_cats:
        cat_data = df[df['category_title'] == cat]
        yearly = cat_data.groupby('year').size()
        axes[1].plot(yearly.index, yearly.values, marker='o', label=cat, linewidth=2)
    
    axes[1].set_title('Top 5 Categories Over Time', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Number of Events')
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('analysis_outputs/category_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: category_analysis.png")

def create_geographic_analysis(df):
    """Create geographic visualizations"""
    print("Creating geographic analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Latitude distribution
    axes[0].hist(df['latitude'], bins=50, color='skyblue', edgecolor='black')
    axes[0].axvline(df['latitude'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
    axes[0].set_title('Latitude Distribution', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Latitude')
    axes[0].set_ylabel('Frequency')
    axes[0].legend()
    
    # Longitude distribution
    axes[1].hist(df['longitude'], bins=50, color='lightcoral', edgecolor='black')
    axes[1].axvline(df['longitude'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
    axes[1].set_title('Longitude Distribution', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Longitude')
    axes[1].set_ylabel('Frequency')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('analysis_outputs/geographic_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: geographic_distribution.png")

if __name__ == "__main__":
    print("\nNASA EONET - EXPLORATORY ANALYSIS\n")
    print("="*70)
    
    try:
        # Load cleaned data
        df = pd.read_csv('eonet_cleaned.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        print(f"Loaded {len(df)} events\n")
        
        # Create output directory
        os.makedirs('analysis_outputs', exist_ok=True)
        
        # Create all visualizations
        create_temporal_analysis(df)
        create_category_analysis(df)
        create_geographic_analysis(df)
        
        # Print statistics
        print("\n" + "="*70)
        print("STATISTICS")
        print("="*70)
        print(f"Total events: {len(df):,}")
        print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")
        print(f"Categories: {df['category_title'].nunique()}")
        print(f"Geographic span:")
        print(f"  Latitude: {df['latitude'].min():.1f}° to {df['latitude'].max():.1f}°")
        print(f"  Longitude: {df['longitude'].min():.1f}° to {df['longitude'].max():.1f}°")
        
        print("\n" + "="*70)
        print("✓ SUCCESS! All visualizations saved to: analysis_outputs/")
        print("="*70)
        print("\nNext: Run python 03_geospatial_visualization.py")
        
    except FileNotFoundError:
        print("\nERROR: eonet_cleaned.csv not found!")
        print("Run 01_data_loading.py first.")
    except Exception as e:
        print(f"\nERROR: {e}")