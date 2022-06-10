from flask import Flask, jsonify
import logging
from Simulation.Simulation import Simulation

# Disable flask logging
log = logging.getLogger('werkzeug')
log.disabled = True

# Init flask app + simulation instances
app = Flask(__name__)
simulation = Simulation()

# Return price at simulation's next tick on GET /next-tick
@app.route("/next-tick")
def next_tick():
    simulation.next_tick()
    return jsonify(curr_price=simulation.orderbook.curr_price)
