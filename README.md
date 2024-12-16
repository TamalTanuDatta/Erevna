# Erevna - Intelligent Website Search Bot

<div align="center">
  <img src="static/erevna_logo.png" alt="Erevna Logo" width="400"/>
</div>

Erevna is a powerful web crawling and search tool that helps you find specific content across websites. Whether you're searching through production sites or local development servers, Erevna makes it easy to find what you're looking for.

## Features

- 🔍 **Smart Search**: Search for any keyword or phrase across entire websites
- 🌐 **Comprehensive Crawling**: Intelligently crawls through websites while respecting server limits
- 💻 **Local Development Support**: Works with localhost and development servers
- 🎯 **Context-Aware Results**: Shows relevant context around search matches
- 🚀 **Modern UI**: Clean, responsive dark-mode interface
- ⏹️ **Search Control**: Stop searches at any time
- 📄 **PDF Reports**: Download search results as beautifully formatted PDF reports
- 🎨 **Dynamic Branding**: Custom designed logo with modern visual effects

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TamalTanuDatta/Erevna.git
cd Erevna
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit:
```
http://localhost:8081
```

## Usage

1. Enter the website URL you want to search (supports both public websites and local development servers)
2. Enter your search term
3. Set the maximum number of pages to search (default: 100)
4. Click "Search" to start
5. Use the "Stop Search" button if you want to end the search early
6. After getting results, click "Download Results as PDF" to get a detailed report

## PDF Reports

The PDF reports include:
- Erevna logo and branding
- Search parameters (website URL and search term)
- All search results with their full context
- Professional formatting and layout
- Timestamp and attribution

## Technical Details

### Core Features
- Built with Python and Flask
- Uses BeautifulSoup4 for HTML parsing
- Supports multiple content types (HTML, JSON)
- Handles SSL certificates for local development
- Implements rate limiting to be respectful to servers

### Libraries Used
- `flask`: Web framework
- `flask-cors`: Cross-origin resource sharing
- `beautifulsoup4`: HTML parsing
- `requests`: HTTP requests
- `reportlab`: PDF generation

## Development

### Project Structure
```
Erevna/
├── app.py              # Main Flask application
├── website_search_bot.py # Core search functionality
├── create_logo.py      # Logo generation script
├── requirements.txt    # Python dependencies
├── static/            # Static assets
│   └── erevna_logo.png # Generated logo
└── templates/         # HTML templates
    └── index.html     # Main interface
```

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or find any bugs.

## License

MIT License - feel free to use this in your own projects!
