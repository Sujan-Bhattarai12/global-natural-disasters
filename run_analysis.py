"""
NASA EONET Natural Events Analysis - Main Runner
Execute all analysis scripts in sequence
"""

import subprocess
import sys
import time

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print("\n" + "="*70)
    print(f"RUNNING: {description}")
    print("="*70)
    
    try:
        start_time = time.time()
        result = subprocess.run([sys.executable, script_name], 
                              check=True, 
                              capture_output=True, 
                              text=True)
        
        print(result.stdout)
        if result.stderr:
            print("WARNINGS/ERRORS:")
            print(result.stderr)
        
        elapsed = time.time() - start_time
        print(f"\n✓ Completed in {elapsed:.2f} seconds")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error running {script_name}:")
        print(e.stdout)
        print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"\n✗ Script not found: {script_name}")
        return False

def main():
    """Main execution pipeline"""
    print("\n" + "="*70)
    print("NASA EONET NATURAL EVENTS - COMPLETE ANALYSIS PIPELINE")
    print("="*70)
    print("\nThis pipeline will:")
    print("  1. Load and clean the data")
    print("  2. Perform exploratory data analysis")
    print("  3. Create geospatial visualizations")
    print("  4. Run advanced spatial analysis")
    print("\nNote: Make sure 'eonet_data.csv' is in the current directory")
    print("="*70)
    
    input("\nPress Enter to start the analysis pipeline...")
    
    # Pipeline steps
    steps = [
        ('01_data_loading.py', 'Data Loading and Cleaning'),
        ('02_exploratory_analysis.py', 'Exploratory Data Analysis'),
        ('03_geospatial_visualization.py', 'Geospatial Visualization'),
        ('04_advanced_analysis.py', 'Advanced Spatial Analysis')
    ]
    
    results = []
    total_start = time.time()
    
    for script, description in steps:
        success = run_script(script, description)
        results.append((description, success))
        
        if not success:
            print("\n⚠ WARNING: Script failed. Continuing with next step...")
        
        time.sleep(1)  # Brief pause between scripts
    
    # Final summary
    total_time = time.time() - total_start
    
    print("\n\n" + "="*70)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*70)
    
    for description, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {description}")
    
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    
    successful = sum(1 for _, success in results if success)
    print(f"\nCompleted {successful}/{len(steps)} steps successfully")
    
    if successful == len(steps):
        print("\n🎉 All analyses completed successfully!")
        print("\nOutput directories:")
        print("  • analysis_outputs/ - EDA visualizations")
        print("  • geospatial_outputs/ - Interactive maps and visualizations")
        print("  • advanced_analysis/ - Advanced spatial analysis results")
        print("\nOpen the HTML files in your browser for interactive exploration!")
    else:
        print("\n⚠ Some steps failed. Check the output above for details.")
    
    print("="*70)

if __name__ == "__main__":
    main()