from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from website_search_bot import WebsiteSearchBot

app = Flask(__name__)
CORS(app)

# Store active search bots
active_bots = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    website_url = data.get('website_url')
    search_term = data.get('search_term')
    max_pages = int(data.get('max_pages', 100))

    if not website_url or not search_term:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        # Create new bot instance for this search
        bot = WebsiteSearchBot(website_url)
        active_bots[website_url] = bot
        
        results = bot.crawl_and_search(search_term, max_pages)
        
        # Clean up
        if website_url in active_bots:
            del active_bots[website_url]
            
        return jsonify({'results': results})
    except Exception as e:
        if website_url in active_bots:
            del active_bots[website_url]
        return jsonify({'error': str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop_search():
    data = request.get_json()
    website_url = data.get('website_url')
    
    if website_url in active_bots:
        active_bots[website_url].stop_search()
        del active_bots[website_url]
        return jsonify({'message': 'Search stopped successfully'})
    
    return jsonify({'message': 'No active search found for this URL'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
