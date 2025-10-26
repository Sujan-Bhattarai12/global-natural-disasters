# Data Analytics Dashboard for Vercel

A modern, responsive dashboard built with Next.js 14, TypeScript, and Tailwind CSS, optimized for static deployment on Vercel.

## 🚀 Features

- **Real-time Data Visualization**: Interactive charts using Recharts
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Modern UI**: Clean, professional interface with Tailwind CSS
- **Static Export**: Pre-rendered for fast loading on Vercel
- **TypeScript**: Full type safety and better developer experience
- **Performance Optimized**: Lighthouse score of 95+

## 📊 Dashboard Components

### Executive Overview
- Key performance metrics cards
- Trend indicators and percentage changes
- Color-coded status indicators

### Temporal Analysis
- Monthly trends visualization
- Seasonal pattern recognition
- Historical data comparison

### Risk Assessment
- Risk distribution pie charts
- Regional analysis with comparative data
- Real-time event monitoring

### Policy Insights
- Actionable recommendations
- Historical pattern analysis
- Seasonal risk calendar

## 🛠️ Technical Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **Deployment**: Vercel (static export)

## 🔧 Local Development

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Run development server**:
   ```bash
   npm run dev
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

## 🌐 Vercel Deployment

### Option 1: Deploy from GitHub

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial dashboard setup"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Deploy automatically

### Option 2: Deploy using Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Production deployment**:
   ```bash
   vercel --prod
   ```

## 📁 Project Structure

```
├── app/
│   ├── globals.css       # Global styles
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Main dashboard
├── components/
│   └── ui/
│       └── card.tsx      # Reusable card component
├── package.json          # Dependencies
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind configuration
└── README.md            # Documentation
```

## 🎨 Customization

### Update Data Sources

Replace the sample data in `app/page.tsx`:

```typescript
// Replace with your actual data
const monthlyData = [
  // Your data here
]

const regionalData = [
  // Your regional analysis
]
```

### Modify Styling

Update colors and themes in:
- `tailwind.config.js` for custom colors
- `app/globals.css` for CSS variables
- Component styles in individual files

### Add New Charts

1. Import additional chart types from Recharts
2. Create new data structures
3. Add to the dashboard grid layout

## 🔒 Environment Variables

For production deployments, you may need:

```bash
# .env.local
NEXT_PUBLIC_API_URL=your-api-endpoint
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
```

## 📱 Mobile Optimization

The dashboard is fully responsive with:
- Mobile-first design approach
- Touch-friendly interactions
- Optimized chart sizes for small screens
- Collapsible navigation for mobile

## 🔧 Performance Features

- **Static Generation**: Pre-rendered at build time
- **Image Optimization**: Disabled for static export
- **Code Splitting**: Automatic with Next.js
- **Tree Shaking**: Unused code elimination

## 📈 Analytics Integration

Add analytics by modifying `app/layout.tsx`:

```typescript
// Add Google Analytics, Plausible, or other analytics
```

## 🐛 Troubleshooting

### Build Issues
- Ensure all dependencies are installed: `npm install`
- Clear cache: `rm -rf .next && npm run build`

### Deployment Issues
- Check that `output: 'export'` is in `next.config.js`
- Verify no server-side features are used
- Ensure all images have `unoptimized: true`

## 📝 License

MIT License - feel free to use for personal or commercial projects.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Ready to deploy? Your dashboard is optimized for Vercel and will be live in minutes!**