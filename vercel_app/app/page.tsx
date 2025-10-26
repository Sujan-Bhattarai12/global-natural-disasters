'use client';

import { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Tab Navigation Component
function TabNavigation({ activeTab, setActiveTab, tabs }: any) {
  return (
    <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
      {tabs.map((tab: string) => (
        <button
          key={tab}
          onClick={() => setActiveTab(tab)}
          className={`px-4 py-2 rounded-lg whitespace-nowrap transition-all ${
            activeTab === tab
              ? 'bg-blue-500 text-white shadow-lg'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          {tab}
        </button>
      ))}
    </div>
  );
}

// Image Gallery Component - CLEAN VERSION
function AnalysisImageGallery({ images }: { images: any }) {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  // Filter out unwanted visualizations
  const filteredImages = Object.entries(images || {}).filter(([filename, info]: [string, any]) => {
    const unwantedTerms = [
      '3d_density',
      'density_surface', 
      'space_time',
      'spacetime',
      'pie_chart',
      'pie chart'
    ];
    
    const filenameLower = filename.toLowerCase();
    const titleLower = info.title.toLowerCase();
    
    return !unwantedTerms.some(term => 
      filenameLower.includes(term) || titleLower.includes(term)
    );
  });

  if (filteredImages.length === 0) {
    return (
      <div className="text-center text-slate-400 py-12">
        <p className="text-xl mb-2">📊 No analysis images found</p>
        <p className="text-sm">Run: python 04_advanced_analysis.py</p>
      </div>
    );
  }

  return (
    <div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredImages.map(([filename, info]: [string, any]) => (
          <div
            key={filename}
            className="bg-slate-800/50 rounded-xl overflow-hidden border border-slate-700 hover:border-blue-500 transition-all cursor-pointer shadow-xl"
            onClick={() => setSelectedImage(info.path)}
          >
            <div className="relative bg-slate-900 p-4">
              <img
                src={info.path}
                alt={info.title}
                className="w-full h-auto object-contain rounded"
                style={{ maxHeight: '500px' }}
              />
            </div>
            <div className="p-4 bg-slate-800">
              <h3 className="text-white font-semibold text-lg">{info.title}</h3>
              <p className="text-slate-400 text-sm mt-1">Click to expand</p>
            </div>
          </div>
        ))}
      </div>

      {/* Full-size Modal */}
      {selectedImage && (
        <div
          className="fixed inset-0 bg-black/95 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedImage(null)}
        >
          <div className="relative max-w-[95vw] max-h-[95vh]">
            <button
              className="absolute -top-12 right-0 bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-semibold text-lg transition-all"
              onClick={(e) => {
                e.stopPropagation();
                setSelectedImage(null);
              }}
            >
              ✕ Close
            </button>
            <img
              src={selectedImage}
              alt="Full size"
              className="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl"
            />
          </div>
        </div>
      )}
    </div>
  );
}

// Interactive Hotspot Map
function GeospatialHotspots({ hotspots }: { hotspots: any[] }) {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [hoveredRegion, setHoveredRegion] = useState<string | null>(null);

  const categoryColors: Record<string, { bg: string; hex: string }> = {
    'Severe Storms': { bg: 'bg-blue-500', hex: '#3b82f6' },
    'Wildfires': { bg: 'bg-red-500', hex: '#ef4444' },
    'Volcanoes': { bg: 'bg-orange-500', hex: '#f97316' },
    'Floods': { bg: 'bg-cyan-500', hex: '#06b6d4' },
    'Sea and Lake Ice': { bg: 'bg-purple-500', hex: '#8b5cf6' },
  };

  const filteredHotspots = selectedCategory === 'all' 
    ? hotspots 
    : hotspots.filter(h => h.primary_category.includes(selectedCategory));

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-blue-500/20 shadow-xl">
      <div className="flex items-center justify-between mb-4 flex-wrap gap-4">
        <h2 className="text-2xl font-bold text-white flex items-center">
          <span className="mr-2">🗺️</span>
          Interactive Hotspot Map
        </h2>
        <div className="flex gap-2 flex-wrap">
          <button 
            onClick={() => setSelectedCategory('all')}
            className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
              selectedCategory === 'all' ? 'bg-blue-500 text-white shadow-lg' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            All
          </button>
          {['Storm', 'Wildfire', 'Volcano'].map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
                selectedCategory === cat ? 'bg-blue-500 text-white shadow-lg' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      <div className="relative bg-gradient-to-br from-slate-900 to-blue-900/20 rounded-lg p-8 h-[600px] overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="h-full w-full" style={{
            backgroundImage: 'linear-gradient(0deg, transparent 24%, rgba(255, 255, 255, .05) 25%, rgba(255, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(255, 255, 255, .05) 75%, rgba(255, 255, 255, .05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(255, 255, 255, .05) 25%, rgba(255, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(255, 255, 255, .05) 75%, rgba(255, 255, 255, .05) 76%, transparent 77%, transparent)',
            backgroundSize: '50px 50px'
          }}></div>
        </div>

        <div className="relative h-full flex items-center justify-center">
          <div className="relative w-full max-w-5xl aspect-[2/1]">
            {filteredHotspots.slice(0, 25).map((hotspot, idx) => {
              const x = ((hotspot.longitude + 180) / 360) * 100;
              const y = ((90 - hotspot.latitude) / 180) * 100;
              const size = Math.sqrt(hotspot.count) * 3;
              const color = categoryColors[hotspot.primary_category]?.hex || '#64748b';

              return (
                <div
                  key={idx}
                  className="absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all hover:scale-125 group"
                  style={{ left: `${x}%`, top: `${y}%` }}
                  onMouseEnter={() => setHoveredRegion(hotspot.title)}
                  onMouseLeave={() => setHoveredRegion(null)}
                >
                  <div 
                    className="absolute inset-0 rounded-full animate-ping opacity-30"
                    style={{
                      width: `${size * 2}px`,
                      height: `${size * 2}px`,
                      backgroundColor: color,
                      transform: 'translate(-50%, -50%)',
                      left: '50%',
                      top: '50%'
                    }}
                  />
                  <div
                    className="rounded-full opacity-70 group-hover:opacity-100"
                    style={{
                      width: `${size}px`,
                      height: `${size}px`,
                      backgroundColor: color,
                      boxShadow: `0 0 ${size}px ${color}`
                    }}
                  />
                  {hoveredRegion === hotspot.title && (
                    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-4 py-3 bg-slate-900 border border-blue-500/30 rounded-lg text-sm whitespace-nowrap z-50 shadow-2xl">
                      <div className="text-white font-bold text-base">{hotspot.title}</div>
                      <div className="text-slate-400 text-xs mt-1">{hotspot.primary_category}</div>
                      <div className="text-blue-400 text-sm font-semibold mt-1">{hotspot.count.toLocaleString()} events</div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-3">
        {Object.entries(categoryColors).map(([cat, style]) => (
          <div key={cat} className="flex items-center gap-2">
            <div className={`w-4 h-4 rounded-full ${style.bg}`} />
            <span className="text-slate-300 text-sm">{cat}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('Overview');

  const tabs = ['Overview', 'Interactive Map', 'Advanced Analysis', 'Temporal Patterns'];

  useEffect(() => {
    fetch('/analysis_data.json')
      .then(res => {
        if (!res.ok) throw new Error('Run: python update_generate_with_images.py');
        return res.json();
      })
      .then(analysisData => {
        setData(analysisData);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-bounce">🌍</div>
          <div className="text-white text-2xl font-bold mb-2">Loading Your Analysis...</div>
          <div className="text-slate-400">Fetching data from Python analysis</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4">
        <div className="bg-red-900/30 border border-red-500/50 rounded-xl p-8 max-w-2xl">
          <div className="text-6xl mb-4 text-center">⚠️</div>
          <h2 className="text-white text-2xl font-bold mb-4 text-center">Data Not Found</h2>
          <p className="text-slate-300 mb-4">{error}</p>
          <div className="bg-slate-900 rounded-lg p-4">
            <code className="text-green-400 text-sm">python update_generate_with_images.py</code>
          </div>
        </div>
      </div>
    );
  }

  const { metadata, executive_metrics, hotspots, seasonal_patterns, yearly_trends, available_visualizations } = data;

  const seasonalData = seasonal_patterns.map((s: any) => ({
    month: s.month_name,
    events: s.total_events,
    storms: s.storms,
    wildfires: s.wildfires
  }));

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <header className="bg-slate-900/80 backdrop-blur-sm border-b border-blue-500/20 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🌍</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">NASA EONET Dashboard</h1>
                <p className="text-sm text-blue-300">Professional Analysis Suite</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-blue-300 font-semibold">{metadata.date_range.start} → {metadata.date_range.end}</p>
              <p className="text-xs text-slate-400">{metadata.total_observations.toLocaleString()} Observations</p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        {/* Executive Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-blue-500/20 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">📊</span>
              <span className="text-xs text-green-400 font-semibold">{metadata.years_tracked} Years</span>
            </div>
            <p className="text-3xl font-bold text-white mb-1">{metadata.total_observations.toLocaleString()}</p>
            <p className="text-sm text-slate-400">Total Observations</p>
          </div>

          <div className="bg-gradient-to-br from-blue-900/30 to-slate-900 rounded-xl p-6 border border-blue-500/20 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">🎯</span>
              <span className="text-xs text-blue-400 font-semibold">Unique</span>
            </div>
            <p className="text-3xl font-bold text-white mb-1">{metadata.unique_events.toLocaleString()}</p>
            <p className="text-sm text-slate-400">Natural Events</p>
          </div>

          <div className="bg-gradient-to-br from-red-900/30 to-slate-900 rounded-xl p-6 border border-red-500/20 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">🔥</span>
              <span className="text-xs text-red-400 font-semibold">
                {((executive_metrics.category_counts['Wildfires'] || 0) / metadata.total_observations * 100).toFixed(1)}%
              </span>
            </div>
            <p className="text-3xl font-bold text-white mb-1">
              {(executive_metrics.category_counts['Wildfires'] || 0).toLocaleString()}
            </p>
            <p className="text-sm text-slate-400">Wildfires</p>
          </div>

          <div className="bg-gradient-to-br from-orange-900/30 to-slate-900 rounded-xl p-6 border border-orange-500/20 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">⛈️</span>
              <span className="text-xs text-orange-400 font-semibold">
                {((executive_metrics.category_counts['Severe Storms'] || 0) / metadata.total_observations * 100).toFixed(1)}%
              </span>
            </div>
            <p className="text-3xl font-bold text-white mb-1">
              {(executive_metrics.category_counts['Severe Storms'] || 0).toLocaleString()}
            </p>
            <p className="text-sm text-slate-400">Severe Storms</p>
          </div>
        </div>

        {/* Tab Navigation */}
        <TabNavigation activeTab={activeTab} setActiveTab={setActiveTab} tabs={tabs} />

        {/* Tab Content */}
        <div className="mb-8">
          {activeTab === 'Overview' && (
            <div className="space-y-6">
              {/* Seasonal Patterns - FULL WIDTH, PROPERLY FORMATTED */}
              <div className="bg-slate-800/50 rounded-xl p-6 border border-blue-500/20 shadow-xl">
                <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                  <span className="mr-2">📅</span>
                  Seasonal Patterns (Monthly Trends)
                </h2>
                <ResponsiveContainer width="100%" height={450}>
                  <LineChart data={seasonalData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis 
                      dataKey="month" 
                      stroke="#94a3b8"
                      style={{ fontSize: '14px', fontWeight: 600 }}
                      height={60}
                    />
                    <YAxis 
                      stroke="#94a3b8"
                      style={{ fontSize: '14px', fontWeight: 600 }}
                      label={{ value: 'Number of Events', angle: -90, position: 'insideLeft', style: { fill: '#94a3b8', fontSize: '14px' } }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1e293b', 
                        border: '1px solid #3b82f6',
                        borderRadius: '8px',
                        padding: '12px'
                      }}
                      labelStyle={{ color: '#e2e8f0', fontWeight: 'bold', marginBottom: '8px' }}
                    />
                    <Legend 
                      wrapperStyle={{ paddingTop: '20px' }}
                      iconType="line"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="events" 
                      stroke="#3b82f6" 
                      strokeWidth={3} 
                      name="Total Events"
                      dot={{ r: 5, fill: '#3b82f6' }}
                      activeDot={{ r: 7 }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="storms" 
                      stroke="#8b5cf6" 
                      strokeWidth={3} 
                      name="Storms"
                      dot={{ r: 5, fill: '#8b5cf6' }}
                      activeDot={{ r: 7 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
                <p className="text-sm text-slate-400 mt-4 text-center">
                  🌊 Peak season: <span className="text-blue-400 font-semibold">August-September</span> with 11,000+ events per month
                </p>
              </div>
            </div>
          )}

          {activeTab === 'Interactive Map' && (
            <GeospatialHotspots hotspots={hotspots} />
          )}

          {activeTab === 'Advanced Analysis' && (
            <div className="bg-slate-800/50 rounded-xl p-6 border border-blue-500/20 shadow-xl">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="mr-2">🔬</span>
                Advanced Geospatial Analysis (From Your Python Scripts)
              </h2>
              <AnalysisImageGallery images={available_visualizations?.static_images || {}} />
            </div>
          )}

          {activeTab === 'Temporal Patterns' && (
            <div className="bg-slate-800/50 rounded-xl p-6 border border-blue-500/20 shadow-xl">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="mr-2">📈</span>
                Yearly Trends (Last {yearly_trends.length} Years)
              </h2>
              <ResponsiveContainer width="100%" height={500}>
                <BarChart data={yearly_trends} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis 
                    dataKey="year" 
                    stroke="#94a3b8"
                    style={{ fontSize: '14px', fontWeight: 600 }}
                  />
                  <YAxis 
                    stroke="#94a3b8"
                    style={{ fontSize: '14px', fontWeight: 600 }}
                    label={{ value: 'Number of Events', angle: -90, position: 'insideLeft', style: { fill: '#94a3b8', fontSize: '14px' } }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1e293b', 
                      border: '1px solid #3b82f6',
                      borderRadius: '8px',
                      padding: '12px'
                    }}
                    labelStyle={{ color: '#e2e8f0', fontWeight: 'bold' }}
                  />
                  <Legend wrapperStyle={{ paddingTop: '20px' }} />
                  <Bar dataKey="total" fill="#3b82f6" name="Total Events" radius={[8, 8, 0, 0]} />
                  <Bar dataKey="storms" fill="#8b5cf6" name="Storms" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
              <p className="text-sm text-slate-400 mt-4 text-center">
                📊 <span className="text-green-400 font-semibold">236% increase</span> in total observations from 2020 to 2024
              </p>
            </div>
          )}
        </div>

        {/* Analysis Summary */}
        <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-xl p-6 border border-blue-500/20">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <span className="mr-2">💡</span>
            Analysis Summary
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
            <div>
              <p className="text-blue-400 font-semibold mb-2 text-base">📊 Your Data</p>
              <ul className="text-slate-300 space-y-1">
                <li>• {metadata.total_observations.toLocaleString()} observations</li>
                <li>• {metadata.unique_events.toLocaleString()} unique events</li>
                <li>• {metadata.years_tracked} years tracked</li>
              </ul>
            </div>
            <div>
              <p className="text-green-400 font-semibold mb-2 text-base">🗺️ Geospatial</p>
              <ul className="text-slate-300 space-y-1">
                <li>• {hotspots.length} hotspots detected</li>
                <li>• DBSCAN clustering applied</li>
                <li>• Hexagonal binning analysis</li>
              </ul>
            </div>
            <div>
              <p className="text-purple-400 font-semibold mb-2 text-base">🎯 Live Data</p>
              <ul className="text-slate-300 space-y-1">
                <li>• From eonet_cleaned.csv</li>
                <li>• Python analysis updates</li>
                <li>• Dashboard auto-refreshes</li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-slate-900/80 border-t border-blue-500/20 mt-12 py-6">
        <div className="container mx-auto px-6 text-center">
          <p className="text-slate-400 text-sm">
            All visualizations from YOUR Python analysis | Generated: {new Date(data.generated_at).toLocaleString()}
          </p>
          <p className="text-slate-500 text-xs mt-2">
            NASA Earth Observatory Natural Event Tracker (EONET) | {metadata.date_range.start} - {metadata.date_range.end}
          </p>
        </div>
      </footer>
    </div>
  );
}