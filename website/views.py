"""
In this file, the main routes of the website are managed
"""

from flask import Blueprint, render_template
from flask import g, current_app

views = Blueprint("views", __name__)
overviews = Blueprint("overviews", __name__, static_folder="static")


# this function is executed once before every request :
@views.before_request
@overviews.before_request
def check_user():
    g.engine = current_app.config["engine"]

    def render_template_ctx(page):
        player_list = g.engine.player_list()
        network_list = g.engine.network_list()
        date_list = g.engine.date_list()
        network_members = g.engine.network_members()
        return render_template(
            page,
            engine=g.engine,
            player_list=player_list,
            date_list=date_list,
            network_list=network_list,
            network_members=network_members,
        )

    g.render_template_ctx = render_template_ctx


@views.route("/")
@views.route("/network")
def network():
    return g.render_template_ctx("network.jinja")


@overviews.route("/revenues")
def revenues():
    return g.render_template_ctx("overviews/revenues.jinja")


@overviews.route("/electricity")
def electricity():
    return g.render_template_ctx("overviews/electricity.jinja")


@overviews.route("/storage")
def storage():
    return g.render_template_ctx("overviews/storage.jinja")


@overviews.route("/resources")
def resources():
    return g.render_template_ctx("overviews/resources.jinja")


@overviews.route("/emissions")
def emissions():
    return g.render_template_ctx("overviews/emissions.jinja")
