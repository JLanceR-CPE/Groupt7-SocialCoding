import urllib.parse
import requests
from tabulate import tabulate

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "DCyC94mD9j5zm610lKj1yduatJBIK41P"

def display_route(route_data, units):
    print("Trip Duration:   {}".format(route_data["formattedTime"]))

    # Convert distance to the selected units
    if units == "imperial":
        distance = route_data["distance"]
        distance_text = "{:.2f} miles".format(distance * 0.621371)  # Convert to miles
    else:
        distance = route_data["distance"] * 1.60934
        distance_text = "{:.2f} km".format(distance)

    print("Distance:        {}".format(distance_text))

    # Check if "fuelUsed" is available in the response
    if "fuelUsed" in route_data:
        fuel_used = route_data["fuelUsed"]
        if units == "imperial":
            fuel_used *= 0.264172  # Convert to gallons
            fuel_used_text = "{:.2f} gallons".format(fuel_used)
        else:
            fuel_used_text = "{:.2f} liters".format(fuel_used)

        print("Fuel Used (Ltr): {}".format(fuel_used_text))
    else:
        print("Fuel Used (Ltr): Data not available")

    print("=============================================")

def display_maneuvers(maneuvers, units):
    headers = ["Maneuver", "Distance"]
    data = [(maneuver["narrative"], "{:.2f} miles".format(maneuver["distance"] * 0.621371) if units == "imperial" else "{:.2f} km".format(maneuver["distance"] * 1.61)) for maneuver in maneuvers]
    print(tabulate(data, headers=headers, tablefmt="pretty"))

def get_alternative_routes(orig, dest, units):
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest, "routeType": "fastest", "maxRoutes": 3})
    json_data = requests.get(url).json()

    # Check if the route data exists in the response
    if "route" in json_data:
        primary_route = json_data["route"]
        alternative_routes = json_data["route"]["alternateRoutes"] if "alternateRoutes" in json_data["route"] else []

        return primary_route, alternative_routes
    else:
        return None, []  # Return None when route data is not available

while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break

    units = input("Select units (metric/imperial): ").lower()
    if units not in ["metric", "imperial"]:
        print("Invalid unit selection. Using default (metric).")
        units = "metric"

    primary_route, alternative_routes = get_alternative_routes(orig, dest, units)

    if primary_route is not None:
        print("API Status: 0 = A successful route call.\n")
        print("=============================================")
        print("Directions from {} to {}".format(orig, dest))

        # Display primary route
        print("Primary Route:")
        display_route(primary_route, units)

        # Display alternative routes
        for i, alt_route in enumerate(alternative_routes):
            print(f"Alternative Route {i + 1}:")
            display_route(alt_route, units)

            # Display alternative route maneuvers in a table
            print(f"Alternative Route {i + 1} Maneuvers:")
            display_maneuvers(alt_route["legs"][0]["maneuvers"], units)

        # Display primary route maneuvers in a table
        print("Primary Route Maneuvers:")
        display_maneuvers(primary_route["legs"][0]["maneuvers"], units)

        print("=============================================")

    else:
        print("Route data not available.")