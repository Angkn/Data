from flask import Flask, render_template, jsonify, request, session
import random

app = Flask(__name__)
app.secret_key = "secret"

# ข้อมูลคำศัพท์ (List)
word_pairs = [
    ("cat", "แมว"), ("dog", "สุนัข"), ("apple", "แอปเปิ้ล"), ("banana", "กล้วย"),
    ("car", "รถยนต์"), ("book", "หนังสือ"), ("sun", "ดวงอาทิตย์"), ("moon", "พระจันทร์"),
    ("water", "น้ำ"), ("fire", "ไฟ"), ("tree", "ต้นไม้"), ("flower", "ดอกไม้"),
    ("house", "บ้าน"), ("school", "โรงเรียน"), ("fish", "ปลา"), ("bird", "นก"),
    ("computer", "คอมพิวเตอร์"), ("phone", "โทรศัพท์"), ("music", "เพลง"), ("milk", "นม"),
    ("pen", "ปากกา"), ("paper", "กระดาษ"), ("shirt", "เสื้อ"), ("shoe", "รองเท้า"),
    ("ball", "ลูกบอล")
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_cards')
def get_cards():
    cards = []
    for eng, thai in word_pairs:
        cards.append({"text": eng, "pair": thai})
        cards.append({"text": thai, "pair": eng})
    random.shuffle(cards)

    session['cards'] = cards
    session['score'] = 0
    session['life'] = 3
    session['stack'] = []  # Stack

    return jsonify(cards)

@app.route('/check_match', methods=['POST'])
def check_match():
    data = request.get_json()
    card_text = data['text']

    stack = session.get('stack', [])
    cards = session.get('cards', [])
    score = session.get('score', 0)
    life = session.get('life', 3)

    stack.append(card_text)
    result = {"match": False, "score": score, "life": life}

    if len(stack) == 2:
        first, second = stack
        pair_dict = {c["text"]: c["pair"] for c in cards}
        if pair_dict.get(first) == second:
            score += 10
            result["match"] = True
        else:
            life -= 1
        stack.clear()

    session['stack'] = stack
    session['score'] = score
    session['life'] = life
    result["score"] = score
    result["life"] = life

    return jsonify(result)

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/end')
def end():
    score = session.get('score', 0)
    return render_template('end.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
