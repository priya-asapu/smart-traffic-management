# Maps & Route Engine (Member 2 Module)

This is the **Maps & Route Engine** module of the Smart Traffic
Management System. Built with Python + Flask. It's a REST API —
the frontend/backend teams call these endpoints to get route data.

## 1. Setup

```bash
pip install -r requirements.txt
```

This project uses **OpenRouteService** (free, no card required):
1. Sign up at https://openrouteservice.org
2. Copy your "Basic Key" from the dashboard
3. Rename `.env.example` to `.env` and paste the key inside

## 2. Run

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`.

## 3. Endpoints (share this with your team)

### `GET /geocode?place=BVCITS`
Converts a place name into lat/lng coordinates.
Used when the user types a destination.

### `GET /reverse-geocode?lat=..&lng=..`
Converts lat/lng into a readable address (to confirm current location).

### `GET /route?src_lat=..&src_lng=..&dest_lat=..&dest_lng=..&mode=driving`
**This is the Main Route Engine.** Given a source and destination,
it returns distance, ETA, route coordinates (to draw on the map),
and step-by-step directions.

`mode` options: `driving`, `walking`, `cycling`
(the Public Transport module can use `walking` for the leg to the bus stand)

### `GET /nearby?lat=..&lng=..&query=restaurant`
Finds nearby places (food, fuel, parking, bus stand, hospital, mechanic).
Used by Member 4 (Nearby Services), but included here since it's
part of the route engine.

`query` examples:
- `restaurant` → Food
- `petrol pump` → Fuel
- `parking` → Parking
- `bus stand` → Public Transport
- `hospital` → Emergency
- `mechanic` → Vehicle Help

## 4. How other modules use this

- **Smart Route (Home)**: calls `/route` to show 2-3 routes; when the
  user selects one, its coordinates are drawn on the map.
- **Public Transport**: uses `/nearby?query=bus stand` to find the
  stop, then `/route?mode=walking` for the walking leg.
- **Food/Fuel/Parking**: uses `/nearby` to find places, then `/route`
  for navigation to that point.
- **Emergency**: uses `/nearby?query=hospital` to find hospitals, calls
  `/route` for each, and recommends whichever is fastest and not blocked.

## 5. TODO (next steps)

- [ ] Integrate real-time traffic/congestion data from the Traffic
      module (Member 3) into route recommendations
- [ ] Connect with frontend on how to render `route_coordinates` on
      the map (e.g. Leaflet.js `L.polyline()`)
- [ ] Work with the backend team to save routes/history to the database
- [ ] Improve error handling (API limits, invalid locations, etc.)
