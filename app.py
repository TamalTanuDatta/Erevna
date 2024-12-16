from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from website_search_bot import WebsiteSearchBot
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
import tempfile

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
            
        # Format results for frontend
        formatted_results = []
        for url, matches in results.items():
            for match in matches.get('text_matches', []):
                formatted_results.append({
                    'url': url,
                    'context': match
                })
            
        return jsonify({'results': formatted_results})
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
    return jsonify({'message': 'No active search found for this website'})

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    data = request.get_json()
    results = data.get('results', [])
    search_term = data.get('search_term', '')
    website_url = data.get('website_url', '')

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12
    )

    # Create the PDF content
    story = []

    # Add logo
    logo_path = os.path.join(app.static_folder, 'erevna_logo.png')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=2*inch, height=2*inch)
        story.append(img)
        story.append(Spacer(1, 12))

    # Add creator text right after logo
    story.append(Paragraph(
        "Your results are found by Erevna. Erevna is a search bot created by Tamal Datta",
        ParagraphStyle('Creator', parent=styles['Normal'], fontSize=12, textColor=colors.gray, alignment=1)
    ))
    story.append(Spacer(1, 24))

    # Add title and search information
    story.append(Paragraph("Search Results", title_style))
    story.append(Paragraph(f"Search Term: {search_term}", heading_style))
    story.append(Paragraph(f"Website: {website_url}", heading_style))
    story.append(Spacer(1, 12))

    # Add results
    for result in results:
        story.append(Paragraph(f"Found in URL: {result.get('url', '')}", heading_style))
        story.append(Paragraph(result.get('context', ''), normal_style))
        story.append(Spacer(1, 12))

    # Build PDF
    doc.build(story)

    # Send the file
    return send_file(
        temp_file.name,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='search_results.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
