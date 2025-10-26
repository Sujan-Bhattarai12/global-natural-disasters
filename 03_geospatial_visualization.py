"""
NASA EONET - POLICY-FOCUSED GEOSPATIAL VISUALIZATION SUITE
=============================================================
Designed for Mars-Earth Policy Recommendations

Key Principles:
- Dynamic date ranges (adapts to actual data)
- Clean, readable labels
- No repetition - each chart serves unique purpose
- Policy-relevant insights
- Decision-support visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap, MarkerCluster
import seaborn as sns
from datetime import datetime
from scipy.stats import gaussian_kde
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import os
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")


class PolicyVisualizationSuite:
    """Policy-focused geospatial visualization suite"""
    
    def __init__(self, df):
        self.df = df
        self.output_dir = 'policy_visualizations'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Analyze actual date range
        self.start_date = df['datetime'].min()
        self.end_date = df['datetime'].max()
        self.date_range_years = (self.end_date - self.start_date).days / 365.25
        
        print("="*80)
        print("POLICY-FOCUSED VISUALIZATION SUITE")
        print("="*80)
        print(f"Dataset: {len(df):,} events")
        print(f"Period: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        print(f"Coverage: {self.date_range_years:.1f} years")
        print(f"Categories: {df['category_title'].nunique()}")
        print("="*80 + "\n")
    
    def create_all_visualizations(self):
        """Generate all policy-focused visualizations"""
        
        print("GENERATING POLICY VISUALIZATIONS\n")
        
        # Section 1: Executive Summary
        print("Section 1: Executive Summary Dashboard")
        self.create_executive_dashboard()
        
        # Section 2: Risk Assessment
        print("\nSection 2: Risk Assessment Maps")
        self.create_risk_hotspot_map()
        self.create_temporal_risk_analysis()
        
        # Section 3: Geographic Intelligence
        print("\nSection 3: Geographic Intelligence")
        self.create_3d_globe_intelligence()
        self.create_regional_impact_analysis()
        
        # Section 4: Predictive Insights
        print("\nSection 4: Predictive Insights")
        self.create_trend_forecasting()
        self.create_seasonal_risk_calendar()
        
        # Section 5: Policy Recommendations
        print("\nSection 5: Policy Recommendation Report")
        self.create_policy_report()
        
        print("\n" + "="*80)
        print("VISUALIZATION SUITE COMPLETE")
        print("="*80)
        self.print_summary()
    
    # ========== EXECUTIVE SUMMARY ==========
    
    def create_executive_dashboard(self):
        """Clean executive dashboard with key metrics"""
        print("  Creating Executive Dashboard...")
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=(
                'Event Distribution by Category',
                'Temporal Trend',
                'Geographic Coverage',
                'Monthly Risk Pattern',
                'Top 5 Affected Regions',
                'Event Severity Index'
            ),
            specs=[
                [{'type': 'pie'}, {'type': 'scatter'}, {'type': 'scattergeo'}],
                [{'type': 'bar'}, {'type': 'bar'}, {'type': 'indicator'}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # 1. Clean pie chart with readable labels
        cat_counts = self.df['category_title'].value_counts().head(5)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        fig.add_trace(
            go.Pie(
                labels=[f"{cat[:20]}" for cat in cat_counts.index],  # Truncate long labels
                values=cat_counts.values,
                hole=0.3,
                marker=dict(colors=colors),
                textinfo='label+percent',
                textfont=dict(size=11),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # 2. Temporal trend - adaptive to date range
        if self.date_range_years > 3:
            # Yearly trend for longer periods
            yearly = self.df.groupby('year').size()
            x_data = yearly.index
            y_data = yearly.values
            x_title = 'Year'
        else:
            # Monthly trend for shorter periods
            monthly = self.df.groupby(self.df['datetime'].dt.to_period('M')).size()
            x_data = [str(x) for x in monthly.index]
            y_data = monthly.values
            x_title = 'Month'
        
        fig.add_trace(
            go.Scatter(
                x=x_data,
                y=y_data,
                mode='lines+markers',
                line=dict(color='#FF6B6B', width=3),
                marker=dict(size=8),
                name='Events',
                fill='tozeroy',
                fillcolor='rgba(255, 107, 107, 0.2)'
            ),
            row=1, col=2
        )
        
        # 3. Geographic coverage - sampled for clarity
        sample_size = min(1000, len(self.df))
        df_sample = self.df.sample(sample_size, random_state=42)
        
        fig.add_trace(
            go.Scattergeo(
                lon=df_sample['longitude'],
                lat=df_sample['latitude'],
                mode='markers',
                marker=dict(
                    size=4,
                    color='#FF6B6B',
                    opacity=0.6,
                    line=dict(width=0)
                ),
                name='Events',
                hovertemplate='Lat: %{lat:.2f}<br>Lon: %{lon:.2f}<extra></extra>'
            ),
            row=1, col=3
        )
        
        # 4. Monthly risk pattern - all months
        month_counts = self.df['month'].value_counts().sort_index()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig.add_trace(
            go.Bar(
                x=month_names,
                y=[month_counts.get(i, 0) for i in range(1, 13)],
                marker=dict(color='#4ECDC4'),
                name='Events by Month'
            ),
            row=2, col=1
        )
        
        # 5. Top affected regions (by coordinate clustering)
        self.df['lat_region'] = pd.cut(self.df['latitude'], bins=10, labels=False)
        self.df['lon_region'] = pd.cut(self.df['longitude'], bins=10, labels=False)
        self.df['region_id'] = self.df['lat_region'].astype(str) + '_' + self.df['lon_region'].astype(str)
        
        top_regions = self.df['region_id'].value_counts().head(5)
        region_labels = [f"Region {i+1}" for i in range(len(top_regions))]
        
        fig.add_trace(
            go.Bar(
                x=region_labels,
                y=top_regions.values,
                marker=dict(color='#45B7D1'),
                name='Events per Region'
            ),
            row=2, col=2
        )
        
        # 6. Severity Index (events per day metric)
        days_in_period = (self.end_date - self.start_date).days
        events_per_day = len(self.df) / max(days_in_period, 1)
        
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=events_per_day,
                title={"text": "Events/Day<br><span style='font-size:0.8em'>Risk Metric</span>"},
                delta={'reference': events_per_day * 0.8, 'relative': False},
                number={'suffix': '', 'font': {'size': 40}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=2, col=3
        )
        
        # Update layout
        fig.update_geos(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            projection_type='natural earth',
            showframe=False
        )
        
        fig.update_xaxes(title_text=x_title, row=1, col=2)
        fig.update_yaxes(title_text='Events', row=1, col=2)
        fig.update_xaxes(title_text='Month', row=2, col=1)
        fig.update_yaxes(title_text='Events', row=2, col=1)
        fig.update_xaxes(title_text='Region', row=2, col=2)
        fig.update_yaxes(title_text='Events', row=2, col=2)
        
        fig.update_layout(
            title_text=f"<b>Executive Dashboard: Natural Events {self.start_date.year}-{self.end_date.year}</b>",
            title_font_size=22,
            showlegend=False,
            height=900
        )
        
        fig.write_html(f'{self.output_dir}/01_executive_dashboard.html')
        print("    ✓ Saved: 01_executive_dashboard.html")
    
    # ========== RISK ASSESSMENT ==========
    
    def create_risk_hotspot_map(self):
        """Advanced hotspot analysis for risk assessment"""
        print("  Creating Risk Hotspot Map...")
        
        # Create KDE for risk zones
        xy = np.vstack([self.df['longitude'], self.df['latitude']])
        kde = gaussian_kde(xy, bw_method='scott')
        
        # Create grid
        lon_range = self.df['longitude'].max() - self.df['longitude'].min()
        lat_range = self.df['latitude'].max() - self.df['latitude'].min()
        
        lon_grid = np.linspace(self.df['longitude'].min() - lon_range*0.1, 
                              self.df['longitude'].max() + lon_range*0.1, 100)
        lat_grid = np.linspace(self.df['latitude'].min() - lat_range*0.1, 
                              self.df['latitude'].max() + lat_range*0.1, 100)
        lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)
        
        # Evaluate KDE
        grid_coords = np.vstack([lon_mesh.ravel(), lat_mesh.ravel()])
        z = kde(grid_coords).reshape(lon_mesh.shape)
        
        # Create risk zones
        fig = go.Figure()
        
        # Add contour map
        fig.add_trace(go.Contour(
            x=lon_grid,
            y=lat_grid,
            z=z,
            colorscale=[
                [0, 'rgb(255,255,255)'],
                [0.3, 'rgb(255,255,178)'],
                [0.5, 'rgb(254,204,92)'],
                [0.7, 'rgb(253,141,60)'],
                [0.9, 'rgb(227,26,28)'],
                [1, 'rgb(128,0,38)']
            ],
            contours=dict(
                start=z.min(),
                end=z.max(),
                size=(z.max()-z.min())/10,
                showlabels=True,
                labelfont=dict(size=10, color='white')
            ),
            colorbar=dict(
                title='Risk<br>Level',
                ticktext=['Low', 'Medium', 'High', 'Critical'],
                tickvals=[z.min(), z.min() + (z.max()-z.min())*0.33,
                         z.min() + (z.max()-z.min())*0.66, z.max()],
                len=0.7
            )
        ))
        
        # Add scatter overlay
        fig.add_trace(go.Scatter(
            x=self.df['longitude'],
            y=self.df['latitude'],
            mode='markers',
            marker=dict(
                size=3,
                color='white',
                opacity=0.3,
                line=dict(width=0)
            ),
            name='Events',
            hovertemplate='<b>Event</b><br>Lat: %{y:.2f}<br>Lon: %{x:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'<b>Risk Hotspot Analysis ({self.start_date.year}-{self.end_date.year})</b><br>' + 
                  '<sub>Kernel Density Estimation showing high-risk zones</sub>',
            title_font_size=20,
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            height=700,
            showlegend=False
        )
        
        fig.write_html(f'{self.output_dir}/02_risk_hotspot_map.html')
        print("    ✓ Saved: 02_risk_hotspot_map.html")
    
    def create_temporal_risk_analysis(self):
        """Temporal risk evolution"""
        print("  Creating Temporal Risk Analysis...")
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(
                f'Event Frequency Trend ({self.start_date.year}-{self.end_date.year})',
                'Seasonal Risk Distribution'
            ),
            vertical_spacing=0.15,
            row_heights=[0.5, 0.5]
        )
        
        # Cumulative trend
        daily = self.df.groupby(self.df['datetime'].dt.date).size().sort_index()
        cumulative = daily.cumsum()
        
        fig.add_trace(
            go.Scatter(
                x=daily.index,
                y=cumulative.values,
                mode='lines',
                fill='tozeroy',
                line=dict(color='#FF6B6B', width=2),
                fillcolor='rgba(255, 107, 107, 0.3)',
                name='Cumulative Events'
            ),
            row=1, col=1
        )
        
        # Seasonal heatmap
        self.df['season'] = self.df['month'].map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        })
        
        pivot = pd.crosstab(self.df['year'], self.df['season'])[['Winter', 'Spring', 'Summer', 'Fall']]
        
        fig.add_trace(
            go.Heatmap(
                z=pivot.values,
                x=['Winter', 'Spring', 'Summer', 'Fall'],
                y=pivot.index,
                colorscale='Reds',
                colorbar=dict(title='Events', len=0.4, y=0.2),
                text=pivot.values,
                texttemplate='%{text}',
                textfont=dict(size=10)
            ),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text='Date', row=1, col=1)
        fig.update_yaxes(title_text='Cumulative Events', row=1, col=1)
        fig.update_xaxes(title_text='Season', row=2, col=1)
        fig.update_yaxes(title_text='Year', row=2, col=1)
        
        fig.update_layout(
            title_text='<b>Temporal Risk Evolution Analysis</b>',
            title_font_size=20,
            showlegend=False,
            height=900
        )
        
        fig.write_html(f'{self.output_dir}/03_temporal_risk_analysis.html')
        print("    ✓ Saved: 03_temporal_risk_analysis.html")
    
    # ========== GEOGRAPHIC INTELLIGENCE ==========
    
    def create_3d_globe_intelligence(self):
        """3D globe with intelligence overlay"""
        print("  Creating 3D Geographic Intelligence Globe...")
        
        # Sample for performance
        sample_size = min(2000, len(self.df))
        df_sample = self.df.sample(sample_size, random_state=42)
        
        fig = go.Figure()
        
        # Get top 3 categories only
        top_cats = self.df['category_title'].value_counts().head(3).index
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        for i, cat in enumerate(top_cats):
            cat_data = df_sample[df_sample['category_title'] == cat]
            
            fig.add_trace(go.Scattergeo(
                lon=cat_data['longitude'],
                lat=cat_data['latitude'],
                text=cat_data['title'],
                name=cat,
                mode='markers',
                marker=dict(
                    size=6,
                    color=colors[i],
                    opacity=0.7,
                    line=dict(width=0.5, color='white')
                ),
                hovertemplate='<b>%{text}</b><br>Category: ' + cat + '<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text=f'<b>3D Geographic Intelligence ({self.start_date.year}-{self.end_date.year})</b>',
                font=dict(size=20)
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
                projection_rotation=dict(lon=-30, lat=30, roll=0)
            ),
            height=800,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255,255,255,0.9)",
                font=dict(size=12)
            )
        )
        
        fig.write_html(f'{self.output_dir}/04_3d_intelligence_globe.html')
        print("    ✓ Saved: 04_3d_intelligence_globe.html")
    
    def create_regional_impact_analysis(self):
        """Regional impact breakdown"""
        print("  Creating Regional Impact Analysis...")
        
        # Define meaningful regions
        def assign_region(row):
            lat, lon = row['latitude'], row['longitude']
            if -170 < lon < -50:
                if lat > 15:
                    return 'North America'
                else:
                    return 'South America'
            elif -20 < lon < 60:
                if lat > 35:
                    return 'Europe'
                else:
                    return 'Africa'
            elif 60 < lon < 150:
                if lat > 0:
                    return 'Asia'
                else:
                    return 'Oceania'
            else:
                return 'Other'
        
        self.df['region'] = self.df.apply(assign_region, axis=1)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(
                'Events by Region',
                'Regional Trend Analysis'
            ),
            specs=[[{'type': 'bar'}, {'type': 'scatter'}]],
            horizontal_spacing=0.15
        )
        
        # Regional distribution
        region_counts = self.df['region'].value_counts().sort_values(ascending=True)
        
        fig.add_trace(
            go.Bar(
                y=region_counts.index,
                x=region_counts.values,
                orientation='h',
                marker=dict(color='#FF6B6B'),
                text=region_counts.values,
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Events: %{x}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Regional trends
        for region in region_counts.head(5).index:
            region_data = self.df[self.df['region'] == region]
            yearly = region_data.groupby('year').size()
            
            fig.add_trace(
                go.Scatter(
                    x=yearly.index,
                    y=yearly.values,
                    mode='lines+markers',
                    name=region,
                    line=dict(width=2),
                    marker=dict(size=6)
                ),
                row=1, col=2
            )
        
        fig.update_xaxes(title_text='Number of Events', row=1, col=1)
        fig.update_yaxes(title_text='Region', row=1, col=1)
        fig.update_xaxes(title_text='Year', row=1, col=2)
        fig.update_yaxes(title_text='Events', row=1, col=2)
        
        fig.update_layout(
            title_text='<b>Regional Impact Analysis</b>',
            title_font_size=20,
            showlegend=True,
            height=600,
            legend=dict(font=dict(size=11))
        )
        
        fig.write_html(f'{self.output_dir}/05_regional_impact_analysis.html')
        print("    ✓ Saved: 05_regional_impact_analysis.html")
    
    # ========== PREDICTIVE INSIGHTS ==========
    
    def create_trend_forecasting(self):
        """Trend analysis with forecast indicators"""
        print("  Creating Trend Forecasting Analysis...")
        
        yearly = self.df.groupby('year').size()
        
        # Simple linear trend
        years = yearly.index.values
        values = yearly.values
        z = np.polyfit(years, values, 1)
        p = np.poly1d(z)
        trend_line = p(years)
        
        # Calculate growth rate
        if len(values) > 1:
            growth_rate = ((values[-1] - values[0]) / values[0]) * 100
        else:
            growth_rate = 0
        
        fig = go.Figure()
        
        # Actual data
        fig.add_trace(go.Scatter(
            x=years,
            y=values,
            mode='lines+markers',
            name='Actual Events',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)'
        ))
        
        # Trend line
        fig.add_trace(go.Scatter(
            x=years,
            y=trend_line,
            mode='lines',
            name='Trend Line',
            line=dict(color='#45B7D1', width=2, dash='dash')
        ))
        
        # Add annotation
        fig.add_annotation(
            x=years[-1],
            y=values[-1],
            text=f'Growth Rate: {growth_rate:+.1f}%',
            showarrow=True,
            arrowhead=2,
            bgcolor='white',
            bordercolor='#FF6B6B',
            borderwidth=2,
            font=dict(size=14)
        )
        
        fig.update_layout(
            title=f'<b>Event Frequency Trend & Forecast ({self.start_date.year}-{self.end_date.year})</b>',
            title_font_size=20,
            xaxis_title='Year',
            yaxis_title='Number of Events',
            height=600,
            showlegend=True,
            legend=dict(font=dict(size=12))
        )
        
        fig.write_html(f'{self.output_dir}/06_trend_forecasting.html')
        print("    ✓ Saved: 06_trend_forecasting.html")
    
    def create_seasonal_risk_calendar(self):
        """Seasonal risk calendar for planning"""
        print("  Creating Seasonal Risk Calendar...")
        
        # Create month-day heatmap
        self.df['month_day'] = self.df['datetime'].dt.strftime('%m-%d')
        
        # Aggregate by month and day of month
        self.df['day_of_month'] = self.df['datetime'].dt.day
        pivot = pd.crosstab(self.df['month'], self.df['day_of_month'])
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=list(range(1, 32)),
            y=month_names,
            colorscale='Reds',
            colorbar=dict(title='Events'),
            hovertemplate='<b>%{y} %{x}</b><br>Events: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title='<b>Seasonal Risk Calendar: When Events Occur</b>',
            title_font_size=20,
            xaxis_title='Day of Month',
            yaxis_title='Month',
            height=600
        )
        
        fig.write_html(f'{self.output_dir}/07_seasonal_risk_calendar.html')
        print("    ✓ Saved: 07_seasonal_risk_calendar.html")
    
    # ========== POLICY REPORT ==========
    
    def create_policy_report(self):
        """Generate policy recommendation report"""
        print("  Creating Policy Recommendation Report...")
        
        fig = plt.figure(figsize=(20, 14))
        fig.suptitle(f'POLICY RECOMMENDATION REPORT: Natural Events {self.start_date.year}-{self.end_date.year}',
                    fontsize=24, fontweight='bold', y=0.98)
        
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
        
        # Panel 1: Geographic Distribution
        ax1 = fig.add_subplot(gs[0:2, 0:2])
        scatter = ax1.scatter(self.df['longitude'], self.df['latitude'],
                            c=self.df['year'], cmap='YlOrRd',
                            s=15, alpha=0.6, edgecolors='black', linewidth=0.3)
        ax1.set_xlabel('Longitude', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Latitude', fontsize=14, fontweight='bold')
        ax1.set_title(f'A. Global Distribution of {len(self.df):,} Events',
                     fontsize=16, fontweight='bold', pad=10)
        ax1.grid(True, alpha=0.3)
        cbar = plt.colorbar(scatter, ax=ax1, label='Year')
        cbar.ax.tick_params(labelsize=10)
        
        # Panel 2: Category Breakdown (clean)
        ax2 = fig.add_subplot(gs[0, 2])
        cat_counts = self.df['category_title'].value_counts().head(5)
        colors = plt.cm.Set3(range(len(cat_counts)))
        
        # Truncate labels
        labels = [label[:20] + '...' if len(label) > 20 else label for label in cat_counts.index]
        
        wedges, texts, autotexts = ax2.pie(cat_counts.values, labels=labels,
                                           autopct='%1.1f%%', colors=colors,
                                           startangle=90, textprops={'fontsize': 10})
        ax2.set_title('B. Event Categories', fontsize=14, fontweight='bold')
        
        # Panel 3: Temporal Trend
        ax3 = fig.add_subplot(gs[1, 2])
        yearly = self.df.groupby('year').size()
        ax3.plot(yearly.index, yearly.values, marker='o', linewidth=3,
                color='#FF6B6B', markersize=8)
        ax3.fill_between(yearly.index, yearly.values, alpha=0.3, color='#FF6B6B')
        ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Events', fontsize=12, fontweight='bold')
        ax3.set_title('C. Annual Trend', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Panel 4: Monthly Pattern
        ax4 = fig.add_subplot(gs[2, 0])
        monthly = self.df['month'].value_counts().sort_index()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax4.bar(month_names, [monthly.get(i, 0) for i in range(1, 13)],
               color='#4ECDC4', edgecolor='black')
        ax4.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Events', fontsize=12, fontweight='bold')
        ax4.set_title('D. Seasonal Pattern', fontsize=14, fontweight='bold')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Panel 5: Regional Distribution
        ax5 = fig.add_subplot(gs[2, 1])
        region_counts = self.df['region'].value_counts().head(5)
        ax5.barh(range(len(region_counts)), region_counts.values,
                color='#45B7D1', edgecolor='black')
        ax5.set_yticks(range(len(region_counts)))
        ax5.set_yticklabels(region_counts.index, fontsize=10)
        ax5.set_xlabel('Events', fontsize=12, fontweight='bold')
        ax5.set_title('E. Top 5 Regions', fontsize=14, fontweight='bold')
        ax5.invert_yaxis()
        ax5.grid(True, alpha=0.3, axis='x')
        
        # Panel 6: Key Metrics
        ax6 = fig.add_subplot(gs[2, 2])
        ax6.axis('off')
        
        # Calculate key metrics
        total_events = len(self.df)
        avg_per_year = total_events / max(self.date_range_years, 1)
        top_category = self.df['category_title'].value_counts().index[0]
        top_category_pct = (self.df['category_title'].value_counts().iloc[0] / total_events) * 100
        
        metrics_text = f"""
KEY METRICS

Total Events: {total_events:,}
Time Period: {self.date_range_years:.1f} years
Avg/Year: {avg_per_year:.0f}

Top Category:
{top_category[:30]}
({top_category_pct:.1f}%)

Geographic Span:
Lat: {self.df['latitude'].min():.1f}° to {self.df['latitude'].max():.1f}°
Lon: {self.df['longitude'].min():.1f}° to {self.df['longitude'].max():.1f}°
        """
        
        ax6.text(0.1, 0.5, metrics_text, transform=ax6.transAxes,
                fontsize=11, verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
                family='monospace')
        ax6.set_title('F. Summary Metrics', fontsize=14, fontweight='bold')
        
        plt.savefig(f'{self.output_dir}/08_policy_report.png',
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print("    ✓ Saved: 08_policy_report.png (300 DPI)")
    
    def print_summary(self):
        """Print summary of generated files"""
        print("\n" + "="*80)
        print("POLICY VISUALIZATION SUITE - FILES GENERATED")
        print("="*80)
        print(f"\nOutput Directory: {self.output_dir}/")
        print("\nExecutive & Planning:")
        print("  1. 01_executive_dashboard.html - Key metrics overview")
        print("\nRisk Assessment:")
        print("  2. 02_risk_hotspot_map.html - High-risk geographic zones")
        print("  3. 03_temporal_risk_analysis.html - Risk evolution over time")
        print("\nGeographic Intelligence:")
        print("  4. 04_3d_intelligence_globe.html - 3D rotating globe")
        print("  5. 05_regional_impact_analysis.html - Regional breakdowns")
        print("\nPredictive Insights:")
        print("  6. 06_trend_forecasting.html - Trend analysis")
        print("  7. 07_seasonal_risk_calendar.html - Planning calendar")
        print("\nPolicy Report:")
        print("  8. 08_policy_report.png - Publication-ready summary")
        
        print("\n" + "="*80)
        print("RECOMMENDED VIEWING ORDER")
        print("="*80)
        print("\nFor Mars-Earth Policy Meeting:")
        print("  1. Start: 01_executive_dashboard.html")
        print("  2. Risks: 02_risk_hotspot_map.html")
        print("  3. Globe: 04_3d_intelligence_globe.html")
        print("  4. Print: 08_policy_report.png")
        
        print("\n" + "="*80)
        print("All visualizations adapt to your actual date range!")
        print(f"Your data: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        print("="*80 + "\n")


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("POLICY-FOCUSED VISUALIZATION SUITE")
    print("="*80 + "\n")
    
    try:
        # Load data
        print("Loading data...")
        df = pd.read_csv('eonet_cleaned.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        print(f"Loaded {len(df):,} events\n")
        
        # Create visualizer
        visualizer = PolicyVisualizationSuite(df)
        
        # Generate all visualizations
        visualizer.create_all_visualizations()
        
        print("\n" + "="*80)
        print("MISSION ACCOMPLISHED")
        print("="*80)
        print("\nReady for Mars-Earth policy recommendations!")
        print("\n")
        
    except FileNotFoundError:
        print("\nERROR: eonet_cleaned.csv not found!")
        print("Please run 01_data_loading.py first.\n")
    except Exception as e:
        print(f"\nERROR: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()