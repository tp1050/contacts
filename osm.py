import requests
import json
ways=[]
amenity=["clinic",  "doctors", "doctor", "health", "healthcare", "کلینیک_زیبایی","health_care","دکتر","پزشک","مطب","حکیم" ,"beutician", "healthcare=doctor"]
f = """[out:json];
(
  way["highway"]["name"](35.6007,51.2534,35.8086,51.5602);
);
out body;
>;
out skel qt;"""
overpass_url = "http://192.168.1.7:12345/api/interpreter"

def fetch_data(query):
    response = requests.get(overpass_url, params={'data': query})
    if response.status_code == 200:
        # print(response.content)
        return response.json()
    else:
        print(response)
        return None

def fetch_doctors(way_id):
    ret=[]
    for a in amenity:
        doctor_query = f"""
    [out:json];
    way(id:{way_id});
    node(w)["amenity"~"{a}"];
    out;
    """
        data = fetch_data(doctor_query)
        ret.extend([elem for elem in data['elements'] if elem['type'] == 'node']) if data else []
    return ret

# data = fetch_data(f)
# if not data:
#     exit()
# else :print(data)

# ways = [{
#     'id': element['id'],
#     'name': element.get('tags', {}).get('name', 'Unknown'),
#     'highway': element.get('tags', {}).get('highway', 'Unknown'),
#     'nodes': element['nodes']
# } for element in data['elements'] if element['type'] == 'way']

# for way in ways:
#     print(f"ID: {way['id']}, Name: {way['name']}, Type: {way['highway']}")
#     doctors = fetch_doctors(way['id'])
    
#     if doctors:
#         print(f"Found {len(doctors)} doctor(s) along way {way['id']} ({way['name']}):")
#         for doctor in doctors:
#             doctor_name = doctor.get('tags', {}).get('name', 'Unnamed')
#             print(f"  - Doctor: {doctor_name} (Node ID: {doctor['id']})")
            
#             with open(f'{doctor["id"]}.json', 'w') as f:
#                 json.dump(doctor, f, indent=2,ensure_ascii=False)
#     else:
#         print(f"No doctors found along way {way['id']} ({way['name']})")

# with open('ways.json', 'w') as f:
#     json.dump(ways, f, indent=2,ensure_ascii=False)
with open('ways.json', 'r+') as f:
    ways=json.load( f)
def fetch_doctors_near_way(way_id, distance=100):
    doctor_query = f"""
    [out:json];
    way(id:{way_id});
    (
      node(around:{distance})["amenity"="doctors"];
    );
    out center;
    """
    data = fetch_data(doctor_query)
    return [elem for elem in data['elements'] if elem['type'] in ['node', 'way']] if data else []

for way in ways:
    print(f"ID: {way['id']}, Name: {way['name']}, Type: {way['highway']}")
    doctors = fetch_doctors_near_way(way['id'])
    if doctors:
        print(f"Found {len(doctors)} doctor(s) near way {way['id']} ({way['name']}):")
        for doctor in doctors:
            # doctor_name = doctor.get('tags', {}).get('name', 'Unnamed')
            # doctor_type = "Node" if doctor['type'] == 'node' else "Way"
            # print(f"  - Doctor: {doctor_name} ({doctor_type} ID: {doctor['id']})")
            doc = {
                    "lat": doctor.get('lat') or doctor.get('center', {}).get('lat'),
                    "lon": doctor.get('lon') or doctor.get('center', {}).get('lon'),
                    "osm_id": doctor['id'],
                    "type": doctor['type'],
                    **doctor.get('tags', {})
                }
            if "phone" in doc or "mobile" in list(doc.keys()) or "telephone" in list(doc.keys()):
                # results.append(doc)
                with open(f"returns/json3/{doc['osm_id']}.json", "w") as f:json.dump(doc, f, ensure_ascii=False)
            
            
            
            
            
            
            
            
            
            
            
            
            # with open(f'returns/json2/{doctor["id"]}.json', 'w') as f:
            #     json.dump(doctor, f, indent=2, ensure_ascii=False)
    else:
        print(f"No doctors found near way {way['id']} ({way['name']})")
