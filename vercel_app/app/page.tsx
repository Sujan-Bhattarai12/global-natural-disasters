'use client';

import { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function TabNavigation({ activeTab, setActiveTab, tabs }: any) {
  return (
    <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
      {tabs.map((tab: string) => (
        <button key={tab} onClick={() => setActiveTab(tab)} className={`px-4 py-2 rounded-lg whitespace-nowrap transition-all ${activeTab === tab ? 'bg-blue-500 text-white shadow-lg' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>{tab}</button>
      ))}
    </div>
  );
}
// FINAL Interactive Hotspot Map with COUNTRY LABELS and CONTINENT OUTLINES!

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

  const topHotspots = filteredHotspots.slice(0, 5);

  return (
    <div className="space-y-6">
      {/* Map Section */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-blue-500/20 shadow-xl">
        <div className="flex items-center justify-between mb-4 flex-wrap gap-4">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center">
              <span className="mr-2">🗺️</span>
              Global Event Hotspots
            </h2>
            <p className="text-slate-400 text-sm mt-1">
              {filteredHotspots.length} hotspots • {filteredHotspots.reduce((sum, h) => sum + h.count, 0).toLocaleString()} total events
            </p>
          </div>
          <div className="flex gap-2 flex-wrap">
            <button 
              onClick={() => setSelectedCategory('all')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
                selectedCategory === 'all' ? 'bg-blue-500 text-white shadow-lg' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              All ({hotspots.length})
            </button>
            {['Storm', 'Wildfire', 'Volcano'].map(cat => {
              const count = hotspots.filter(h => h.primary_category.includes(cat)).length;
              return (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
                    selectedCategory === cat ? 'bg-blue-500 text-white shadow-lg' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  {cat} ({count})
                </button>
              );
            })}
          </div>
        </div>

        {/* Map Container with World Map, Outlines, and Labels */}
        <div className="relative bg-slate-900 rounded-lg overflow-hidden border-2 border-slate-700" style={{ height: '700px' }}>
          {/* SVG World Map with CLEAR CONTINENT OUTLINES */}
          <svg
            viewBox="0 0 1000 500"
            className="absolute inset-0 w-full h-full"
            preserveAspectRatio="xMidYMid slice"
          >
            <defs>
              <filter id="glow">
                <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                <feMerge>
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>

            {/* Ocean background */}
            <rect fill="#0f172a" width="1000" height="500"/>

            {/* Continents with CLEAR OUTLINES */}
            <g opacity="0.3">
              {/* North America */}
              <path 
                d="M 80,100 L 150,75 L 200,85 L 240,95 L 260,130 L 250,170 L 220,190 L 200,200 L 180,210 L 150,200 L 120,180 L 100,150 L 85,120 Z" 
                fill="#475569" 
                stroke="#94a3b8" 
                strokeWidth="2"
              />
              {/* Central America */}
              <path 
                d="M 180,210 L 200,200 L 210,220 L 205,235 L 190,240 L 180,230 Z" 
                fill="#475569" 
                stroke="#94a3b8" 
                strokeWidth="2"
              />
              {/* South America */}
              <path 
                d="M 190,240 L 220,235 L 240,255 L 250,295 L 245,330 L 230,360 L 210,370 L 190,365 L 175,340 L 170,300 L 175,260 Z" 
                fill="#475569" 
                stroke="#94a3b8" 
                strokeWidth="2"
              />
              {/* Europe */}
              <path 
                d="M 470,90 L 510,80 L 545,85 L 560,100 L 565,125 L 555,145 L 535,150 L 510,145 L 485,130 L 475,110 Z" 
                fill="#475569" 
                stroke="#94a3b8" 
                strokeWidth="2"
              />
              {/* Africa */}
              <path 
                d="M 490,160 L 520,155 L 555,165 L 580,190 L 595,240 L 590,290 L 570,330 L 540,345 L 510,340 L 485,310 L 475,270 L 478,220 L 485,180 Z" 
                fill="#475569" 
                stroke="#94a3b8" 
                strokeWidth="2"
              />
              {/* Asia */}
              <path 
                d="M 565,75 L 630,70 L 720,75 L 800,85 L 850,110 L 870,145 L 860,175 L 820,190 L 760,195 L 700,185 L 650,165 L 610,140 L 580,110 Z" 
                fill="#475569" 
                stroke="#94a3b8" 
                strokeWidth="2"
              />
              {/* Southeast Asia */}
              <path 
                d="M 700,195 L 750,200 L 780,220 L 785,245 L 770,260 L 740,265 L 715,250 L 705,225 Z" 
                fill="#475569" 
                stroke="#94a3b8" 
                strokeWidth="2"
              />
              {/* Australia */}
              <path 
                d="M 740,310 L 790,305 L 835,315 L 860,340 L 865,370 L 850,395 L 815,405 L 770,405 L 740,385 L 728,355 L 730,330 Z" 
                fill="#475569" 
                stroke="#94a3b8" 
                strokeWidth="2"
              />
            </g>

            {/* Grid lines */}
            <g stroke="#475569" strokeWidth="0.5" opacity="0.2">
              {[...Array(9)].map((_, i) => (
                <line key={`h${i}`} x1="0" y1={i * 500/8} x2="1000" y2={i * 500/8} />
              ))}
              {[...Array(17)].map((_, i) => (
                <line key={`v${i}`} x1={i * 1000/16} y1="0" x2={i * 1000/16} y2="500" />
              ))}
            </g>

            {/* Country Labels */}
            <g fill="#94a3b8" fontSize="11" fontWeight="600" opacity="0.7" fontFamily="system-ui">
              {/* North America */}
              <text x="120" y="110">USA</text>
              <text x="90" y="85">CANADA</text>
              <text x="185" y="215">MEXICO</text>
              
              {/* South America */}
              <text x="200" y="280">BRAZIL</text>
              <text x="175" y="330">ARGENTINA</text>
              
              {/* Europe */}
              <text x="485" y="120">EUROPE</text>
              <text x="510" y="105">UK</text>
              
              {/* Africa */}
              <text x="515" y="240">AFRICA</text>
              
              {/* Asia */}
              <text x="625" y="120">RUSSIA</text>
              <text x="730" y="115">CHINA</text>
              <text x="795" y="160">JAPAN</text>
              <text x="720" y="235">INDIA</text>
              
              {/* Australia */}
              <text x="780" y="360">AUSTRALIA</text>
              
              {/* Oceans */}
              <text x="350" y="250" opacity="0.3" fontSize="14" fontStyle="italic">ATLANTIC</text>
              <text x="650" y="400" opacity="0.3" fontSize="14" fontStyle="italic">PACIFIC</text>
            </g>
          </svg>

          {/* Coordinate labels */}
          <div className="absolute top-3 left-3 right-3 flex justify-between text-xs text-slate-400 font-mono font-semibold">
            <span>180°W</span>
            <span>90°W</span>
            <span>0°</span>
            <span>90°E</span>
            <span>180°E</span>
          </div>
          <div className="absolute top-3 bottom-3 left-3 flex flex-col justify-between text-xs text-slate-400 font-mono font-semibold">
            <span>90°N</span>
            <span>45°N</span>
            <span>0°</span>
            <span>45°S</span>
            <span>90°S</span>
          </div>

          {/* Hotspot markers */}
          <div className="absolute inset-0">
            {filteredHotspots.map((hotspot, idx) => {
              const x = ((hotspot.longitude + 180) / 360) * 100;
              const y = ((90 - hotspot.latitude) / 180) * 100;
              const size = Math.min(Math.sqrt(hotspot.count) * 2, 40);
              const color = categoryColors[hotspot.primary_category]?.hex || '#64748b';

              return (
                <div
                  key={idx}
                  className="absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all hover:z-50 group"
                  style={{ left: `${x}%`, top: `${y}%` }}
                  onMouseEnter={() => setHoveredRegion(hotspot.title)}
                  onMouseLeave={() => setHoveredRegion(null)}
                >
                  {/* Animated pulse ring */}
                  <div 
                    className="absolute inset-0 rounded-full animate-ping opacity-30"
                    style={{
                      width: `${size * 2}px`,
                      height: `${size * 2}px`,
                      backgroundColor: color,
                      transform: 'translate(-50%, -50%)',
                      left: '50%',
                      top: '50%',
                      animationDuration: '2s'
                    }}
                  />
                  
                  {/* Main hotspot dot */}
                  <div
                    className="rounded-full opacity-75 group-hover:opacity-100 group-hover:scale-125 transition-all relative z-10 border-2 border-white/40"
                    style={{
                      width: `${size}px`,
                      height: `${size}px`,
                      backgroundColor: color,
                      boxShadow: `0 0 ${size}px ${color}, 0 0 ${size * 2}px ${color}`,
                    }}
                  />

                  {/* Tooltip on hover */}
                  {hoveredRegion === hotspot.title && (
                    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-4 min-w-[220px] z-50">
                      <div className="bg-slate-900/98 backdrop-blur-sm border-2 border-blue-500/60 rounded-xl p-4 shadow-2xl">
                        <div className="text-white font-bold text-lg mb-2">{hotspot.title}</div>
                        <div className="flex items-center gap-2 mb-3">
                          <div 
                            className="w-4 h-4 rounded-full shadow-lg" 
                            style={{ backgroundColor: color, boxShadow: `0 0 10px ${color}` }}
                          />
                          <span className="text-slate-300 text-sm font-semibold">{hotspot.primary_category}</span>
                        </div>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between bg-slate-800/50 rounded px-3 py-2">
                            <span className="text-slate-400 text-xs">Events:</span>
                            <span className="text-blue-400 text-base font-bold">{hotspot.count.toLocaleString()}</span>
                          </div>
                          <div className="flex items-center justify-between bg-slate-800/50 rounded px-3 py-2">
                            <span className="text-slate-400 text-xs">Coordinates:</span>
                            <span className="text-slate-300 text-xs font-mono">
                              {hotspot.latitude.toFixed(2)}°, {hotspot.longitude.toFixed(2)}°
                            </span>
                          </div>
                        </div>
                        {/* Arrow */}
                        <div 
                          className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1"
                          style={{
                            width: 0,
                            height: 0,
                            borderLeft: '10px solid transparent',
                            borderRight: '10px solid transparent',
                            borderTop: '10px solid rgba(59, 130, 246, 0.6)'
                          }}
                        />
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Info overlay */}
          <div className="absolute top-16 left-4 bg-slate-900/95 backdrop-blur-sm rounded-lg px-4 py-3 border-2 border-blue-500/40 shadow-xl">
            <p className="text-white text-sm font-bold mb-1">
              🎯 {filteredHotspots.length} Active Hotspots
            </p>
            <p className="text-slate-400 text-xs">
              {selectedCategory === 'all' ? 'All Categories' : `${selectedCategory} Events Only`}
            </p>
          </div>
        </div>

        {/* Category Legend */}
        <div className="mt-4 grid grid-cols-2 md:grid-cols-5 gap-3">
          {Object.entries(categoryColors).map(([cat, style]) => (
            <div key={cat} className="flex items-center gap-2 bg-slate-900/50 rounded-lg px-3 py-2 border border-slate-700/50">
              <div 
                className={`w-4 h-4 rounded-full ${style.bg}`}
                style={{ boxShadow: `0 0 8px ${style.hex}` }}
              />
              <span className="text-slate-300 text-sm">{cat}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Top 5 Hotspots Data Cards */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-blue-500/20 shadow-xl">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center">
          <span className="mr-2">🔥</span>
          Top 5 Hotspots {selectedCategory !== 'all' && `(${selectedCategory})`}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {topHotspots.map((hotspot, idx) => {
            const color = categoryColors[hotspot.primary_category]?.hex || '#64748b';
            return (
              <div 
                key={idx}
                className="bg-slate-900/70 rounded-lg p-4 border border-slate-700 hover:border-blue-500/50 transition-all"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl font-bold text-slate-500">#{idx + 1}</span>
                  <div 
                    className="w-6 h-6 rounded-full"
                    style={{ 
                      backgroundColor: color,
                      boxShadow: `0 0 12px ${color}`
                    }}
                  />
                </div>
                <h4 className="text-white font-semibold text-sm mb-2 line-clamp-2">{hotspot.title}</h4>
                <div className="space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-xs">Events:</span>
                    <span className="text-blue-400 font-bold text-sm">{hotspot.count.toLocaleString()}</span>
                  </div>
                  <div className="text-slate-500 text-xs">
                    📍 {hotspot.latitude.toFixed(1)}°, {hotspot.longitude.toFixed(1)}°
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Statistics Bar */}
      <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-xl p-6 border border-blue-500/20">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="text-center">
            <p className="text-3xl font-bold text-blue-400 mb-1">
              {filteredHotspots.reduce((sum, h) => sum + h.count, 0).toLocaleString()}
            </p>
            <p className="text-sm text-slate-400">Total Events</p>
          </div>
          <div className="text-center">
            <p className="text-3xl font-bold text-green-400 mb-1">
              {filteredHotspots.length}
            </p>
            <p className="text-sm text-slate-400">Active Hotspots</p>
          </div>
          <div className="text-center">
            <p className="text-3xl font-bold text-orange-400 mb-1">
              {filteredHotspots.length > 0 
                ? Math.round(filteredHotspots.reduce((sum, h) => sum + h.count, 0) / filteredHotspots.length).toLocaleString()
                : 0}
            </p>
            <p className="text-sm text-slate-400">Avg per Hotspot</p>
          </div>
          <div className="text-center">
            <p className="text-3xl font-bold text-purple-400 mb-1">
              {filteredHotspots.length > 0 
                ? Math.max(...filteredHotspots.map(h => h.count)).toLocaleString()
                : 0}
            </p>
            <p className="text-sm text-slate-400">Max Intensity</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Globe3D({ globeUrl }: { globeUrl: string | null }) {
  const [isFullscreen, setIsFullscreen] = useState(false);
  if (!globeUrl) return <div className="bg-gradient-to-br from-blue-900/30 to-purple-900/30 rounded-xl p-12 border border-blue-500/20"><div className="text-center text-slate-400"><div className="text-6xl mb-4">🌍</div><p className="text-xl">3D Globe not found</p></div></div>;
  return (<><div className="bg-gradient-to-br from-slate-800/50 to-blue-900/30 rounded-xl overflow-hidden border border-blue-500/20 shadow-2xl"><div className="bg-gradient-to-r from-blue-900/50 to-purple-900/50 px-6 py-4 border-b border-blue-500/20"><div className="flex items-center justify-between"><div><h2 className="text-2xl font-bold text-white flex items-center"><span className="mr-3">🌍</span>3D Global Natural Events Distribution</h2></div><button onClick={() => setIsFullscreen(true)} className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold transition-all">⛶ Fullscreen</button></div></div><iframe src={globeUrl} className="w-full h-[600px] border-0" title="3D Globe"/></div>{isFullscreen && (<div className="fixed inset-0 bg-slate-900 z-50 flex flex-col"><div className="bg-slate-800 border-b border-blue-500/20 p-4 flex justify-between"><h2 className="text-white text-xl font-bold">🌍 3D Globe</h2><button className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-semibold" onClick={() => setIsFullscreen(false)}>✕ Close</button></div><iframe src={globeUrl} className="flex-1 w-full border-0"/></div>)}</>);
}

function AnalysisImageGallery({ images }: { images: any }) {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const filteredImages = Object.entries(images || {}).filter(([filename]) => !['3d_density_surface', '3d_spacetime_scatter'].some(bad => filename.toLowerCase().includes(bad)));
  if (filteredImages.length === 0) return <div className="text-center text-slate-400 py-12"><p>📊 No images found</p></div>;
  return (<div><p className="text-slate-300 mb-4">📊 {filteredImages.length} visualizations</p><div className="grid grid-cols-1 lg:grid-cols-2 gap-6">{filteredImages.map(([filename, info]: [string, any]) => (<div key={filename} className="bg-slate-800/50 rounded-xl overflow-hidden border border-slate-700 hover:border-blue-500 transition-all cursor-pointer shadow-xl" onClick={() => setSelectedImage(info.path)}><div className="relative bg-slate-900 p-4"><img src={info.path} alt={info.title} className="w-full h-auto object-contain rounded" style={{maxHeight:'500px'}}/></div><div className="p-4 bg-slate-800"><h3 className="text-white font-semibold text-lg">{info.title}</h3></div></div>))}</div>{selectedImage && (<div className="fixed inset-0 bg-black/95 z-50 flex items-center justify-center p-4" onClick={() => setSelectedImage(null)}><button className="absolute top-4 right-4 bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-semibold" onClick={(e) => {e.stopPropagation(); setSelectedImage(null);}}>✕</button><img src={selectedImage} alt="Full" className="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl"/></div>)}</div>);
}

function InteractiveMapsGallery({ maps }: { maps: any }) {
  const [selectedMap, setSelectedMap] = useState<string | null>(null);
  if (!maps || Object.keys(maps).length === 0) return <div className="text-center text-slate-400 py-12"><p>🗺️ No maps</p></div>;
  const mapEntries = Object.entries(maps).filter(([filename]) => !filename.includes('3d_globe_interactive'));
  return (<div><p className="text-slate-300 mb-4">🗺️ {mapEntries.length} interactive maps</p><div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">{mapEntries.map(([filename, info]: [string, any]) => (<div key={filename} className="bg-slate-800/50 rounded-xl border border-slate-700 hover:border-blue-500 transition-all cursor-pointer shadow-xl p-6 text-center" onClick={() => setSelectedMap(info.path)}><div className="text-6xl mb-4">🗺️</div><h3 className="text-white font-semibold text-lg mb-2">{info.title}</h3></div>))}</div>{selectedMap && (<div className="fixed inset-0 bg-slate-900 z-50 flex flex-col"><div className="bg-slate-800 border-b p-4 flex justify-between"><h2 className="text-white text-xl font-bold">Map</h2><button className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-semibold" onClick={() => setSelectedMap(null)}>✕</button></div><iframe src={selectedMap} className="flex-1 w-full border-0"/></div>)}</div>);
}

export default function Dashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('Overview');
  const tabs = ['Overview', 'Interactive Map', 'Python Analysis', 'Interactive Maps', 'Temporal Patterns'];

  useEffect(() => {
    fetch('/analysis_data.json').then(res => {if(!res.ok) throw new Error('Run python script'); return res.json();}).then(d => {setData(d); setLoading(false);}).catch(e => {setError(e.message); setLoading(false);});
  }, []);

  if (loading) return <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center"><div className="text-center"><div className="text-6xl mb-4 animate-bounce">🌍</div><div className="text-white text-2xl font-bold">Loading...</div></div></div>;
  if (error) return <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4"><div className="bg-red-900/30 border border-red-500/50 rounded-xl p-8"><h2 className="text-white text-2xl font-bold mb-4">Data Not Found</h2><p className="text-slate-300">{error}</p></div></div>;

  const { metadata, executive_metrics, hotspots, seasonal_patterns, yearly_trends, available_visualizations } = data;
  const globeUrl = available_visualizations?.interactive_maps?.['3d_globe_interactive.html']?.path || null;
  const seasonalData = seasonal_patterns.map((s: any) => ({month: s.month_name, total: s.total_events, storms: s.storms, wildfires: s.wildfires, volcanoes: s.volcanoes || 0, floods: s.floods || 0, ice: s.ice || 0}));

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <header className="bg-slate-900/80 backdrop-blur-sm border-b border-blue-500/20 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center"><span className="text-2xl">🌍</span></div>
              <div><h1 className="text-2xl font-bold text-white">NASA EONET Dashboard</h1><p className="text-sm text-blue-300">Global Natural Events Analysis</p></div>
            </div>
            <div className="text-right"><p className="text-sm text-blue-300 font-semibold">{metadata.date_range.start} → {metadata.date_range.end}</p><p className="text-xs text-slate-400">{metadata.total_observations.toLocaleString()} Observations</p></div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-blue-500/20 shadow-xl"><div className="flex items-center justify-between mb-2"><span className="text-3xl">📊</span><span className="text-xs text-green-400 font-semibold">{metadata.years_tracked} Years</span></div><p className="text-3xl font-bold text-white mb-1">{metadata.total_observations.toLocaleString()}</p><p className="text-sm text-slate-400">Total Observations</p></div>
          <div className="bg-gradient-to-br from-blue-900/30 to-slate-900 rounded-xl p-6 border border-blue-500/20 shadow-xl"><div className="flex items-center justify-between mb-2"><span className="text-3xl">🎯</span><span className="text-xs text-blue-400 font-semibold">Unique</span></div><p className="text-3xl font-bold text-white mb-1">{metadata.unique_events.toLocaleString()}</p><p className="text-sm text-slate-400">Natural Events</p></div>
          <div className="bg-gradient-to-br from-red-900/30 to-slate-900 rounded-xl p-6 border border-red-500/20 shadow-xl"><div className="flex items-center justify-between mb-2"><span className="text-3xl">🔥</span><span className="text-xs text-red-400 font-semibold">{((executive_metrics.category_counts['Wildfires'] || 0) / metadata.total_observations * 100).toFixed(1)}%</span></div><p className="text-3xl font-bold text-white mb-1">{(executive_metrics.category_counts['Wildfires'] || 0).toLocaleString()}</p><p className="text-sm text-slate-400">Wildfires</p></div>
          <div className="bg-gradient-to-br from-orange-900/30 to-slate-900 rounded-xl p-6 border border-orange-500/20 shadow-xl"><div className="flex items-center justify-between mb-2"><span className="text-3xl">⛈️</span><span className="text-xs text-orange-400 font-semibold">{((executive_metrics.category_counts['Severe Storms'] || 0) / metadata.total_observations * 100).toFixed(1)}%</span></div><p className="text-3xl font-bold text-white mb-1">{(executive_metrics.category_counts['Severe Storms'] || 0).toLocaleString()}</p><p className="text-sm text-slate-400">Severe Storms</p></div>
        </div>

        <TabNavigation activeTab={activeTab} setActiveTab={setActiveTab} tabs={tabs} />

        <div className="mb-8">
          {activeTab === 'Overview' && (
            <div className="space-y-6">
              <div className="bg-slate-800/50 rounded-xl p-6 border border-blue-500/20 shadow-xl">
                <h2 className="text-2xl font-bold text-white mb-6 flex items-center"><span className="mr-2">📅</span>Seasonal Patterns - All Disaster Types</h2>
                <ResponsiveContainer width="100%" height={500}>
                  <LineChart data={seasonalData} margin={{top:20,right:30,left:20,bottom:20}}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155"/>
                    <XAxis dataKey="month" stroke="#94a3b8" style={{fontSize:'14px',fontWeight:600}}/>
                    <YAxis stroke="#94a3b8" style={{fontSize:'14px',fontWeight:600}} label={{value:'Events',angle:-90,position:'insideLeft',style:{fill:'#94a3b8',fontSize:'14px'}}}/>
                    <Tooltip contentStyle={{backgroundColor:'#1e293b',border:'1px solid #3b82f6',borderRadius:'8px',padding:'12px'}}/>
                    <Legend wrapperStyle={{paddingTop:'20px'}}/>
                    <Line type="monotone" dataKey="total" stroke="#3b82f6" strokeWidth={3} name="Total" dot={{r:5}}/>
                    <Line type="monotone" dataKey="storms" stroke="#8b5cf6" strokeWidth={2} name="Storms" dot={{r:4}}/>
                    <Line type="monotone" dataKey="wildfires" stroke="#ef4444" strokeWidth={2} name="Wildfires" dot={{r:4}}/>
                    <Line type="monotone" dataKey="volcanoes" stroke="#f97316" strokeWidth={2} name="Volcanoes" dot={{r:4}}/>
                    <Line type="monotone" dataKey="floods" stroke="#06b6d4" strokeWidth={2} name="Floods" dot={{r:4}}/>
                    <Line type="monotone" dataKey="ice" stroke="#a855f7" strokeWidth={2} name="Ice" dot={{r:4}}/>
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <Globe3D globeUrl={globeUrl}/>
            </div>
          )}
          {activeTab === 'Interactive Map' && <GeospatialHotspots hotspots={hotspots}/>}
          {activeTab === 'Python Analysis' && (<div className="bg-slate-800/50 rounded-xl p-6 border border-blue-500/20 shadow-xl"><h2 className="text-2xl font-bold text-white mb-6">🔬 Python Analysis</h2><AnalysisImageGallery images={available_visualizations?.static_images||{}}/></div>)}
          {activeTab === 'Interactive Maps' && (<div className="bg-slate-800/50 rounded-xl p-6 border border-blue-500/20 shadow-xl"><h2 className="text-2xl font-bold text-white mb-6">🗺️ Interactive Maps</h2><InteractiveMapsGallery maps={available_visualizations?.interactive_maps||{}}/></div>)}
          {activeTab === 'Temporal Patterns' && (
            <div className="bg-slate-800/50 rounded-xl p-6 border border-blue-500/20 shadow-xl">
              <h2 className="text-2xl font-bold text-white mb-6">📈 Yearly Trends</h2>
              <ResponsiveContainer width="100%" height={500}>
                <BarChart data={yearly_trends} margin={{top:20,right:30,left:20,bottom:20}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155"/>
                  <XAxis dataKey="year" stroke="#94a3b8" style={{fontSize:'14px',fontWeight:600}}/>
                  <YAxis stroke="#94a3b8" style={{fontSize:'14px',fontWeight:600}}/>
                  <Tooltip contentStyle={{backgroundColor:'#1e293b',border:'1px solid #3b82f6',borderRadius:'8px'}}/>
                  <Legend/>
                  <Bar dataKey="total" fill="#3b82f6" name="Total" radius={[8,8,0,0]}/>
                  <Bar dataKey="storms" fill="#8b5cf6" name="Storms" radius={[8,8,0,0]}/>
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}