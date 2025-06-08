import os
from flask import Flask, render_template, request, send_file
from docx_utils import save_answer_to_docx
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    docx_file_path = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            docx_file_path = save_answer_to_docx(answer)
        except Exception as e:
            answer = f"❌ Błąd: {str(e)}"

    return render_template("index.html", answer=answer, docx_file_path=docx_file_path)

@app.route("/download")
def download():
    docx_file_path = request.args.get("path")
    return send_file(docx_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
