import requests
import json
with open('ways.json')as f:ways=json.load(f)
amenity=["clinic",  "doctors", "doctor", "health", "healthcare", "کلینیک_زیبایی","health_care","دکتر","پزشک","مطب","حکیم" ,"beutician", "healthcare=doctor"]
overpass_url = "http://192.168.1.7:12345/api/interpreter"

def fetch_data(query):
    response = requests.get(overpass_url, params={'data': query})
    if response.status_code == 200:
        try:
            return response.json()
        except Exception as e:
            print(e)
    else:
        print(response)
        return {[]}
def fetch_amenity_near_way(way_id, amenity="پزشک",distance=1000):
    doctor_query = f"""
    [out:json];
    way(id:{way_id});
    (
      node(around:{distance})["amenity"="{amenity}"]["contact:phone"];
      node(around:{distance})["amenity"="{amenity}"]["phone"];
      way(around:{distance})["amenity"="{amenity}"];
    );
    out center;
    """
    data = fetch_data(doctor_query)
    return [elem for elem in data['elements'] if elem['type'] in ['node', 'way']] if data else []

for way in ways:
    print(f"ID: {way['id']}, Name: {way['name']}, Type: {way['highway']}")
    doctors = fetch_amenity_near_way(way['id'])
    if doctors:
        print(f"Found {len(doctors)} doctor(s) near way {way['id']} ({way['name']}):")
        for doctor in doctors:
            doc = {
                    "lat": doctor.get('lat') or doctor.get('center', {}).get('lat'),
                    "lon": doctor.get('lon') or doctor.get('center', {}).get('lon'),
                    "osm_id": doctor['id'],
                    "type": doctor['type'],
                    **doctor.get('tags', {})
                }
            if "phone" in doc or "mobile" in list(doc.keys()) or "telephone" in list(doc.keys()):
                with open(f"returns/json3/{doc['osm_id']}.json", "w") as f:json.dump(doc, f, ensure_ascii=False)

    else:
        print(f"No doctors found near way {way['id']} ({way['name']})")
