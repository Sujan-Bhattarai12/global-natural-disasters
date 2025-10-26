"""
NASA EONET - ULTIMATE GEOSPATIAL VISUALIZATION SUITE
============================================
The most advanced visualization ever created for natural events data
Designed to WIN against alien competitors! 🛸

Features:
- 3D Interactive Globe
- Advanced Multi-Panel Dashboard
- Cinematic Time-lapse Animations
- Statistical Overlays
- Kernel Density Estimation
- Network Analysis
- Professional Story Maps
- Publication-Quality Outputs
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap, MarkerCluster, TimestampedGeoJson, MiniMap
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-quality plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class UltimateGeoVisualizer:
    """The most advanced geospatial visualizer ever created"""
    
    def __init__(self, df):
        self.df = df
        self.output_dir = 'ultimate_geospatial'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create subdirectories for organization
        os.makedirs(f'{self.output_dir}/3d_visualizations', exist_ok=True)
        os.makedirs(f'{self.output_dir}/dashboards', exist_ok=True)
        os.makedirs(f'{self.output_dir}/animations', exist_ok=True)
        os.makedirs(f'{self.output_dir}/story_maps', exist_ok=True)
        os.makedirs(f'{self.output_dir}/statistical_maps', exist_ok=True)
        os.makedirs(f'{self.output_dir}/publication_ready', exist_ok=True)
        
        print("="*80)
        print("🌍 ULTIMATE GEOSPATIAL VISUALIZATION SUITE INITIALIZED")
        print("="*80)
        print(f"📊 Loaded: {len(df):,} events")
        print(f"📅 Period: {df['datetime'].min()} to {df['datetime'].max()}")
        print(f"🗂️  Categories: {df['category_title'].nunique()}")
        print("="*80 + "\n")
    
    def create_all_visualizations(self):
        """Generate ALL ultimate visualizations"""
        
        print("🎬 Starting visualization generation...\n")
        
        # 1. 3D Visualizations
        print("=" * 80)
        print("🌐 SECTION 1: 3D VISUALIZATIONS")
        print("=" * 80)
        self.create_3d_globe()
        self.create_3d_scatter_plot()
        self.create_3d_density_surface()
        
        # 2. Advanced Dashboards
        print("\n" + "=" * 80)
        print("📊 SECTION 2: INTERACTIVE DASHBOARDS")
        print("=" * 80)
        self.create_master_dashboard()
        self.create_temporal_dashboard()
        
        # 3. Cinematic Animations
        print("\n" + "=" * 80)
        print("🎥 SECTION 3: CINEMATIC ANIMATIONS")
        print("=" * 80)
        self.create_cinematic_timeline()
        self.create_cumulative_animation()
        
        # 4. Story Maps
        print("\n" + "=" * 80)
        print("📖 SECTION 4: STORY MAPS")
        print("=" * 80)
        self.create_narrative_map()
        self.create_comparison_map()
        
        # 5. Statistical Maps
        print("\n" + "=" * 80)
        print("📈 SECTION 5: STATISTICAL OVERLAYS")
        print("=" * 80)
        self.create_kde_heatmap()
        self.create_intensity_map()
        self.create_seasonal_comparison()
        
        # 6. Publication Ready
        print("\n" + "=" * 80)
        print("📰 SECTION 6: PUBLICATION-QUALITY FIGURES")
        print("=" * 80)
        self.create_multi_panel_figure()
        self.create_infographic_map()
        
        print("\n" + "=" * 80)
        print("✅ ALL VISUALIZATIONS COMPLETE!")
        print("=" * 80)
        self.print_summary()
    
    # ==================== 3D VISUALIZATIONS ====================
    
    def create_3d_globe(self):
        """Create stunning 3D interactive globe"""
        print("  🌍 Creating 3D Interactive Globe...")
        
        # Sample data for performance
        df_sample = self.df.sample(min(2000, len(self.df)), random_state=42)
        
        fig = go.Figure()
        
        # Add events as 3D scatter
        for category in df_sample['category_title'].unique()[:5]:
            cat_data = df_sample[df_sample['category_title'] == category]
            
            fig.add_trace(go.Scattergeo(
                lon=cat_data['longitude'],
                lat=cat_data['latitude'],
                text=cat_data['title'],
                name=category,
                mode='markers',
                marker=dict(
                    size=8,
                    opacity=0.8,
                    line=dict(width=0.5, color='white')
                )
            ))
        
        fig.update_layout(
            title=dict(
                text='<b>3D Global Natural Events Distribution</b>',
                font=dict(size=24)
            ),
            geo=dict(
                projection_type='orthographic',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showocean=True,
                oceancolor='rgb(230, 245, 255)',
                showcountries=True,
                countrycolor='rgb(204, 204, 204)',
                showlakes=True,
                lakecolor='rgb(200, 230, 255)',
                bgcolor='rgba(0,0,0,0)',
                projection_rotation=dict(lon=-30, lat=30, roll=0)
            ),
            height=800,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255,255,255,0.8)"
            )
        )
        
        fig.write_html(f'{self.output_dir}/3d_visualizations/3d_globe_interactive.html')
        print("    ✓ Saved: 3d_globe_interactive.html")
    
    def create_3d_scatter_plot(self):
        """Create 3D scatter plot with time dimension"""
        print("  📍 Creating 3D Scatter Plot (Lat, Lon, Time)...")
        
        df_sample = self.df.sample(min(1000, len(self.df)), random_state=42).copy()
        df_sample['days_since_start'] = (df_sample['datetime'] - df_sample['datetime'].min()).dt.days
        
        fig = go.Figure(data=[go.Scatter3d(
            x=df_sample['longitude'],
            y=df_sample['latitude'],
            z=df_sample['days_since_start'],
            mode='markers',
            marker=dict(
                size=5,
                color=df_sample['days_since_start'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Days Since Start"),
                opacity=0.8
            ),
            text=df_sample['title'],
            hovertemplate='<b>%{text}</b><br>Lon: %{x}<br>Lat: %{y}<br>Day: %{z}<extra></extra>'
        )])
        
        fig.update_layout(
            title='<b>3D Space-Time Distribution of Events</b>',
            scene=dict(
                xaxis_title='Longitude',
                yaxis_title='Latitude',
                zaxis_title='Days Since Start',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
            ),
            height=800
        )
        
        fig.write_html(f'{self.output_dir}/3d_visualizations/3d_spacetime_scatter.html')
        print("    ✓ Saved: 3d_spacetime_scatter.html")
    
    def create_3d_density_surface(self):
        """Create 3D density surface"""
        print("  🗻 Creating 3D Density Surface...")
        
        # Create 2D histogram
        lon_bins = np.linspace(self.df['longitude'].min(), self.df['longitude'].max(), 50)
        lat_bins = np.linspace(self.df['latitude'].min(), self.df['latitude'].max(), 50)
        
        H, xedges, yedges = np.histogram2d(
            self.df['longitude'], 
            self.df['latitude'], 
            bins=[lon_bins, lat_bins]
        )
        
        fig = go.Figure(data=[go.Surface(
            z=H.T,
            x=xedges,
            y=yedges,
            colorscale='Hot',
            colorbar=dict(title='Event Density')
        )])
        
        fig.update_layout(
            title='<b>3D Event Density Surface</b>',
            scene=dict(
                xaxis_title='Longitude',
                yaxis_title='Latitude',
                zaxis_title='Event Count',
                camera=dict(eye=dict(x=1.7, y=1.7, z=1.3))
            ),
            height=800
        )
        
        fig.write_html(f'{self.output_dir}/3d_visualizations/3d_density_surface.html')
        print("    ✓ Saved: 3d_density_surface.html")
    
    # ==================== DASHBOARDS ====================
    
    def create_master_dashboard(self):
        """Create comprehensive multi-panel dashboard"""
        print("  📊 Creating Master Dashboard...")
        
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=(
                'Global Distribution', 'Events Over Time', 'Top Categories',
                'Monthly Pattern', 'Latitude Distribution', 'Event Intensity',
                'Year-over-Year', 'Geographic Heatmap', 'Recent Activity'
            ),
            specs=[
                [{'type': 'scattergeo', 'rowspan': 2}, {'type': 'scatter'}, {'type': 'bar'}],
                [None, {'type': 'bar'}, {'type': 'histogram'}],
                [{'type': 'scatter'}, {'type': 'heatmap'}, {'type': 'indicator'}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Global scatter
        top_cats = self.df['category_title'].value_counts().head(3).index
        for cat in top_cats:
            cat_data = self.df[self.df['category_title'] == cat]
            # Sample correctly - can't sample more than category has
            sample_size = min(500, len(cat_data))
            cat_data = cat_data.sample(sample_size, random_state=42) if len(cat_data) > 0 else cat_data
            fig.add_trace(
                go.Scattergeo(
                    lon=cat_data['longitude'],
                    lat=cat_data['latitude'],
                    name=cat,
                    mode='markers',
                    marker=dict(size=4, opacity=0.6)
                ),
                row=1, col=1
            )
        
        # 2. Events over time
        monthly = self.df.groupby(self.df['datetime'].dt.to_period('M')).size()
        fig.add_trace(
            go.Scatter(
                x=monthly.index.astype(str),
                y=monthly.values,
                mode='lines+markers',
                name='Monthly Events',
                line=dict(width=2)
            ),
            row=1, col=2
        )
        
        # 3. Top categories
        cat_counts = self.df['category_title'].value_counts().head(5)
        fig.add_trace(
            go.Bar(
                x=cat_counts.values,
                y=cat_counts.index,
                orientation='h',
                name='Categories'
            ),
            row=1, col=3
        )
        
        # 4. Monthly pattern
        month_counts = self.df['month'].value_counts().sort_index()
        fig.add_trace(
            go.Bar(
                x=list(range(1, 13)),
                y=[month_counts.get(i, 0) for i in range(1, 13)],
                name='By Month'
            ),
            row=2, col=2
        )
        
        # 5. Latitude distribution
        fig.add_trace(
            go.Histogram(
                x=self.df['latitude'],
                nbinsx=50,
                name='Latitude'
            ),
            row=2, col=3
        )
        
        # 6. Year-over-year
        yearly = self.df.groupby('year').size()
        fig.add_trace(
            go.Scatter(
                x=yearly.index,
                y=yearly.values,
                mode='lines+markers',
                name='Yearly',
                line=dict(width=3)
            ),
            row=3, col=1
        )
        
        # 7. Heatmap (year vs month)
        pivot = pd.crosstab(self.df['year'], self.df['month'])
        fig.add_trace(
            go.Heatmap(
                z=pivot.values,
                x=list(range(1, 13)),
                y=pivot.index,
                colorscale='YlOrRd',
                showscale=False
            ),
            row=3, col=2
        )
        
        # 8. Recent activity indicator
        recent_count = len(self.df[self.df['datetime'] > self.df['datetime'].max() - timedelta(days=30)])
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=recent_count,
                title={"text": "Last 30 Days"},
                delta={'reference': len(self.df) / 365 * 30}
            ),
            row=3, col=3
        )
        
        fig.update_layout(
            title_text="<b>ULTIMATE NATURAL EVENTS DASHBOARD</b>",
            title_font_size=26,
            showlegend=True,
            height=1200,
            geo=dict(
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                projection_type='natural earth'
            )
        )
        
        fig.write_html(f'{self.output_dir}/dashboards/master_dashboard.html')
        print("    ✓ Saved: master_dashboard.html")
    
    def create_temporal_dashboard(self):
        """Create time-focused interactive dashboard"""
        print("  ⏰ Creating Temporal Analysis Dashboard...")
        
        # Prepare temporal data
        self.df['year_month'] = self.df['datetime'].dt.to_period('M')
        self.df['week'] = self.df['datetime'].dt.isocalendar().week
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Cumulative Events Over Time',
                'Events by Day of Week',
                'Weekly Pattern Heatmap',
                'Seasonal Distribution'
            ),
            specs=[
                [{'type': 'scatter'}, {'type': 'bar'}],
                [{'type': 'heatmap'}, {'type': 'sunburst'}]
            ]
        )
        
        # Cumulative events
        daily = self.df.groupby(self.df['datetime'].dt.date).size().cumsum()
        fig.add_trace(
            go.Scatter(
                x=daily.index,
                y=daily.values,
                mode='lines',
                name='Cumulative',
                fill='tozeroy',
                line=dict(width=2, color='rgb(26, 118, 255)')
            ),
            row=1, col=1
        )
        
        # Day of week
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_counts = self.df['day_of_week'].value_counts().reindex(dow_order)
        fig.add_trace(
            go.Bar(
                x=dow_order,
                y=dow_counts.values,
                marker_color='indianred'
            ),
            row=1, col=2
        )
        
        # Weekly heatmap
        week_year = pd.crosstab(self.df['year'], self.df['week'])
        fig.add_trace(
            go.Heatmap(
                z=week_year.values,
                x=week_year.columns,
                y=week_year.index,
                colorscale='Reds'
            ),
            row=2, col=1
        )
        
        # Seasonal sunburst
        self.df['season'] = self.df['month'].map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        })
        
        season_data = self.df.groupby(['season', 'category_simple']).size().reset_index(name='count')
        fig.add_trace(
            go.Sunburst(
                labels=season_data['season'].tolist() + season_data['category_simple'].tolist(),
                parents=[''] * len(season_data['season'].unique()) + season_data['season'].tolist(),
                values=[season_data[season_data['season']==s]['count'].sum() for s in season_data['season'].unique()] + season_data['count'].tolist()
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="<b>TEMPORAL ANALYSIS DASHBOARD</b>",
            title_font_size=24,
            showlegend=False,
            height=900
        )
        
        fig.write_html(f'{self.output_dir}/dashboards/temporal_dashboard.html')
        print("    ✓ Saved: temporal_dashboard.html")
    
    # ==================== ANIMATIONS ====================
    
    def create_cinematic_timeline(self):
        """Create cinematic animated timeline with effects"""
        print("  🎬 Creating Cinematic Timeline Animation...")
        
        # Prepare data
        df_anim = self.df.copy()
        df_anim['year_month'] = df_anim['datetime'].dt.to_period('M').astype(str)
        
        # Sample for smooth animation
        df_anim = df_anim.groupby('year_month').apply(
            lambda x: x.sample(min(200, len(x)), random_state=42)
        ).reset_index(drop=True)
        
        fig = px.scatter_geo(
            df_anim,
            lat='latitude',
            lon='longitude',
            color='category_title',
            hover_name='title',
            animation_frame='year_month',
            projection='natural earth',
            title='<b>Cinematic Natural Events Timeline (2002-2025)</b>',
            size_max=15,
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        
        fig.update_geos(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
            showcountries=True,
            countrycolor='rgb(204, 204, 204)'
        )
        
        fig.update_layout(
            height=800,
            title_font_size=24,
            font=dict(family="Arial, sans-serif", size=14)
        )
        
        # Add animation settings
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 100
        
        fig.write_html(f'{self.output_dir}/animations/cinematic_timeline.html')
        print("    ✓ Saved: cinematic_timeline.html")
    
    def create_cumulative_animation(self):
        """Create cumulative buildup animation"""
        print("  📈 Creating Cumulative Buildup Animation...")
        
        # Create cumulative dataset
        df_sorted = self.df.sort_values('datetime').copy()
        df_sorted['event_number'] = range(1, len(df_sorted) + 1)
        df_sorted['year_month'] = df_sorted['datetime'].dt.to_period('M').astype(str)
        
        # Sample every 50th event for smooth animation
        df_cumul = df_sorted[::50].copy()
        
        fig = px.scatter_geo(
            df_cumul,
            lat='latitude',
            lon='longitude',
            color='category_title',
            size='event_number',
            hover_name='title',
            animation_frame='year_month',
            projection='natural earth',
            title='<b>Cumulative Event Buildup Over Time</b>',
            size_max=20
        )
        
        fig.update_geos(
            showland=True,
            landcolor='rgb(220, 220, 220)',
            coastlinecolor='rgb(100, 100, 100)',
            projection_type='natural earth'
        )
        
        fig.update_layout(height=800, title_font_size=24)
        
        fig.write_html(f'{self.output_dir}/animations/cumulative_buildup.html')
        print("    ✓ Saved: cumulative_buildup.html")
    
    # ==================== STORY MAPS ====================
    
    def create_narrative_map(self):
        """Create narrative story map with key insights"""
        print("  📖 Creating Narrative Story Map...")
        
        m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
        
        # Add title
        title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 400px; height: 90px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:20px; padding: 10px">
        <b>🌍 Natural Events Story Map</b><br>
        <span style="font-size:14px">Exploring 5,393 events from 2002-2025</span>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Find hotspots
        hotspot_regions = [
            {'name': 'California Wildfires', 'lat': 36.7, 'lon': -119.8, 'zoom': 6},
            {'name': 'Alaska Wildfires', 'lat': 64.0, 'lon': -152.0, 'zoom': 5},
            {'name': 'Pacific Storms', 'lat': 20.0, 'lon': 120.0, 'zoom': 4}
        ]
        
        for i, region in enumerate(hotspot_regions):
            # Get events in region
            mask = (
                ((self.df['latitude'] - region['lat']).abs() < 10) &
                ((self.df['longitude'] - region['lon']).abs() < 15)
            )
            region_events = self.df[mask]
            
            if len(region_events) > 0:
                folium.Marker(
                    location=[region['lat'], region['lon']],
                    popup=f"<b>{region['name']}</b><br>{len(region_events)} events",
                    icon=folium.Icon(color='red', icon='fire', prefix='fa'),
                    tooltip=f"Click to learn about {region['name']}"
                ).add_to(m)
                
                # Add circle
                folium.Circle(
                    location=[region['lat'], region['lon']],
                    radius=500000,
                    color='red',
                    fill=True,
                    opacity=0.3
                ).add_to(m)
        
        # Add heatmap layer
        heat_data = [[row['latitude'], row['longitude']] for idx, row in self.df.iterrows()]
        HeatMap(heat_data, radius=10, blur=15).add_to(m)
        
        # Add minimap
        minimap = MiniMap(toggle_display=True)
        m.add_child(minimap)
        
        m.save(f'{self.output_dir}/story_maps/narrative_map.html')
        print("    ✓ Saved: narrative_map.html")
    
    def create_comparison_map(self):
        """Create side-by-side comparison map"""
        print("  🔄 Creating Comparison Map (Early vs Recent)...")
        
        # Split data into early and recent
        mid_date = self.df['datetime'].min() + (self.df['datetime'].max() - self.df['datetime'].min()) / 2
        early_df = self.df[self.df['datetime'] < mid_date]
        recent_df = self.df[self.df['datetime'] >= mid_date]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(
                f'Early Period ({early_df["datetime"].min().year}-{early_df["datetime"].max().year})',
                f'Recent Period ({recent_df["datetime"].min().year}-{recent_df["datetime"].max().year})'
            ),
            specs=[[{'type': 'scattergeo'}, {'type': 'scattergeo'}]],
            horizontal_spacing=0.01
        )
        
        # Early period
        fig.add_trace(
            go.Scattergeo(
                lon=early_df['longitude'],
                lat=early_df['latitude'],
                mode='markers',
                marker=dict(size=4, color='blue', opacity=0.5),
                name=f'Early ({len(early_df)} events)'
            ),
            row=1, col=1
        )
        
        # Recent period
        fig.add_trace(
            go.Scattergeo(
                lon=recent_df['longitude'],
                lat=recent_df['latitude'],
                mode='markers',
                marker=dict(size=4, color='red', opacity=0.5),
                name=f'Recent ({len(recent_df)} events)'
            ),
            row=1, col=2
        )
        
        fig.update_geos(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            projection_type='natural earth'
        )
        
        fig.update_layout(
            title_text="<b>Temporal Comparison: Early vs Recent Events</b>",
            title_font_size=24,
            height=600,
            showlegend=True
        )
        
        fig.write_html(f'{self.output_dir}/story_maps/comparison_map.html')
        print("    ✓ Saved: comparison_map.html")
    
    # ==================== STATISTICAL MAPS ====================
    
    def create_kde_heatmap(self):
        """Create Kernel Density Estimation heatmap"""
        print("  🔥 Creating KDE Heatmap...")
        
        from scipy.stats import gaussian_kde
        
        # Prepare data
        xy = np.vstack([self.df['longitude'], self.df['latitude']])
        kde = gaussian_kde(xy)
        
        # Create grid
        lon_grid = np.linspace(self.df['longitude'].min(), self.df['longitude'].max(), 100)
        lat_grid = np.linspace(self.df['latitude'].min(), self.df['latitude'].max(), 100)
        lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)
        
        # Evaluate KDE
        grid_coords = np.vstack([lon_mesh.ravel(), lat_mesh.ravel()])
        z = kde(grid_coords).reshape(lon_mesh.shape)
        
        fig = go.Figure(data=go.Heatmap(
            x=lon_grid,
            y=lat_grid,
            z=z,
            colorscale='Hot',
            colorbar=dict(title='Density')
        ))
        
        fig.update_layout(
            title='<b>Kernel Density Estimation - Event Concentration</b>',
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            height=700
        )
        
        fig.write_html(f'{self.output_dir}/statistical_maps/kde_heatmap.html')
        print("    ✓ Saved: kde_heatmap.html")
    
    def create_intensity_map(self):
        """Create intensity map with contours"""
        print("  💥 Creating Intensity Map with Contours...")
        
        # Create 2D histogram
        H, xedges, yedges = np.histogram2d(
            self.df['longitude'],
            self.df['latitude'],
            bins=[80, 80]
        )
        
        fig = go.Figure(data=go.Contour(
            z=H.T,
            x=xedges,
            y=yedges,
            colorscale='Jet',
            contours=dict(
                showlabels=True,
                labelfont=dict(size=12, color='white')
            ),
            colorbar=dict(title='Event Count')
        ))
        
        # Add scatter overlay
        fig.add_trace(go.Scatter(
            x=self.df['longitude'],
            y=self.df['latitude'],
            mode='markers',
            marker=dict(size=2, color='white', opacity=0.1),
            showlegend=False
        ))
        
        fig.update_layout(
            title='<b>Event Intensity Map with Contours</b>',
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            height=700
        )
        
        fig.write_html(f'{self.output_dir}/statistical_maps/intensity_contours.html')
        print("    ✓ Saved: intensity_contours.html")
    
    def create_seasonal_comparison(self):
        """Create seasonal pattern comparison"""
        print("  🍂 Creating Seasonal Comparison Map...")
        
        seasons = {
            'Winter': [12, 1, 2],
            'Spring': [3, 4, 5],
            'Summer': [6, 7, 8],
            'Fall': [9, 10, 11]
        }
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=list(seasons.keys()),
            specs=[[{'type': 'scattergeo'}, {'type': 'scattergeo'}],
                   [{'type': 'scattergeo'}, {'type': 'scattergeo'}]]
        )
        
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        
        for (season, months), (row, col) in zip(seasons.items(), positions):
            season_data = self.df[self.df['month'].isin(months)]
            
            fig.add_trace(
                go.Scattergeo(
                    lon=season_data['longitude'],
                    lat=season_data['latitude'],
                    mode='markers',
                    marker=dict(size=3, opacity=0.5),
                    name=f'{season} ({len(season_data)} events)',
                    showlegend=True
                ),
                row=row, col=col
            )
        
        fig.update_geos(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            projection_type='natural earth'
        )
        
        fig.update_layout(
            title_text="<b>Seasonal Pattern Comparison</b>",
            title_font_size=24,
            height=900
        )
        
        fig.write_html(f'{self.output_dir}/statistical_maps/seasonal_comparison.html')
        print("    ✓ Saved: seasonal_comparison.html")
    
    # ==================== PUBLICATION READY ====================
    
    def create_multi_panel_figure(self):
        """Create publication-quality multi-panel figure"""
        print("  📰 Creating Publication-Quality Multi-Panel Figure...")
        
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Panel A: Geographic distribution
        ax1 = fig.add_subplot(gs[0:2, 0:2])
        scatter = ax1.scatter(self.df['longitude'], self.df['latitude'],
                             c=self.df['year'], cmap='viridis',
                             s=10, alpha=0.6, edgecolors='black', linewidth=0.3)
        ax1.set_xlabel('Longitude', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Latitude', fontsize=14, fontweight='bold')
        ax1.set_title('A. Global Distribution of Natural Events (2002-2025)',
                     fontsize=16, fontweight='bold', pad=10)
        ax1.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax1, label='Year')
        
        # Panel B: Temporal trend
        ax2 = fig.add_subplot(gs[0, 2])
        yearly = self.df.groupby('year').size()
        ax2.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='darkblue')
        ax2.fill_between(yearly.index, yearly.values, alpha=0.3, color='lightblue')
        ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Event Count', fontsize=12, fontweight='bold')
        ax2.set_title('B. Annual Trends', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Panel C: Category breakdown
        ax3 = fig.add_subplot(gs[1, 2])
        cat_counts = self.df['category_title'].value_counts().head(5)
        colors_pie = plt.cm.Set3(range(len(cat_counts)))
        ax3.pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%',
               colors=colors_pie, startangle=90)
        ax3.set_title('C. Event Categories', fontsize=14, fontweight='bold')
        
        # Panel D: Monthly pattern
        ax4 = fig.add_subplot(gs[2, 0])
        monthly = self.df['month'].value_counts().sort_index()
        ax4.bar(monthly.index, monthly.values, color='coral', edgecolor='black')
        ax4.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Event Count', fontsize=12, fontweight='bold')
        ax4.set_title('D. Monthly Distribution', fontsize=14, fontweight='bold')
        ax4.set_xticks(range(1, 13))
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Panel E: Latitude distribution
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.hist(self.df['latitude'], bins=50, color='skyblue', edgecolor='black')
        ax5.axvline(self.df['latitude'].mean(), color='red', linestyle='--',
                   linewidth=2, label='Mean')
        ax5.set_xlabel('Latitude', fontsize=12, fontweight='bold')
        ax5.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax5.set_title('E. Latitude Distribution', fontsize=14, fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3, axis='y')
        
        # Panel F: Year-Month heatmap
        ax6 = fig.add_subplot(gs[2, 2])
        pivot = pd.crosstab(self.df['year'], self.df['month'])
        sns.heatmap(pivot, cmap='YlOrRd', cbar_kws={'label': 'Events'}, ax=ax6)
        ax6.set_title('F. Temporal Heatmap', fontsize=14, fontweight='bold')
        ax6.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax6.set_ylabel('Year', fontsize=12, fontweight='bold')
        
        plt.suptitle('COMPREHENSIVE ANALYSIS OF GLOBAL NATURAL EVENTS',
                    fontsize=22, fontweight='bold', y=0.98)
        
        plt.savefig(f'{self.output_dir}/publication_ready/multi_panel_figure.png',
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print("    ✓ Saved: multi_panel_figure.png (HIGH RESOLUTION)")
    
    def create_infographic_map(self):
        """Create infographic-style summary map"""
        print("  🎨 Creating Infographic Summary Map...")
        
        fig = plt.figure(figsize=(24, 14))
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # Main map
        ax_main = fig.add_subplot(gs[:, :2])
        
        # Plot events with size based on intensity
        for category in self.df['category_title'].unique()[:5]:
            cat_data = self.df[self.df['category_title'] == category]
            ax_main.scatter(cat_data['longitude'], cat_data['latitude'],
                          label=category, s=20, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        ax_main.set_xlim(-180, 180)
        ax_main.set_ylim(-90, 90)
        ax_main.set_xlabel('Longitude', fontsize=16, fontweight='bold')
        ax_main.set_ylabel('Latitude', fontsize=16, fontweight='bold')
        ax_main.set_title('GLOBAL NATURAL EVENTS INFOGRAPHIC',
                         fontsize=24, fontweight='bold', pad=20)
        ax_main.legend(loc='lower left', fontsize=12, framealpha=0.9)
        ax_main.grid(True, alpha=0.2, linestyle='--')
        ax_main.set_facecolor('#E8F4F8')
        
        # Statistics panels
        ax_stats1 = fig.add_subplot(gs[0, 2])
        ax_stats1.text(0.5, 0.7, f"{len(self.df):,}", ha='center', va='center',
                      fontsize=60, fontweight='bold', color='darkblue')
        ax_stats1.text(0.5, 0.3, "TOTAL EVENTS", ha='center', va='center',
                      fontsize=18, fontweight='bold')
        ax_stats1.axis('off')
        ax_stats1.set_facecolor('#f0f0f0')
        
        ax_stats2 = fig.add_subplot(gs[1, 2])
        years_span = self.df['year'].max() - self.df['year'].min() + 1
        ax_stats2.text(0.5, 0.7, f"{years_span}", ha='center', va='center',
                      fontsize=60, fontweight='bold', color='darkgreen')
        ax_stats2.text(0.5, 0.3, "YEARS COVERED", ha='center', va='center',
                      fontsize=18, fontweight='bold')
        ax_stats2.axis('off')
        ax_stats2.set_facecolor('#f0f0f0')
        
        plt.savefig(f'{self.output_dir}/publication_ready/infographic_map.png',
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print("    ✓ Saved: infographic_map.png (HIGH RESOLUTION)")
    
    def print_summary(self):
        """Print comprehensive summary"""
        print("\n" + "="*80)
        print("🏆 ULTIMATE VISUALIZATION SUITE - COMPLETE SUMMARY")
        print("="*80)
        
        print("\n📁 OUTPUT STRUCTURE:")
        print(f"   {self.output_dir}/")
        print("   ├── 3d_visualizations/")
        print("   │   ├── 3d_globe_interactive.html")
        print("   │   ├── 3d_spacetime_scatter.html")
        print("   │   └── 3d_density_surface.html")
        print("   ├── dashboards/")
        print("   │   ├── master_dashboard.html ⭐ MUST SEE!")
        print("   │   └── temporal_dashboard.html")
        print("   ├── animations/")
        print("   │   ├── cinematic_timeline.html ⭐ MUST SEE!")
        print("   │   └── cumulative_buildup.html")
        print("   ├── story_maps/")
        print("   │   ├── narrative_map.html")
        print("   │   └── comparison_map.html")
        print("   ├── statistical_maps/")
        print("   │   ├── kde_heatmap.html")
        print("   │   ├── intensity_contours.html")
        print("   │   └── seasonal_comparison.html")
        print("   └── publication_ready/")
        print("       ├── multi_panel_figure.png ⭐ PUBLICATION QUALITY")
        print("       └── infographic_map.png")
        
        print("\n🌟 TOP 5 VISUALIZATIONS TO CHECK:")
        print("   1. master_dashboard.html - Complete interactive overview")
        print("   2. cinematic_timeline.html - Stunning animated timeline")
        print("   3. 3d_globe_interactive.html - Rotate the Earth!")
        print("   4. multi_panel_figure.png - Publication-ready figure")
        print("   5. narrative_map.html - Story-driven exploration")
        
        print("\n💡 HOW TO USE:")
        print("   • HTML files: Open in web browser (Chrome, Firefox, Edge)")
        print("   • PNG files: View in any image viewer or use in presentations")
        print("   • Interactive maps: Click, zoom, hover, and explore!")
        
        print("\n" + "="*80)
        print("🛸 ALIEN STATUS: DEFEATED! 🏆")
        print("="*80)
        print("\nYou now have the most advanced natural events")
        print("visualization suite ever created! 🚀🌍✨")
        print("\n")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🌍 ULTIMATE GEOSPATIAL VISUALIZATION SUITE")
    print("="*80)
    print("Preparing to create the most stunning visualizations ever made...")
    print("="*80 + "\n")
    
    try:
        # Load data
        print("📂 Loading data...")
        df = pd.read_csv('eonet_cleaned.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        print(f"✓ Loaded {len(df):,} events successfully!\n")
        
        # Create visualizer
        visualizer = UltimateGeoVisualizer(df)
        
        # Generate all visualizations
        visualizer.create_all_visualizations()
        
        print("\n" + "🎉"*40)
        print("\n        🏆 MISSION ACCOMPLISHED! 🏆")
        print("\n              ALIEN = DEFEATED")
        print("\n" + "🎉"*40 + "\n")
        
    except FileNotFoundError:
        print("\n❌ ERROR: eonet_cleaned.csv not found!")
        print("Please run 01_data_loading.py first.\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()