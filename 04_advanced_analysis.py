"""
NASA EONET Natural Events - Advanced Spatial Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import os
import warnings
warnings.filterwarnings('ignore')

def detect_hotspots(df):
    """Detect geographic hotspots"""
    print("Detecting hotspots...")
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    
    # Overall hotspots
    hexbin1 = axes[0].hexbin(df['longitude'], df['latitude'], 
                             gridsize=30, cmap='YlOrRd', mincnt=1)
    axes[0].set_xlabel('Longitude', fontsize=12)
    axes[0].set_ylabel('Latitude', fontsize=12)
    axes[0].set_title('Global Event Hotspots', fontsize=14, fontweight='bold')
    plt.colorbar(hexbin1, ax=axes[0], label='Event Count')
    axes[0].grid(True, alpha=0.3)
    
    # Wildfire hotspots
    wildfires = df[df['category_title'].str.contains('Wildfire', na=False)]
    if len(wildfires) > 0:
        hexbin2 = axes[1].hexbin(wildfires['longitude'], wildfires['latitude'],
                                 gridsize=30, cmap='Reds', mincnt=1)
        axes[1].set_xlabel('Longitude', fontsize=12)
        axes[1].set_ylabel('Latitude', fontsize=12)
        axes[1].set_title('Wildfire Hotspots', fontsize=14, fontweight='bold')
        plt.colorbar(hexbin2, ax=axes[1], label='Event Count')
        axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('advanced_analysis/hotspot_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: hotspot_analysis.png")

def spatial_clustering(df):
    """Perform DBSCAN clustering"""
    print("Performing spatial clustering...")
    
    # Prepare coordinates
    coords = df[['latitude', 'longitude']].values
    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(coords)
    
    # DBSCAN clustering
    db = DBSCAN(eps=0.5, min_samples=10).fit(coords_scaled)
    df['cluster'] = db.labels_
    
    n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
    n_noise = list(db.labels_).count(-1)
    
    print(f"  Found {n_clusters} clusters, {n_noise} noise points")
    
    # Visualize
    fig, ax = plt.subplots(figsize=(18, 10))
    
    unique_labels = set(db.labels_)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    
    for label, color in zip(unique_labels, colors):
        if label == -1:
            color = 'grey'
            marker = '.'
            size = 10
            alpha = 0.3
        else:
            marker = 'o'
            size = 50
            alpha = 0.7
        
        cluster_data = df[df['cluster'] == label]
        ax.scatter(cluster_data['longitude'], cluster_data['latitude'],
                  c=[color], marker=marker, s=size, alpha=alpha,
                  edgecolors='black', linewidths=0.5,
                  label=f'Cluster {label}' if label != -1 else 'Noise')
    
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.set_title(f'Spatial Clustering ({n_clusters} clusters)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Legend for first 10 clusters
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:11], labels[:11], loc='best', fontsize=8, ncol=2)
    
    plt.tight_layout()
    plt.savefig('advanced_analysis/spatial_clusters.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: spatial_clusters.png")

def temporal_spatial_patterns(df):
    """Analyze temporal-spatial patterns"""
    print("Analyzing temporal-spatial patterns...")
    
    # Create latitude bands
    df['lat_band'] = pd.cut(df['latitude'], 
                            bins=[-90, -60, -30, 0, 30, 60, 90],
                            labels=['Far South', 'South', 'Eq. South', 
                                   'Eq. North', 'North', 'Far North'])
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    # Events by latitude band over time
    pivot = pd.crosstab(df['year'], df['lat_band'])
    pivot.plot(ax=axes[0], marker='o')
    axes[0].set_title('Events by Latitude Band Over Time', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Number of Events')
    axes[0].legend(title='Latitude Band', bbox_to_anchor=(1.05, 1))
    axes[0].grid(True, alpha=0.3)
    
    # Heatmap: year vs month
    pivot2 = pd.crosstab(df['year'], df['month'])
    sns.heatmap(pivot2, cmap='YlOrRd', ax=axes[1], cbar_kws={'label': 'Events'})
    axes[1].set_title('Events by Year and Month', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Year')
    
    plt.tight_layout()
    plt.savefig('advanced_analysis/temporal_spatial_patterns.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: temporal_spatial_patterns.png")

def regional_analysis(df):
    """Analyze by region"""
    print("Performing regional analysis...")
    
    def assign_region(row):
        lat, lon = row['latitude'], row['longitude']
        if -170 < lon < -50:
            return 'Americas' if lat > 0 else 'South America'
        elif -20 < lon < 60:
            return 'Europe' if lat > 35 else 'Africa'
        elif 60 < lon < 150:
            return 'Asia' if lat > 0 else 'Oceania'
        return 'Other'
    
    df['region'] = df.apply(assign_region, axis=1)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Regional counts
    region_counts = df['region'].value_counts()
    axes[0].bar(range(len(region_counts)), region_counts.values, 
               color='steelblue', edgecolor='black')
    axes[0].set_xticks(range(len(region_counts)))
    axes[0].set_xticklabels(region_counts.index, rotation=45)
    axes[0].set_title('Events by Region', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Number of Events')
    
    # Regional trends
    for region in region_counts.head(5).index:
        region_data = df[df['region'] == region]
        yearly = region_data.groupby('year').size()
        axes[1].plot(yearly.index, yearly.values, marker='o', label=region, linewidth=2)
    
    axes[1].set_title('Regional Trends Over Time', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Number of Events')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('advanced_analysis/regional_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: regional_analysis.png")

def category_concentration(df):
    """Analyze category geographic concentration"""
    print("Analyzing category concentration...")
    
    top_cats = df['category_title'].value_counts().head(3).index
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    for idx, cat in enumerate(top_cats):
        cat_data = df[df['category_title'] == cat]
        axes[idx].scatter(cat_data['longitude'], cat_data['latitude'],
                         alpha=0.5, s=20, c='red', edgecolors='black', linewidths=0.5)
        axes[idx].set_xlabel('Longitude')
        axes[idx].set_ylabel('Latitude')
        axes[idx].set_title(f'{cat}\n({len(cat_data)} events)', fontweight='bold')
        axes[idx].grid(True, alpha=0.3)
        axes[idx].set_xlim(-180, 180)
        axes[idx].set_ylim(-90, 90)
    
    plt.tight_layout()
    plt.savefig('advanced_analysis/category_concentration.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: category_concentration.png")

if __name__ == "__main__":
    print("\nNASA EONET - ADVANCED ANALYSIS\n")
    print("="*70)
    
    try:
        # Load data
        df = pd.read_csv('eonet_cleaned.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        print(f"Loaded {len(df)} events\n")
        
        # Create output directory
        os.makedirs('advanced_analysis', exist_ok=True)
        
        # Run all analyses
        detect_hotspots(df)
        spatial_clustering(df)
        temporal_spatial_patterns(df)
        regional_analysis(df)
        category_concentration(df)
        
        print("\n" + "="*70)
        print("✓ SUCCESS! All analyses saved to: advanced_analysis/")
        print("="*70)
        print("\nGenerated files:")
        print("  • hotspot_analysis.png")
        print("  • spatial_clusters.png")
        print("  • temporal_spatial_patterns.png")
        print("  • regional_analysis.png")
        print("  • category_concentration.png")
        print("\n🎉 COMPLETE ANALYSIS FINISHED!")
        
    except FileNotFoundError:
        print("\nERROR: eonet_cleaned.csv not found!")
        print("Run 01_data_loading.py first.")
    except Exception as e:
        print(f"\nERROR: {e}")