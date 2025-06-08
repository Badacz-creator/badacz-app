import os
from flask import Flask, request, send_file, render_template_string
import openai
from docx_utils import save_answer_to_docx

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY") or ""

HTML = '''
<!DOCTYPE html><html><head><meta charset="utf-8"><title>Badacz</title></head>
<body><h1>Badacz GPT‑4o</h1>
<form method="POST"><textarea name="prompt" rows="5" cols="60" placeholder="Zadaj pytanie..."></textarea><br><button type="submit">Wyślij</button></form>
{% if answer %}<h2>Odpowiedź:</h2><pre>{{answer}}</pre><a href="/download">Pobierz .docx</a>{% endif %}
</body></html>
'''

last_answer = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global last_answer
    answer = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        resp = openai.ChatCompletion.create(
            model="gpt-4o",
            assistant_id="asst_iJXrOx7SYtIw5hBBWnb1xfji",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = resp.choices[0].message.content
        last_answer = answer
    return render_template_string(HTML, answer=answer)

@app.route("/download")
def download():
    global last_answer
    path = save_answer_to_docx(last_answer)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
