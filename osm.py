from zto3.statics import MTN, MCI, RITEL, MOB
import requests
from geopy.distance import distance
import json
import os
import concurrent.futures


center_lat = 35.6892
center_lon = 51.3890
min_lat, min_lon = 35.7848, 51.2853
max_lat, max_lon = 35.5848, 51.5853
step_size = 500

beauty_phrases = ["doctor"," متخصص پزشک","مطب زیبایی", "پوست و مو"]
url = "http://192.168.1.7:12345/api/interpreter"
medical_Est = [ "کلینیک_زیبایی","health_care","دکتر","پزشک","مطب","حکیم" ,"midwife", "doctors", "doctor", "shop=beauty", "health", "healthcare", "beutician", "healthcare=doctor", "healthcare=dentist", "healthcare=midwife"]
def q_q(phrase, lat, lon, radius_meters=5000):
    query = f"""
    [out:json];
    ( 
    node(around:{radius_meters},{lat},{lon})["name"~"{phrase}"]["phone"];
    );
    out center;
    """
    return query

def am_q(amenity,lat, lon, radius_meters=2500):
    query = f"""
    [out:json];
    (
      node["amenity"~".*{amenity}.*"](around:{radius_meters},{lat},{lon});
    );
    out center;
    """
    return query
def find_doctors_nearby(lat, lon, phrases=None, amenities=None, radius_meters=5000, url=url):
    domain=[]
    results=[]
    if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):return "bad coordinates"
    if phrases:
        domain=phrases
        q_maker=q_q
    if amenities:
        domain=amenities
        q_maker=am_q
    for q in domain:   
        resp = requests.get(url, params={'data': q_maker(q,lat,lon)})
        try:
            data = resp.json()
            for element in data['elements']:
                doc = {
                    "lat": element.get('lat') or element.get('center', {}).get('lat'),
                    "lon": element.get('lon') or element.get('center', {}).get('lon'),
                    "osm_id": element['id'],
                    "type": element['type'],
                    **element.get('tags', {})
                }
                if "phone" in doc or "mobile" in list(doc.keys()) or "telephone" in list(doc.keys()):
                    results.append(doc)
                    with open(f"returns/json/{doc['osm_id']}.json", "w") as f:json.dump(doc, f, ensure_ascii=False)
        except Exception as e:
            print("error", resp, resp.url, str(e))
    return results

# def search_tehran():
#     total_steps = ((int(min_lat * 1e6) - int(max_lat * 1e6)) // step_size + 1) * ((int(max_lon * 1e6) - int(min_lon * 1e6)) // step_size + 1)
#     current_step = 0
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:  # Create a thread pool
#         futures = []
#         for lat in range(int(min_lat * 1e6), int(max_lat * 1e6), -step_size):
#             for lon in range(int(min_lon * 1e6), int(max_lon * 1e6), step_size):
#                 ret=find_doctors_nearby(lat=lat / 1000000, lon=lon / 1000000,phrases=beauty_phrases)
#               # ret=find_doctors_nearby(lat=lat / 1000000, lon=lon / 1000000,medical_amenities=medical_amenities)

#                 current_step += 1
#                 progress = (current_step / total_steps) * 100
#                 os.system('cls' if os.name == 'nt' else 'clear')
#                 print(f">> Searching Latitude={lat / 1000000}, Longitude={lon / 1000000} ")
#                 print(f">> Progress: {progress:.2f}% completed")
def search_tehran():
    total_steps = ((int(min_lat * 1e6) - int(max_lat * 1e6)) // step_size + 1) * ((int(max_lon * 1e6) - int(min_lon * 1e6)) // step_size + 1)
    current_step = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:  # Create a thread pool
        futures = []
        for lat in range(int(min_lat * 1e6), int(max_lat * 1e6), -step_size):
            for lon in range(int(min_lon * 1e6), int(max_lon * 1e6), step_size):
                futures.append(executor.submit(find_doctors_nearby, lat=lat / 1000000, lon=lon / 1000000,phrases=beauty_phrases))
                futures.append(executor.submit(find_doctors_nearby, lat=lat / 1000000, lon=lon / 1000000,amenities=medical_Est))


        for future in concurrent.futures.as_completed(futures):
            # ... (optional: handle results or errors from each thread) ...
            current_step += 1
            progress = (current_step / total_steps) * 100
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f">> Progress: {progress:.2f}% completed\n {future}")
search_tehran()