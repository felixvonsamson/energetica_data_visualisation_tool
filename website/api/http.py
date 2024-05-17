"""
These functions make the link between the website and the database
"""

from flask import Blueprint, request, jsonify, g, current_app, redirect
import pickle
from pathlib import Path

http = Blueprint("http", __name__)


@http.before_request
def check_user():
    g.engine = current_app.config["engine"]


# Gets the data for the overview charts
@http.route("/get_chart_data", methods=["GET"])
def get_chart_data():
    filename = f"instances/{g.engine.instance_name}/instance/player_data/player_{g.engine.current_player_id}.pck"
    with open(filename, "rb") as file:
        data = pickle.load(file)

    return jsonify(
        {
            "data": data,
        }
    )


@http.route("/get_network_data", methods=["GET"])
def get_network_data():
    network_data = {"network_data": None}
    filename = f"instances/{g.engine.instance_name}/instance/network_data/{g.engine.current_network_id}/time_series.pck"
    with open(filename, "rb") as file:
        network_data = {"network_data": pickle.load(file)}

    return jsonify(
        {
            "data": network_data["network_data"],
        }
    )


# Gets the data from the market for the market graph
@http.route("/get_market_data", methods=["GET"])
def get_market_data():
    market_data = {}
    t = int(request.args.get("t"))
    filename_state = f"network_charts/{g.engine.current_network_id}/market_t{g.engine.current_t-t}.pck"
    if Path(filename_state).is_file():
        with open(filename_state, "rb") as file:
            market_data = pickle.load(file)
            market_data["capacities"] = market_data["capacities"].to_dict(
                orient="list"
            )
            market_data["demands"] = market_data["demands"].to_dict(
                orient="list"
            )
    else:
        market_data = None
    return jsonify(market_data)


@http.route("/player_and_date", methods=["POST"])
def player_and_date():
    player_id = int(request.form.get("player_id"))
    instance_name = request.form.get("date")
    g.engine.switch_database(
        new_instance=instance_name, new_player_id=player_id
    )
    return redirect("/production_overview/electricity", code=303)


@http.route("/network_and_date", methods=["POST"])
def network_and_date():
    network_id = int(request.form.get("network_id"))
    instance_name = request.form.get("date")
    g.engine.switch_database(
        new_instance=instance_name, new_network_id=network_id
    )
    return redirect("/", code=303)


@http.route("/get_players", methods=["GET"])
def get_players():
    player_list = g.engine.player_list()
    return {player["id"]: player for player in player_list}
