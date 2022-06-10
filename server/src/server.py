from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from Simulation.Simulation import Simulation

# Disable flask logging
log = logging.getLogger('werkzeug')
log.disabled = True

# Init flask app + simulation instances
app = Flask(__name__)
CORS(app)
simulation = Simulation()

# Return price at simulation's next tick on GET /next-tick
@app.route("/next-tick")
def next_tick():
    simulation.next_tick()
    return jsonify(curr_price=simulation.orderbook.curr_price)

@app.route("/set-sentiment", methods=["POST"])
def set_sentiment():
    req_body = request.get_json()
    new_sentiment = req_body.get("newSentiment")
    simulation.set_sentiment(new_sentiment)
    return "OK"
