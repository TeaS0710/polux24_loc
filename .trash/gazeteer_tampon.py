import lmdb
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Configuration du geolocator
geolocator = Nominatim(user_agent="gazetteer_association")

# Fonction pour géocoder une localisation
def geocode_location(location_name):
    try:
        location = geolocator.geocode(location_name, timeout=10)
        if location:
            return {
                "name": location_name,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "address": location.address,
            }
    except GeocoderTimedOut:
        print(f"Timeout lors de la géocodage de {location_name}")
    return None

# Initialisation de la base de données LMDB
def init_lmdb(db_path, map_size=10485760):
    return lmdb.open(db_path, map_size=map_size)

# Fonction pour insérer des données dans LMDB
def insert_into_lmdb(env, key, value):
    with env.begin(write=True) as txn:
        txn.put(key.encode("utf-8"), value.encode("utf-8"))

# Fonction pour récupérer des données depuis LMDB
def get_from_lmdb(env, key):
    with env.begin() as txn:
        value = txn.get(key.encode("utf-8"))
        return value.decode("utf-8") if value else None

# Exemple principal
if __name__ == "__main__":
    # Initialisation de LMDB
    lmdb_path = "gazetteer_lmdb"
    env = init_lmdb(lmdb_path)

    # Liste d'entités nommées (REN) détectées
    detected_entities = ["Paris", "Lyon", "Marseille", "Berlin", "New York"]

    # Insertion des entités dans la base LMDB
    for entity in detected_entities:
        insert_into_lmdb(env, entity, "detected")

    # Association des REN avec des points géographiques
    for entity in detected_entities:
        # Vérification si l'entité existe dans LMDB
        status = get_from_lmdb(env, entity)
        if status:
            print(f"Traitement de '{entity}' trouvé dans LMDB.")
            # Géocoder l'entité
            location_data = geocode_location(entity)
            if location_data:
                print(f"'{entity}' est associé à :")
                print(f"  Adresse : {location_data['address']}")
                print(f"  Latitude : {location_data['latitude']}")
                print(f"  Longitude : {location_data['longitude']}")
            else:
                print(f"Impossible de géocoder '{entity}'.")
        else:
            print(f"'{entity}' non trouvé dans LMDB.")

    # Fermeture de la base LMDB
    env.close()
