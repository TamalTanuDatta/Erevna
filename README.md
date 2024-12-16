# Erevna - Intelligent Website Search Bot

Erevna is a powerful web crawling and search tool that helps you find specific content across websites. Whether you're searching through production sites or local development servers, Erevna makes it easy to find what you're looking for.

## Features

- 🔍 **Smart Search**: Search for any keyword or phrase across entire websites
- 🌐 **Comprehensive Crawling**: Intelligently crawls through websites while respecting server limits
- 💻 **Local Development Support**: Works with localhost and development servers
- 🎯 **Context-Aware Results**: Shows relevant context around search matches
- 🚀 **Modern UI**: Clean, responsive dark-mode interface
- ⏹️ **Search Control**: Stop searches at any time

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

## Technical Details

- Built with Python and Flask
- Uses BeautifulSoup4 for HTML parsing
- Supports multiple content types (HTML, JSON)
- Handles SSL certificates for local development
- Implements rate limiting to be respectful to servers

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or find any bugs.

## License

MIT License - feel free to use this in your own projects!
