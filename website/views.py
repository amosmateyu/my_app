from flask import Blueprint, render_template, make_response
from flask_login import login_required

main_bp = Blueprint("main", __name__)

# Helper: disable browser caching
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response



@main_bp.route("/")
@login_required  
def home():
    resp = make_response(render_template("home_screen.html"))
    return no_cache(resp)

@main_bp.route("/prediction")
@login_required  
def prediction():
    resp = make_response(render_template("prediction_screen.html"))
    return no_cache(resp)

@main_bp.route("/about")
@login_required 
def about():
    resp = make_response(render_template("about_screen.html"))
    return no_cache(resp)

@main_bp.route("/results")
@login_required  
def results():
    resp = make_response(render_template("results_screen.html"))
    return no_cache(resp)
