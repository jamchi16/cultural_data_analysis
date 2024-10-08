import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
import spacy
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyDIEujpvInhhthASGaQHE8G4kJ9NeD1w-E')
text = 'Bamako'
result = gmaps.geocode(text)
nlp = spacy.load("en_core_web_trf")
doc = nlp(text)
for ent in doc.ents:
    print(ent.label_, ent.text)

# sentimentAnalyser = SentimentIntensityAnalyzer()
#
# with open('site_links.json', 'r') as file:
#     links = json.load(file)
#
# links = links[0:10]
# mentioned_entities = {}
# overall_data = {}
# site_data = []
#
# for link in links:
#     site_dict = {
#         'site': link,
#         'sentiment': 0
#     }
#     response = requests.get(link)
#     html_string = response.text
#     document = BeautifulSoup(html_string, "html.parser")
#     all_p = document.findAll('p')
#     page_text = ''
#     for p in all_p:
#         page_text += p.text + ' '
#
#     doc = nlp(page_text)
#     sentences = [sent.text.strip() for sent in doc.sents]
#
#     if len(sentences) > 0:
#         for sentence in sentences:
#             sentiment = sentimentAnalyser.polarity_scores(sentence)['compound']
#             site_dict['sentiment'] += sentiment
#             sent_doc = nlp(sentence)
#             if sent_doc.ents:
#                 for ent in doc.ents:
#                     if not ent.text in mentioned_entities.keys():
#                         mentioned_entities[ent.text] = {'mention_count': 0, 'sentiment': 0, 'label': ''}
#
#                     mentioned_entities[ent.text]['mention_count'] += 1
#                     mentioned_entities[ent.text]['label'] = ent.label_
#                     mentioned_entities[ent.text]['sentiment'] += sentiment
#
#         site_dict['sentiment'] = site_dict['sentiment'] / len(sentences)
#
#     else:
#         site_dict['sentiment'] = 0
#     site_data.append(site_dict)
#
# for ent in mentioned_entities:
#     ent['sentiment'] = ent['sentiment'] / ent['mention_count']