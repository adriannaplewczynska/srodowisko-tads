from flask import Blueprint, request, abort, current_app
from .services import policz_wskazniki, dostepne_regiony

panel_bp = Blueprint("panel", __name__)

@panel_bp.get("/")
def index():
    return "Panel wskaźników"

@panel_bp.get("/kpi")
def kpi_html():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    region = request.args.get("region")
    if region and region not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {region}")

    w = policz_wskazniki(sciezka, region)
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])
    reg_label = w["region"] if w["region"] else "Wszystkie"
    return f"<h1>Wskaźniki: {reg_label}</h1><p>Marża: {w['marza']:.2%}</p>"