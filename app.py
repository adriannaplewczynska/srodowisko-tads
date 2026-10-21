from flask import Flask, request, abort, jsonify
from services import policz_wskazniki, dostepne_regiony

app = Flask(__name__)
SCIEZKA_DANYCH = "dane/zamowienia.csv"

@app.get("/")
def index():
    return "Panel wskaźników"

@app.get("/kpi")
def kpi_html():
    region = request.args.get("region")
    if region and region not in dostepne_regiony(SCIEZKA_DANYCH):
        abort(404, description=f"Nieznany region: {region}")
    
    w = policz_wskazniki(SCIEZKA_DANYCH, region)
    reg_label = w["region"] if w["region"] else "Wszystkie"
    return f"<h1>Wskaźniki: {reg_label}</h1><p>Marża: {w['marza']:.2%}</p>"

@app.get("/api/kpi")
def kpi_api():
    region = request.args.get("region")
    if region and region not in dostepne_regiony(SCIEZKA_DANYCH):
        abort(404, description=f"Nieznany region: {region}")
    
    w = policz_wskazniki(SCIEZKA_DANYCH, region)
    return jsonify(w)