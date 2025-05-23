import json
import re
import unicodedata

# دالة لإزالة التشكيل من الكلمات
def remove_diacritics(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

# دالة لتقطيع الجملة لكلمات وتنظيفها (مثل حذف كلمات غير مهمة)
def process_text(sentence):
    # إزالة التشكيل
    sentence = remove_diacritics(sentence)
    
    # تحويل الجملة لكلمات (تقسيم حسب المسافات)
    words = sentence.split()
    
    # قائمة كلمات غير مهمة ممكن تحذفيها من الجملة
    stopwords = {"و", "في", "على", "من", "إلى", "عن", "ال"}
    
    # تنقية الكلمات من الكلمات الغير مهمة
    filtered_words = [word for word in words if word not in stopwords]
    
    return filtered_words

# دالة لمطابقة الكلمات مع الفيديوهات من ملف json
def match_words_to_videos(words, dictionary_path):
    with open(dictionary_path, 'r', encoding='utf-8') as f:
        dictionary = json.load(f)

    matched_videos = []

    for word in words:
        for key, value in dictionary.items():
            # لو الكلمة هي المفتاح نفسه أو من المرادفات (synonyms)
            if word == remove_diacritics(key) or word in [remove_diacritics(s) for s in value.get("synonyms", [])]:
                matched_videos.append(value["video_path"])
                break

    return matched_videos
