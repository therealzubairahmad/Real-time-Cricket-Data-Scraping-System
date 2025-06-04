# Real-time Cricket Data Scraping System

A Python-based system that scrapes cricket match data from CREX in real-time, tracking match schedules and details.

## Project Structure

\`\`\`
cricket-data-scraper/
├── scraper.py         # Main scraping functions
├── scheduler.py       # Scheduling logic for real-time updates
├── requirements.txt   # Python dependencies
├── README.md          # This file
├── vercel.json        # Vercel deployment configuration
├── .gitignore         # Git ignore file
├── data/              # Generated data storage
│   ├── fixtures/      # Match fixtures data
│   └── matches/       # Individual match data
├── logs/              # Error logs
└── utils/             # Utility functions
    └── helpers.py     # Helper functions
\`\`\`

## Features

- Scrapes upcoming cricket match schedules
- Tracks match details including:
  - Match info
  - Team squads
  - Live updates
  - Scorecards
- Automatically triggers real-time updates when matches start
- Stores data in structured JSON format

## Setup

1. Clone the repository:
   \`\`\`
   git clone https://github.com/yourusername/cricket-data-scraper.git
   cd cricket-data-scraper
   \`\`\`

2. Install dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

3. Install Chrome WebDriver (required for Selenium)

4. Run the scraper:
   \`\`\`
   python scraper.py
   \`\`\`

5. Set up the scheduler to run periodically:
   \`\`\`
   python scheduler.py
   \`\`\`

## Deployment

This project can be deployed on Vercel using the provided `vercel.json` configuration.

## Data Structure

### Fixtures Data

Stored in `data/fixtures/fixtures.json`:
\`\`\`json
[
  {
    "teams": "Team A vs Team B",
    "start_time": "Thu, 06 Jun 2024, 03:30 PM",
    "url": "https://crex.live/cricket/matches/123"
  },
  ...
]
\`\`\`

### Match Data

Stored in `data/matches/match_id.json`:
\`\`\`json
{
  "url": "https://crex.live/cricket/matches/123",
  "match_info": "...",
  "squads": "...",
  "scorecard": "...",
  "live": "..."
}
\`\`\`

## License

MIT
\`\`\`

Let's also create empty directories to ensure the structure is complete:
