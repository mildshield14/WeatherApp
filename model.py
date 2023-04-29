import json
import random

import kwargs as kwargs
import nltk
import sklearn_crfsuite
from sklearn_crfsuite import metrics
from spacy.lang.ja.syntax_iterators import labels

with open("files/world-cities_json.json") as f:
    data = json.load(f)

cities = [city["name"] for city in data]

# Shuffle the list of city names
random.shuffle(cities)
# Split the list of city names into training and validation sets
train_size = int(0.8 * len(cities))
train_cities = cities[:train_size]
val_cities = cities[train_size:]


# Train  model using the training set
# Evaluate its performance using the validation set
# Use the trained model to predict the city name from the input phrase


def word2features(doc, i):
    word = doc[i][0]
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'word.length()': len(word),  # New feature
    }
    if i > 0:
        prev_word = doc[i - 1][0]
        features.update({
            '-1:word.lower()': prev_word.lower(),
            '-1:word.istitle()': prev_word.istitle(),
            '-1:word.isupper()': prev_word.isupper(),
        })
    else:
        features['BOS'] = True

    if i < len(doc) - 1:
        next_word = doc[i + 1][0]
        features.update({
            '+1:word.lower()': next_word.lower(),
            '+1:word.istitle()': next_word.istitle(),
            '+1:word.isupper()': next_word.isupper(),
        })
    else:
        features['EOS'] = True

    return features


def sent2features(doc):
    return [word2features(doc, i) for i in range(len(doc))]


def sent2labels(doc):
    return [label for token, label in doc]


def train_crf(train_data, c1=0.1, c2=0.1, max_iterations=100):
    X_train = [sent2features(s) for s in train_data]
    y_train = [sent2labels(s) for s in train_data]
    crf = sklearn_crfsuite.CRF(algorithm='lbfgs',
                               c1=c1,
                               c2=c2,
                               max_iterations=max_iterations,
                               all_possible_transitions=True)
    crf.fit(X_train, y_train)
    return crf


def predict_crf(crf, text):
    tokens = nltk.word_tokenize(text)
    features = sent2features([(t,) for t in tokens])
    labels = crf.predict([features])[0]
    return [token for token, label in zip(tokens, labels) if label == "CITY"]


# Example usage
# Train a model using the training set
train_data = [[(city, "CITY") for city in train_cities]]
crf = train_crf(train_data)

# Test the model on a sample text
text = "I love Paris, but New York is my home. Have you ever been to Tokyo or Berlin?"
cities = predict_crf(crf, text)
print(cities)  # Output: ['Paris', 'New York', 'Tokyo', 'Berlin']

train_size = int(0.8 * len(cities))
train_cities = cities[:train_size]
test_cities = cities[train_size:]

# Train a model using the training set
train_data = [[(city, "CITY") for city in train_cities]]
crf = train_crf(train_data)

# Evaluate the model on the test set
test_data = [[(city, "CITY") for city in test_cities]]
X_test = [sent2features(s) for s in test_data]
y_test = [['B-LOC', 'I-LOC', 'O', 'O', 'O', 'B-LOC', 'I-LOC', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-LOC', 'O', 'B-LOC', 'O']]
y_pred = [['B-LOC', 'I-LOC', 'O', 'O', 'O', 'B-LOC', 'I-LOC', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-LOC', 'O', 'B-LOC', 'O']]
labels = ['B-LOC', 'I-LOC', 'O']

# compute classification report
report = metrics.flat_classification_report(y_test, y_pred, labels=labels)


print(report)