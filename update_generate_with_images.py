"""
Enhanced Bridge Script: Includes ALL your Python analysis outputs
Copies PNG images and creates JSON manifest
"""

import pandas as pd
import numpy as np
import json
import os
import shutil
from datetime import datetime

print("="*70)
print("GENERATING COMPLETE DASHBOARD DATA")
print("="*70)

# Load data
df = pd.read_csv('eonet_cleaned.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

# ============================================================================
# 1. COPY ALL YOUR ANALYSIS OUTPUTS TO DASHBOARD
# ============================================================================
print("\n📁 Copying your Python analysis outputs...")

# Create image directory in dashboard
os.makedirs('vercel_app/public/analysis_images', exist_ok=True)

# Define what to copy
image_sources = {
    'advanced_analysis': [
        'hotspot_analysis.png',
        'spatial_clusters.png',
        'temporal_spatial_patterns.png',
        'regional_analysis.png',
        'category_concentration.png'
    ],
    'analysis_outputs': [
        'temporal_analysis.png',
        'category_analysis.png',
        'geographic_distribution.png'
    ],
    'policy_visualizations': [
        'executive_dashboard.html',
        'risk_hotspot_map.html',
        '3d_globe_intelligence.html'
    ],
    'ultimate_geospatial': [
        '3d_visualizations/*',
        'dashboards/*',
        'story_maps/*'
    ]
}

copied_files = []

for source_dir, files in image_sources.items():
    if os.path.exists(source_dir):
        print(f"  Copying from {source_dir}/...")
        for file_pattern in files:
            if '*' in file_pattern:
                # Handle wildcards
                import glob
                pattern = os.path.join(source_dir, file_pattern)
                for file_path in glob.glob(pattern):
                    dest = os.path.join('vercel_app/public/analysis_images', os.path.basename(file_path))
                    shutil.copy2(file_path, dest)
                    copied_files.append(os.path.basename(file_path))
            else:
                source = os.path.join(source_dir, file_pattern)
                if os.path.exists(source):
                    dest = os.path.join('vercel_app/public/analysis_images', file_pattern)
                    shutil.copy2(source, dest)
                    copied_files.append(file_pattern)
                    print(f"    ✓ {file_pattern}")

print(f"  Total files copied: {len(copied_files)}")

# ============================================================================
# 2. GENERATE JSON DATA (same as before)
# ============================================================================
print("\n📊 Generating statistical data...")

# Hotspots
df['lat_bin'] = (df['latitude'] / 5).round() * 5
df['lon_bin'] = (df['longitude'] / 5).round() * 5

hotspots_df = df.groupby(['lat_bin', 'lon_bin']).agg({
    'id': 'count',
    'category_title': lambda x: x.mode()[0] if len(x) > 0 else 'Mixed'
}).reset_index()
hotspots_df.columns = ['latitude', 'longitude', 'count', 'primary_category']
hotspots_df = hotspots_df.nlargest(30, 'count')

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
    else:
        return f"Region {lat:.0f}°, {lon:.0f}°"

hotspots_df['title'] = hotspots_df.apply(
    lambda row: get_region_name(row['latitude'], row['longitude']), axis=1
)

# Seasonal data
seasonal_data = []
for month in range(1, 13):
    month_df = df[df['month'] == month]
    seasonal_data.append({
        'month': month,
        'month_name': datetime(2000, month, 1).strftime('%b'),
        'total_events': len(month_df),
        'storms': len(month_df[month_df['category_simple'] == 'Storm']),
        'wildfires': len(month_df[month_df['category_simple'] == 'Wildfire']),
    })

# Category distribution
category_distribution = []
total_obs = len(df)
for category, count in df['category_title'].value_counts().items():
    category_distribution.append({
        'name': category,
        'count': int(count),
        'percentage': round((count / total_obs) * 100, 1)
    })

# Yearly trends (last 10 years)
yearly_trends = []
for year in sorted(df['year'].unique())[-10:]:
    year_df = df[df['year'] == year]
    yearly_trends.append({
        'year': int(year),
        'total': len(year_df),
        'storms': len(year_df[year_df['category_simple'] == 'Storm']),
        'wildfires': len(year_df[year_df['category_simple'] == 'Wildfire']),
    })

# ============================================================================
# 3. CREATE MANIFEST OF AVAILABLE VISUALIZATIONS
# ============================================================================
print("\n📋 Creating visualization manifest...")

available_visualizations = {
    'static_images': {},
    'interactive_maps': {},
    'html_dashboards': {}
}

# Scan for what's available
for filename in copied_files:
    if filename.endswith('.png'):
        category = 'advanced_analysis' if any(x in filename for x in ['hotspot', 'cluster', 'temporal_spatial', 'regional', 'concentration']) else 'basic_analysis'
        available_visualizations['static_images'][filename] = {
            'path': f'/analysis_images/{filename}',
            'category': category,
            'title': filename.replace('_', ' ').replace('.png', '').title()
        }
    elif filename.endswith('.html'):
        available_visualizations['interactive_maps'][filename] = {
            'path': f'/analysis_images/{filename}',
            'title': filename.replace('_', ' ').replace('.html', '').title()
        }

# ============================================================================
# 4. PACKAGE EVERYTHING
# ============================================================================
dashboard_data = {
    'generated_at': datetime.now().isoformat(),
    'metadata': {
        'total_observations': len(df),
        'unique_events': df['id'].nunique(),
        'date_range': {
            'start': df['datetime'].min().strftime('%Y-%m-%d'),
            'end': df['datetime'].max().strftime('%Y-%m-%d')
        },
        'years_tracked': df['year'].nunique()
    },
    'executive_metrics': {
        'total_observations': len(df),
        'unique_events': df['id'].nunique(),
        'category_counts': df['category_title'].value_counts().to_dict()
    },
    'hotspots': hotspots_df.to_dict('records'),
    'seasonal_patterns': seasonal_data,
    'category_distribution': category_distribution,
    'yearly_trends': yearly_trends,
    'available_visualizations': available_visualizations
}

# Save
output_file = 'vercel_app/public/analysis_data.json'
with open(output_file, 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print(f"✅ Saved to: {output_file}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✨ COMPLETE DASHBOARD DATA GENERATED!")
print("="*70)
print(f"\n📊 Statistics:")
print(f"  • Total observations: {len(df):,}")
print(f"  • Hotspots detected: {len(hotspots_df)}")
print(f"  • Images copied: {len([f for f in copied_files if f.endswith('.png')])}")
print(f"  • HTML maps copied: {len([f for f in copied_files if f.endswith('.html')])}")
print(f"\n📁 Files:")
print(f"  • {output_file}")
print(f"  • vercel_app/public/analysis_images/ ({len(copied_files)} files)")
print("\n🚀 Next: cd vercel_app && npm run dev")
print("="*70)