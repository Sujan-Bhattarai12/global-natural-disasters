"""
NASA EONET API Data Fetcher
Retrieves complete natural events data directly from NASA's EONET API
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time

class EONETDataFetcher:
    """Fetch natural events data from NASA EONET API"""
    
    def __init__(self):
        self.base_url = "https://eonet.gsfc.nasa.gov/api/v3"
        self.events_endpoint = f"{self.base_url}/events"
        self.categories_endpoint = f"{self.base_url}/categories"
        
    def get_categories(self):
        """Fetch available event categories"""
        print("Fetching event categories from NASA EONET...")
        
        try:
            response = requests.get(self.categories_endpoint)
            response.raise_for_status()
            data = response.json()
            
            categories = pd.DataFrame(data['categories'])
            print(f"\nAvailable Categories:")
            for idx, row in categories.iterrows():
                print(f"  {row['id']}: {row['title']}")
            
            return categories
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return None
    
    def fetch_events(self, days=None, start_date=None, end_date=None, 
                     status='all', limit=None):
        """
        Fetch events from EONET API
        
        Parameters:
        -----------
        days : int, optional
            Number of days from today to fetch (e.g., days=30 for last 30 days)
        start_date : str, optional
            Start date in YYYY-MM-DD format
        end_date : str, optional
            End date in YYYY-MM-DD format
        status : str
            'open', 'closed', or 'all' (default: 'all')
        limit : int, optional
            Maximum number of events to fetch
        """
        print("="*70)
        print("FETCHING DATA FROM NASA EONET API")
        print("="*70)
        
        # Build query parameters
        params = {
            'status': status
        }
        
        if days:
            params['days'] = days
            print(f"\nFetching events from last {days} days...")
        elif start_date and end_date:
            params['start'] = start_date
            params['end'] = end_date
            print(f"\nFetching events from {start_date} to {end_date}...")
        elif start_date:
            params['start'] = start_date
            print(f"\nFetching events from {start_date} onwards...")
        
        if limit:
            params['limit'] = limit
        
        try:
            print(f"API URL: {self.events_endpoint}")
            print(f"Parameters: {params}\n")
            
            response = requests.get(self.events_endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            events = data.get('events', [])
            print(f"Retrieved {len(events)} events from API\n")
            
            return events
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching events: {e}")
            return None
    
    def parse_events(self, events):
        """Parse events into structured DataFrame"""
        print("Parsing event data...")
        
        parsed_events = []
        
        for event in events:
            event_id = event.get('id')
            title = event.get('title')
            description = event.get('description', '')
            
            # Get categories
            categories = event.get('categories', [])
            category_title = categories[0]['title'] if categories else 'Unknown'
            
            # Get geometries (coordinates)
            geometries = event.get('geometry', [])
            
            if geometries:
                for geom in geometries:
                    # Parse date
                    date_str = geom.get('date')
                    if date_str:
                        try:
                            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                            date = dt.strftime('%Y-%m-%d')
                            time = dt.strftime('%H:%M:%S')
                            year = dt.year
                        except:
                            date = None
                            time = None
                            year = None
                    else:
                        date = None
                        time = None
                        year = None
                    
                    # Get coordinates
                    coords = geom.get('coordinates', [])
                    if coords and len(coords) >= 2:
                        longitude = coords[0]
                        latitude = coords[1]
                    else:
                        longitude = None
                        latitude = None
                    
                    # Create event record
                    parsed_events.append({
                        'ID': event_id,
                        'Title': title,
                        'Description': description,
                        'Category_title': category_title,
                        'Date': date,
                        'Time': time,
                        'Year': year,
                        'Longitude': longitude,
                        'Latitude': latitude
                    })
            else:
                # Event without geometry
                parsed_events.append({
                    'ID': event_id,
                    'Title': title,
                    'Description': description,
                    'Category_title': category_title,
                    'Date': None,
                    'Time': None,
                    'Year': None,
                    'Longitude': None,
                    'Latitude': None
                })
        
        df = pd.DataFrame(parsed_events)
        
        # Remove duplicates and null coordinates
        df = df.dropna(subset=['Longitude', 'Latitude'])
        df = df.drop_duplicates(subset=['ID', 'Longitude', 'Latitude'])
        
        print(f"Parsed {len(df)} valid event records\n")
        
        return df
    
    def get_comprehensive_dataset(self, years_back=5):
        """
        Fetch comprehensive dataset for multiple years
        
        Parameters:
        -----------
        years_back : int
            Number of years to fetch data for (default: 5)
        """
        print("="*70)
        print(f"FETCHING COMPREHENSIVE DATASET ({years_back} years)")
        print("="*70 + "\n")
        
        all_events = []
        
        # Calculate date ranges
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years_back*365)
        
        print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n")
        
        # Fetch in chunks (1 year at a time to avoid API limits)
        for year in range(years_back):
            chunk_end = end_date - timedelta(days=year*365)
            chunk_start = chunk_end - timedelta(days=365)
            
            print(f"Fetching year {chunk_start.year}...")
            
            events = self.fetch_events(
                start_date=chunk_start.strftime('%Y-%m-%d'),
                end_date=chunk_end.strftime('%Y-%m-%d'),
                status='all'
            )
            
            if events:
                all_events.extend(events)
                print(f"  Retrieved {len(events)} events for {chunk_start.year}")
            
            # Be nice to the API
            time.sleep(1)
        
        print(f"\nTotal events retrieved: {len(all_events)}")
        
        # Parse all events
        df = self.parse_events(all_events)
        
        return df
    
    def save_dataset(self, df, filename='eonet_data.csv'):
        """Save dataset to CSV"""
        df.to_csv(filename, index=False)
        print(f"\n{'='*70}")
        print(f"Dataset saved to: {filename}")
        print(f"{'='*70}")
        
        # Print summary
        print(f"\nDataset Summary:")
        print(f"  Total Events: {len(df):,}")
        print(f"  Date Range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"  Years: {df['Year'].nunique()}")
        print(f"  Categories: {df['Category_title'].nunique()}")
        
        print(f"\nTop 5 Categories:")
        for cat, count in df['Category_title'].value_counts().head(5).items():
            print(f"  {cat}: {count:,} ({count/len(df)*100:.1f}%)")
        
        print(f"\nEvents by Year:")
        for year, count in df['Year'].value_counts().sort_index().items():
            print(f"  {year}: {count:,}")


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("NASA EONET DATA FETCHER")
    print("="*70 + "\n")
    
    fetcher = EONETDataFetcher()
    
    # Show available categories
    categories = fetcher.get_categories()
    
    print("\n" + "="*70)
    print("FETCH OPTIONS")
    print("="*70)
    print("\n1. Last 365 days (recommended for testing)")
    print("2. Last 5 years (comprehensive dataset)")
    print("3. Custom date range")
    print("4. All available data")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        # Last 365 days
        events = fetcher.fetch_events(days=365)
        if events:
            df = fetcher.parse_events(events)
            fetcher.save_dataset(df)
    
    elif choice == '2':
        # Last 5 years
        df = fetcher.get_comprehensive_dataset(years_back=5)
        fetcher.save_dataset(df)
    
    elif choice == '3':
        # Custom date range
        start = input("Enter start date (YYYY-MM-DD): ").strip()
        end = input("Enter end date (YYYY-MM-DD): ").strip()
        
        events = fetcher.fetch_events(start_date=start, end_date=end)
        if events:
            df = fetcher.parse_events(events)
            fetcher.save_dataset(df)
    
    elif choice == '4':
        # All available data (no date filter)
        events = fetcher.fetch_events(status='all')
        if events:
            df = fetcher.parse_events(events)
            fetcher.save_dataset(df)
    
    else:
        print("Invalid choice. Fetching last 365 days by default...")
        events = fetcher.fetch_events(days=365)
        if events:
            df = fetcher.parse_events(events)
            fetcher.save_dataset(df)
    
    print("\n" + "="*70)
    print("DATA FETCH COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Review eonet_data.csv")
    print("  2. Run: python 01_data_loading.py")
    print("  3. Continue with analysis pipeline")
    print("\n")


if __name__ == "__main__":
    main()