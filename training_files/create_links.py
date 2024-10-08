from serpapi import GoogleSearch
import json

def search_google(query):
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": 'eac0be02b90cf727cbd0edbbe45876aa16c164251de916ce6b2ba64e588f1a6c',
        "num": 10
    }

    site_links = []
    start = 0

    while start < 1000:
        params["start"] = start
        search = GoogleSearch(params)
        results = search.get_dict().get('organic_results', [])

        if not results:
            break

        for result in results:
            site_links.append(result['link'])

        start += 10

    return site_links


if __name__ == "__main__":
    search_term = 'Pokemon'
    site_links = search_google(search_term)
    with open('site_links.json', 'w') as file:
        json.dump(site_links, file)
