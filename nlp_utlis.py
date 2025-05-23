import re
import json
from nltk.corpus import stopwords

# تأكد إنك محمل stopwords
try:
    stop_words = set(stopwords.words("arabic"))
except:
    import nltk
    nltk.download("stopwords")
    stop_words = set(stopwords.words("arabic"))

def remove_diacritics(text):
    diacritics_pattern = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    return re.sub(diacritics_pattern, '', text)

def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "و", text)
    text = re.sub("ئ", "ي", text)
    text = re.sub("ة", "ه", text)
    return text

def process_text(sentence):
    sentence = remove_diacritics(sentence)
    words = re.findall(r'\w+', sentence)
    words = [normalize_arabic(word) for word in words if word not in stop_words]
    return words

def match_words_to_videos(words, json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    matched_videos = []
    for word in words:
        for key, value in data.items():
            all_forms = [normalize_arabic(key)] + [normalize_arabic(w) for w in value.get("synonyms", [])]
            if word in all_forms:
                matched_videos.append(value["video"])
                break
    return matched_videos
