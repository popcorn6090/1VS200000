from scrapingbee import ScrapingBeeClient; SCRAPINGBEE_API_KEY = 'UO8H6A67OVIPPBNGT233G2LIV20OA3MK5F1WXNHAQVBRVB98733LP55HILQZJIU0J8OF5GE7CYTJQA1B';client = ScrapingBeeClient(api_key=SCRAPINGBEE_API_KEY)
def scrape_url(url, search_terms):
    try:
        response = client.get(url)
        content_str = response.content.decode('utf-8') if response.status_code == 200 else ''
        return {'status': 'success', 'matches': {term: term in content_str for term in search_terms}} if response.status_code == 200 else {'status': 'error', 'message': f'Failed to retrieve the webpage. ScrapingBee error: {response.status_code}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
if __name__ == '__main__':
    url, search_terms = input("Enter the URL: "), [term.strip() for term in input("Enter search terms (comma-separated): ").split(',')];print(scrape_url(url, search_terms))