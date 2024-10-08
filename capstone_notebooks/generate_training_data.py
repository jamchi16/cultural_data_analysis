import json
import spacy
from spacy.tokens import DocBin

# Load blank spacy model
nlp = spacy.blank("en")

# Load in annotations for training
with open('../Corona2.json', 'r') as json_file:
    data = json.load(json_file)['examples']

# Format data suitable for spaCy
training_data = []
for excerpt in data:
    training_text = excerpt["content"]
    confirmed_annotations = []
    for annotation in excerpt["annotations"]:
        start = annotation["start"]
        end = annotation["end"]
        label = annotation["tag_name"]
        value = annotation["value"]
        entity = (start, end, label)
        confirmed_annotations.append(entity)
    training_data.append((training_text, confirmed_annotations))

# Try to catch repeats - does not totally work
seen_labels = {}

# Spacy loop to add annotations for training data
db = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if span:
            if not span.text.lower() in seen_labels.keys():
                seen_labels[span.text.lower()] = span.label_
            else:
                if seen_labels[span.text.lower()] != span.label_:
                    continue

            ents.append(span)
    try:
        doc.ents = ents
        db.add(doc)
    except Exception as e:
        print(e)
        continue

db.to_disk("../spacy_training_data/train.spacy")

# Command to train Model:
# python -m spacy train spacy_training_configs/capstone_config.cfg
# --paths.train spacy_training_data/train.spacy
# --paths.dev spacy_training_data/train.spacy
# --output ./spacy_models/model_1
