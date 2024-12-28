import json
from geopy.geocoders import Nominatim

def analyze_and_store_locations(location_list, output_file):
    geolocator = Nominatim(user_agent="location_analyzer")
    results = []

    for location_name in location_list:
        try:
            location = geolocator.geocode(location_name)
            if location:
                results.append({
                    "name": location_name,
                    "address": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })
            else:
                results.append({
                    "name": location_name,
                    "error": "Location not found"
                })
        except Exception as e:
            results.append({
                "name": location_name,
                "error": str(e)
            })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Results stored in {output_file}")

# Example usage
location_list = ["175 5th Avenue NYC", "Eiffel Tower", "Invalid Location"]
output_file = "locations.json"
analyze_and_store_locations(location_list, output_file)

