from flask import Flask, request, jsonify
from nlp_utils import process_text, match_words_to_videos  # تأكدي اسم الملف صح

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def handle_request():
    data = request.get_json()
    sentence = data.get("sentence", "")
    
    # نحلل الجملة
    words = process_text(sentence)
    
    # نجيب الفيديوهات اللي تطابق الكلمات
    videos = match_words_to_videos(words, "dictionary.json")
    
    return jsonify({"words": words, "videos": videos})

if __name__ == "__main__":
    app.run(debug=True)
