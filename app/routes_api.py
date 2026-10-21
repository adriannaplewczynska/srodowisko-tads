from flask import Blueprint, request, abort, jsonify, current_app
from .services import policz_wskazniki, dostepne_regiony

api_bp = Blueprint("api", __name__)

@api_bp.get("/kpi")
def kpi_api():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    region = request.args.get("region")
    if region and region not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {region}")

    w = policz_wskazniki(sciezka, region)
    return jsonify(w)