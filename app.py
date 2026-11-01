"""Site It 119 Spa da Beleza — Flask.
Rodar:  pip install flask  &&  python app.py   ->  http://localhost:5000
"""
import csv, os, re
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
LEADS = os.path.join(os.path.dirname(__file__), "leads.csv")

CONFIG = {
    "whatsapp": "5519987220119",
    "instagram": "https://www.instagram.com/it119spadabeleza",
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/lead", methods=["POST"])
def lead():
    """Guarda cada contato em leads.csv (nome, telefone, interesse)."""
    d = request.get_json(silent=True) or {}
    nome = str(d.get("nome", "")).strip()[:80]
    tel = re.sub(r"\D", "", str(d.get("telefone", "")))[:13]
    if len(nome) < 2 or len(tel) < 10:
        return jsonify(ok=False, erro="Preencha nome e WhatsApp com DDD."), 400
    novo = not os.path.exists(LEADS)
    with open(LEADS, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["data", "nome", "telefone", "interesse"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), nome, tel,
                    str(d.get("interesse", ""))[:120]])
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(debug=True)
