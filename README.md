# 📊 Cross-Channel Advertising Analytics Dashboard

> **Senior Marketing Analyst - Technical Assignment**  
> A comprehensive solution for analyzing multi-channel advertising performance across Facebook, Google Ads, and TikTok.

[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-blue?style=for-the-badge)](https://marketing-analytics-dashboard-ar.streamlit.app/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

---

## 🎯 Project Overview

This project demonstrates end-to-end data analytics capabilities by:
- **Integrating** data from three major advertising platforms
- **Building** a unified data model in Snowflake
- **Creating** an interactive dashboard for cross-platform analysis
- **Generating** actionable insights for marketing optimization

**Live Dashboard:** [marketing-analytics-dashboard-ar.streamlit.app](https://marketing-analytics-dashboard-ar.streamlit.app/)

---

## 📊 Key Features

### **Interactive Dashboard**
- 🎨 Real-time filtering by date range, platform, and campaign
- 📈 10+ interactive visualizations using Plotly
- 🎯 Key performance indicators (KPIs) with instant calculations
- 💡 Automated insights highlighting top performers

### **Unified Data Model**
- 🗄️ Snowflake database with standardized schema
- 🔗 Combines 330+ records from 3 platforms
- 📊 Automated KPI calculations (CTR, CPC, CPA, ROAS, CPM)
- 🎨 Platform-specific metrics preserved

### **Professional Design**
- 🎨 Brand-accurate colors (Facebook Blue, Google Green, TikTok Pink)
- 📱 Responsive layout
- 🌙 Modern dark theme
- ✨ Clean, intuitive interface

---

## 🚀 Quick Start

### **View the Live Dashboard**
Simply visit: [https://marketing-analytics-dashboard-ar.streamlit.app/](https://marketing-analytics-dashboard-ar.streamlit.app/)

### **Run Locally**

```bash
# Clone the repository
git clone https://github.com/your-username/marketing-analytics-dashboard.git
cd marketing-analytics-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
marketing-analytics-dashboard/
│
├── dashboard_app.py              # Main Streamlit application
├── requirements.txt              # Python dependencies
│
├── 01_facebook_ads.csv          # Facebook advertising data
├── 02_google_ads.csv            # Google Ads data
├── 03_tiktok_ads.csv            # TikTok advertising data
│
├── 1.Table_Generation.sql       # Snowflake table creation
├── 2.Data_Verification.sql      # Data quality checks
├── 3.Generate_Unified_Table.sql # Unified data model
├── 4.Analysis.sql               # Analysis views
├── 5.Verification.sql           # Final verification
│
└── README.md                    # This file
```

---

## 🗄️ Database Setup (Snowflake)

### **Prerequisites**
- Snowflake account (free trial available)
- ACCOUNTADMIN role access

### **Setup Steps**

**1. Create Database Structure**
```sql
-- Run 1.Table_Generation.sql
-- Creates: MARKETING_ANALYTICS database, AD_PLATFORMS schema, and 3 tables
```

**2. Load Data**
- Upload CSV files via Snowflake UI:
  - `FACEBOOK_ADS` ← `01_facebook_ads.csv`
  - `GOOGLE_ADS` ← `02_google_ads.csv`
  - `TIKTOK_ADS` ← `03_tiktok_ads.csv`

**3. Verify Data Load**
```sql
-- Run 2.Data_Verification.sql
-- Should show 110 rows for each platform
```

**4. Create Unified Table**
```sql
-- Run 3.Generate_Unified_Table.sql
-- Creates UNIFIED_AD_PERFORMANCE with 330 rows
```

**5. Create Analysis Views**
```sql
-- Run 4.Analysis.sql
-- Creates 4 aggregate views
```

**6. Final Verification**
```sql
-- Run 5.Verification.sql
-- Confirms everything is working correctly
```

---

## 📊 Data Schema

### **Unified Table Structure**

```sql
UNIFIED_AD_PERFORMANCE
├── platform (VARCHAR)           -- 'Facebook', 'Google', 'TikTok'
├── date (DATE)                  -- Campaign date
├── campaign_id (VARCHAR)        -- Platform campaign ID
├── campaign_name (VARCHAR)      -- Campaign name
├── impressions (INTEGER)        -- Ad impressions
├── clicks (INTEGER)             -- Ad clicks
├── cost (DECIMAL)               -- Ad spend
├── conversions (INTEGER)        -- Conversions generated
│
├── -- Calculated KPIs --
├── ctr (DECIMAL)                -- Click-through rate (%)
├── cpc (DECIMAL)                -- Cost per click ($)
├── cpa (DECIMAL)                -- Cost per acquisition ($)
├── roas (DECIMAL)               -- Return on ad spend (%)
└── cpm (DECIMAL)                -- Cost per thousand impressions ($)
```

---

## 📈 Key Insights

### **Platform Performance (January 2024)**

| Platform | Spend | Conversions | ROAS | CPA | Strength |
|----------|-------|-------------|------|-----|----------|
| **Facebook** | $18,292 | 2,395 | 654.7% | $7.64 | 🏆 Best ROAS |
| **Google** | $37,686 | 4,218 | 559.8% | $8.93 | ⚖️ Balanced |
| **TikTok** | $74,267 | 6,750 | 454.4% | $11.00 | 📊 Most Volume |

### **Top 3 Campaigns**

1. **Google - Search_Brand_Terms**: 980.6% ROAS, 1,445 conversions
2. **Facebook - Conversions_Retargeting**: 839.7% ROAS, 1,070 conversions
3. **Google - Shopping_All_Products**: 788.8% ROAS, 1,801 conversions

### **Strategic Recommendations**

1. ✅ **Increase Google Ads Budget** - Highest efficiency with room to scale
2. ✅ **Optimize TikTok Targeting** - High volume but expensive conversions
3. ✅ **Scale Facebook Retargeting** - Exceptional ROAS on cart abandoners
4. ✅ **Implement Cross-Platform Funnel** - TikTok (awareness) → Facebook (consideration) → Google (conversion)

---

## 🛠️ Technologies Used

### **Data & Analytics**
- **Snowflake** - Cloud data warehouse
- **SQL** - Data transformation and analysis
- **Python** - Dashboard development
- **Pandas** - Data manipulation

### **Visualization**
- **Streamlit** - Interactive web framework
- **Plotly** - Interactive charts and graphs

### **Deployment**
- **Streamlit Cloud** - Free hosting
- **GitHub** - Version control

---

## 📊 Dashboard Features

### **Key Performance Indicators**
- Total Spend, Impressions, Clicks, Conversions, ROAS
- Real-time calculations based on filtered data

### **Platform Comparison**
- Spend distribution pie chart
- Conversions by platform bar chart
- Efficiency metrics table

### **Performance Trends**
- Daily spend trends
- Daily conversions trends
- ROAS trends over time

### **Campaign Rankings**
- Top 10 campaigns by ROAS
- Top 10 campaigns by conversions

### **Efficiency Analysis**
- CPA vs ROAS scatter plot
- Platform performance radar chart

### **Automated Insights**
- Best ROAS platform
- Highest converting platform
- Top performing campaign

---

## 🎨 Design Choices

### **Color Palette**
- **Facebook**: `#1877F2` (Official Facebook Blue)
- **Google**: `#34A853` (Official Google Green)
- **TikTok**: `#FF0050` (Official TikTok Pink)

Brand-accurate colors ensure instant platform recognition and professional appearance.

### **Dark Theme**
- Reduces eye strain for extended viewing
- Modern, professional aesthetic
- Excellent contrast for data visualization

---

## 📝 Assignment Requirements

### ✅ **Completed Deliverables**

- [x] **Database Setup** - Snowflake with 3 platform tables + unified table
- [x] **Data Upload** - All CSV files loaded successfully
- [x] **Unified Data Model** - UNIFIED_AD_PERFORMANCE table (330 rows)
- [x] **One-Page Dashboard** - Interactive Streamlit application
- [x] **Key Metrics** - Comprehensive KPIs and visualizations
- [x] **Cross-Channel Analysis** - Multiple comparison views
- [x] **Insights Generated** - Actionable recommendations

---

## 🔧 Configuration

### **requirements.txt**
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.0.0
numpy>=1.24.0
```

### **Python Version**
- Python 3.11 or higher recommended

---

## 🚀 Deployment

This dashboard is deployed on **Streamlit Cloud** for free:

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with one click
4. Get public URL instantly

**Live URL:** [https://marketing-analytics-dashboard-ar.streamlit.app/](https://marketing-analytics-dashboard-ar.streamlit.app/)

---

## 📊 Data Period

- **Date Range**: January 1-30, 2024
- **Total Records**: 330 (110 per platform)
- **Platforms**: Facebook, Google Ads, TikTok
- **Total Ad Spend**: $130,244.90
- **Total Conversions**: 13,363

---

## 🎯 Use Cases

This dashboard is designed for:
- **Marketing Analysts** - Cross-platform performance analysis
- **Campaign Managers** - Budget allocation decisions
- **Digital Marketers** - Campaign optimization insights
- **Stakeholders** - Executive-level reporting
- **Data Teams** - Reference implementation

---

## 🔮 Future Enhancements

Potential improvements for production use:

- [ ] Real-time API integration with ad platforms
- [ ] Predictive analytics and forecasting
- [ ] Automated email reports
- [ ] Multi-touch attribution modeling
- [ ] Budget optimization algorithms
- [ ] A/B test tracking
- [ ] User authentication and role-based access
- [ ] Export functionality (PDF, Excel)
- [ ] Custom date comparisons (YoY, MoM)
- [ ] Anomaly detection alerts

---

## 📄 License

This project was created as a technical assignment for a Senior Marketing Analyst position.

---

## 🙏 Acknowledgments

- **Streamlit** - For the excellent web framework
- **Plotly** - For interactive visualization capabilities
- **Snowflake** - For cloud data warehousing
- Assignment reviewers for the opportunity to showcase these skills

---

## 📊 Project Stats

- **Lines of Code**: ~600 (Python) + ~400 (SQL)
- **Development Time**: ~5 hours
- **Visualizations**: 10+ interactive charts
- **Data Points**: 330 records analyzed
- **KPIs Tracked**: 20+ metrics

---

<div align="center">

**⭐ If you found this project helpful, please consider starring the repository! ⭐**

[View Live Dashboard](https://marketing-analytics-dashboard-ar.streamlit.app/)

---

Made with ❤️ for data-driven marketing decisions

</div>
