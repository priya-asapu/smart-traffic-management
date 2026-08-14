"""
Smart Traffic Management System
Module: Maps & Route Engine

Uses OpenRouteService (openrouteservice.org) - free, no card required.

To run:
    python app.py

To test (open in browser):
    http://127.0.0.1:5000/geocode?place=Hyderabad
"""

from flask import Flask, request, jsonify
import openrouteservice
import os
from dotenv import load_dotenv

load_dotenv()  # reads the API key from the .env file

app = Flask(__name__)

# ---------------------------------------------------------------
# STEP 0: OpenRouteService client setup
# In .env file put:  ORS_API_KEY=your_key_here
# ---------------------------------------------------------------
API_KEY = os.getenv("ORS_API_KEY")
client = openrouteservice.Client(key=API_KEY)


# ---------------------------------------------------------------
# STEP 1: Place name -> lat/lng (Geocoding)
# When the user types "BVCITS", this converts it to coordinates.
# ---------------------------------------------------------------
@app.route("/geocode", methods=["GET"])
def geocode_place():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "place parameter is required, e.g. ?place=Hyderabad"}), 400

    try:
        result = client.pelias_search(text=place)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    features = result.get("features", [])
    if not features:
        return jsonify({"error": f"Could not find location for '{place}'"}), 404

    top = features[0]
    lng, lat = top["geometry"]["coordinates"]  # ORS order is [lng, lat]

    return jsonify({
        "place": place,
        "formatted_address": top["properties"].get("label", place),
        "lat": lat,
        "lng": lng
    })


# ---------------------------------------------------------------
# STEP 2: lat/lng -> readable address (to confirm current location)
# ---------------------------------------------------------------
@app.route("/reverse-geocode", methods=["GET"])
def reverse_geocode():
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    if not lat or not lng:
        return jsonify({"error": "lat and lng parameters are required"}), 400

    try:
        result = client.pelias_reverse(point=(float(lng), float(lat)))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    features = result.get("features", [])
    if not features:
        return jsonify({"error": "Address not found"}), 404

    return jsonify({
        "lat": lat,
        "lng": lng,
        "address": features[0]["properties"].get("label", "")
    })


# ---------------------------------------------------------------
# STEP 3 & 4: MAIN ROUTE ENGINE
# This is the most important function in the project.
# Given source + destination -> returns distance, ETA, path
# coordinates (to draw on the map), and turn-by-turn steps.
#
# Every module reuses this same function:
#   - Smart Route
#   - Public Transport (walking mode to the bus stand)
#   - Food / Fuel / Parking (route to a nearby place)
#   - Emergency (driving mode, fastest route)
# ---------------------------------------------------------------
MODE_MAP = {
    "driving": "driving-car",
    "walking": "foot-walking",
    "cycling": "cycling-regular"
}


def get_route(source_lat, source_lng, dest_lat, dest_lng, mode="driving"):
    """
    Common Route Engine function.
    mode: "driving" | "walking" | "cycling"

    Returns a dict with distance_km, duration_min, route coordinates,
    and step-by-step instructions.
    """
    ors_mode = MODE_MAP.get(mode, "driving-car")

    coords = ((source_lng, source_lat), (dest_lng, dest_lat))  # ORS order: [lng, lat]

    result = client.directions(
        coordinates=coords,
        profile=ors_mode,
        format="geojson",
        instructions=True
    )

    feature = result["features"][0]
    props = feature["properties"]
    segment = props["segments"][0]

    distance_km = segment["distance"] / 1000
    duration_min = segment["duration"] / 60

    steps = [
        {
            "instruction": step["instruction"],
            "distance_m": round(step["distance"], 0),
            "duration_sec": round(step["duration"], 0)
        }
        for step in segment["steps"]
    ]

    return {
        "distance_km": round(distance_km, 1),
        "duration_min": round(duration_min, 0),
        # frontend can draw this directly on the map
        "route_coordinates": feature["geometry"]["coordinates"],
        "steps": steps
    }


@app.route("/route", methods=["GET"])
def route_endpoint():
    """
    Example call:
    /route?src_lat=17.38&src_lng=78.48&dest_lat=17.44&dest_lng=78.39&mode=driving
    """
    try:
        src_lat = float(request.args.get("src_lat"))
        src_lng = float(request.args.get("src_lng"))
        dest_lat = float(request.args.get("dest_lat"))
        dest_lng = float(request.args.get("dest_lng"))
        mode = request.args.get("mode", "driving")
    except (TypeError, ValueError):
        return jsonify({"error": "Please send valid src_lat, src_lng, dest_lat, dest_lng"}), 400

    try:
        route = get_route(src_lat, src_lng, dest_lat, dest_lng, mode)
    except Exception as e:
        return jsonify({"error": f"Route not found: {str(e)}"}), 404

    return jsonify({
        "source": {"lat": src_lat, "lng": src_lng},
        "destination": {"lat": dest_lat, "lng": dest_lng},
        "mode": mode,
        "route": route
    })


# ---------------------------------------------------------------
# STEP 5: Nearby places (Food, Fuel, Parking, Bus Stand, Mechanic etc)
# Simple version using Pelias search with a category/query keyword.
# ---------------------------------------------------------------
@app.route("/nearby", methods=["GET"])
def nearby_places():
    """
    Example: /nearby?lat=17.38&lng=78.48&query=restaurant
    """
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    query = request.args.get("query", "restaurant")

    if not lat or not lng:
        return jsonify({"error": "lat and lng are required"}), 400

    try:
        result = client.pelias_search(
            text=query,
            focus_point=(float(lng), float(lat))
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    places = []
    for f in result.get("features", [])[:10]:
        coords = f["geometry"]["coordinates"]
        places.append({
            "name": f["properties"].get("name", query),
            "lat": coords[1],
            "lng": coords[0],
            "address": f["properties"].get("label", "")
        })

    return jsonify({"query": query, "count": len(places), "places": places})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
