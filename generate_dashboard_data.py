"""
Bridge Script: Converts your Python analysis to JSON for the dashboard
Run this in global-natural-disasters/ directory
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

print("="*70)
print("GENERATING DASHBOARD DATA FROM YOUR ANALYSIS")
print("="*70)

# Load your actual data
print("\n📊 Loading eonet_cleaned.csv...")
df = pd.read_csv('eonet_cleaned.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

print(f"✅ Loaded {len(df):,} observations")

# ============================================================================
# 1. EXECUTIVE METRICS
# ============================================================================
print("\n📈 Calculating executive metrics...")

executive_metrics = {
    'total_observations': len(df),
    'unique_events': df['id'].nunique(),
    'date_range': {
        'start': df['datetime'].min().strftime('%Y-%m-%d'),
        'end': df['datetime'].max().strftime('%Y-%m-%d')
    },
    'years_tracked': df['year'].nunique(),
    'category_counts': df['category_title'].value_counts().to_dict()
}

print(f"  • Total observations: {executive_metrics['total_observations']:,}")
print(f"  • Unique events: {executive_metrics['unique_events']:,}")

# ============================================================================
# 2. GEOSPATIAL HOTSPOTS (DBSCAN-style clustering)
# ============================================================================
print("\n🗺️  Detecting geographic hotspots...")

# Create geographic bins (5-degree grid)
df['lat_bin'] = (df['latitude'] / 5).round() * 5
df['lon_bin'] = (df['longitude'] / 5).round() * 5

# Group by bins and count events
hotspots_df = df.groupby(['lat_bin', 'lon_bin']).agg({
    'id': 'count',
    'category_title': lambda x: x.mode()[0] if len(x) > 0 else 'Mixed'
}).reset_index()

hotspots_df.columns = ['latitude', 'longitude', 'count', 'primary_category']
hotspots_df = hotspots_df.nlargest(30, 'count')

# Add descriptive titles based on location
def get_region_name(lat, lon):
    if 10 <= lat <= 25 and -110 <= lon <= -85:
        return "Hurricane Activity Zone"
    elif 35 <= lat <= 45 and -125 <= lon <= -110:
        return "California Fire Zone"
    elif 5 <= lat <= 20 and 120 <= lon <= 135:
        return "Pacific Typhoon Belt"
    elif lat > 60:
        return "Arctic Region"
    elif lat < -60:
        return "Antarctic Region"
    elif -30 <= lat <= 0 and 110 <= lon <= 155:
        return "Australian Zone"
    elif -20 <= lat <= 10 and 165 <= lon <= -160:
        return "Pacific Ring of Fire"
    else:
        return f"Region {lat:.0f}°, {lon:.0f}°"

hotspots_df['title'] = hotspots_df.apply(
    lambda row: get_region_name(row['latitude'], row['longitude']), 
    axis=1
)

hotspots = hotspots_df.to_dict('records')
print(f"  • Found {len(hotspots)} major hotspots")
print(f"  • Top hotspot: {hotspots[0]['count']} events at ({hotspots[0]['latitude']}, {hotspots[0]['longitude']})")

# ============================================================================
# 3. SEASONAL PATTERNS
# ============================================================================
print("\n📅 Analyzing seasonal patterns...")

seasonal_data = []
for month in range(1, 13):
    month_df = df[df['month'] == month]
    
    seasonal_data.append({
        'month': month,
        'month_name': datetime(2000, month, 1).strftime('%b'),
        'total_events': len(month_df),
        'storms': len(month_df[month_df['category_simple'] == 'Storm']),
        'wildfires': len(month_df[month_df['category_simple'] == 'Wildfire']),
        'volcanoes': len(month_df[month_df['category_simple'] == 'Volcano']),
        'floods': len(month_df[month_df['category_simple'] == 'Flood']),
        'ice': len(month_df[month_df['category_simple'] == 'Ice'])
    })

print(f"  • Peak month: {max(seasonal_data, key=lambda x: x['total_events'])['month_name']} with {max(seasonal_data, key=lambda x: x['total_events'])['total_events']:,} events")

# ============================================================================
# 4. CATEGORY DISTRIBUTION
# ============================================================================
print("\n🥧 Calculating category distribution...")

category_distribution = []
total_obs = len(df)

for category, count in df['category_title'].value_counts().items():
    category_distribution.append({
        'name': category,
        'count': int(count),
        'percentage': round((count / total_obs) * 100, 1)
    })

# ============================================================================
# 5. YEARLY TRENDS
# ============================================================================
print("\n📈 Analyzing yearly trends...")

yearly_trends = []
for year in sorted(df['year'].unique())[-10:]:  # Last 10 years
    year_df = df[df['year'] == year]
    
    yearly_trends.append({
        'year': int(year),
        'total': len(year_df),
        'storms': len(year_df[year_df['category_simple'] == 'Storm']),
        'wildfires': len(year_df[year_df['category_simple'] == 'Wildfire']),
        'volcanoes': len(year_df[year_df['category_simple'] == 'Volcano'])
    })

# ============================================================================
# 6. RECENT EVENTS (Last 100)
# ============================================================================
print("\n🔴 Getting recent events...")

recent_events = df.nlargest(100, 'datetime')[[
    'id', 'title', 'category_title', 'latitude', 'longitude', 'date'
]].to_dict('records')

# ============================================================================
# 7. SAMPLE DATA FOR INTERACTIVE MAP (Performance optimized)
# ============================================================================
print("\n🌍 Sampling events for interactive map...")

sample_events = []
categories_to_sample = {
    'Storm': 500,
    'Wildfire': 300,
    'Volcano': 100,
    'Ice': 100,
    'Flood': 100
}

for category, sample_size in categories_to_sample.items():
    cat_df = df[df['category_simple'] == category]
    if len(cat_df) > sample_size:
        sampled = cat_df.sample(sample_size)
    else:
        sampled = cat_df
    
    for _, row in sampled.iterrows():
        sample_events.append({
            'lat': float(row['latitude']),
            'lon': float(row['longitude']),
            'category': row['category_title'],
            'title': row['title'],
            'date': row['date']
        })

print(f"  • Sampled {len(sample_events)} events for map")

# ============================================================================
# 8. REGIONAL STATISTICS
# ============================================================================
print("\n🌏 Calculating regional statistics...")

def get_region(lat, lon):
    if -180 <= lon < -30:
        return 'Americas'
    elif -30 <= lon < 60:
        return 'Europe/Africa'
    elif 60 <= lon < 150:
        return 'Asia/Pacific'
    else:
        return 'Other'

df['region'] = df.apply(lambda row: get_region(row['latitude'], row['longitude']), axis=1)

regional_stats = []
for region in df['region'].unique():
    region_df = df[df['region'] == region]
    regional_stats.append({
        'region': region,
        'total_events': len(region_df),
        'wildfires': len(region_df[region_df['category_simple'] == 'Wildfire']),
        'storms': len(region_df[region_df['category_simple'] == 'Storm'])
    })

# ============================================================================
# COMBINE ALL DATA
# ============================================================================
print("\n💾 Packaging all analysis results...")

dashboard_data = {
    'generated_at': datetime.now().isoformat(),
    'metadata': {
        'total_observations': executive_metrics['total_observations'],
        'unique_events': executive_metrics['unique_events'],
        'date_range': executive_metrics['date_range'],
        'years_tracked': executive_metrics['years_tracked']
    },
    'executive_metrics': executive_metrics,
    'hotspots': hotspots,
    'seasonal_patterns': seasonal_data,
    'category_distribution': category_distribution,
    'yearly_trends': yearly_trends,
    'recent_events': recent_events[:50],  # Limit to 50
    'sample_events': sample_events,
    'regional_stats': regional_stats
}

# ============================================================================
# SAVE TO VERCEL APP
# ============================================================================
print("\n💾 Saving to vercel_app/public/...")

import os
os.makedirs('vercel_app/public', exist_ok=True)

output_file = 'vercel_app/public/analysis_data.json'
with open(output_file, 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print(f"✅ Saved to: {output_file}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✨ DASHBOARD DATA GENERATED SUCCESSFULLY!")
print("="*70)
print(f"\n📊 Summary:")
print(f"  • Total observations: {executive_metrics['total_observations']:,}")
print(f"  • Hotspots detected: {len(hotspots)}")
print(f"  • Seasonal patterns: {len(seasonal_data)} months")
print(f"  • Yearly trends: {len(yearly_trends)} years")
print(f"  • Sample events: {len(sample_events)}")
print(f"\n📁 Output file: {output_file}")
print(f"  File size: {os.path.getsize(output_file) / 1024:.1f} KB")
print("\n🚀 Next steps:")
print("  1. cd vercel_app")
print("  2. npm run dev")
print("  3. Dashboard will load YOUR real analysis!")
print("\n" + "="*70)