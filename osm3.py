import requests, json

tabriz_bbox = "37.9,45.9,38.2,46.5"

# List of bboxes for Iran's 60 big cities
iran_city_bboxes = [
    "35.6,51.2,35.8,51.5",  # Tehran
    "32.6,51.6,32.7,51.7",  # Isfahan
    "36.2,59.5,36.4,59.7",  # Mashhad
    "29.5,52.4,29.7,52.6",  # Shiraz
    "38.0,46.2,38.1,46.4",  # Tabriz
    "31.3,48.6,31.4,48.8",  # Ahvaz
    "34.3,47.0,34.4,47.1",  # Kermanshah
    "36.8,54.4,36.9,54.5",  # Gorgan
    "34.6,50.8,34.7,51.0",  # Qom
    "37.2,49.5,37.3,49.7",  # Rasht
    "33.9,51.5,34.0,51.6",  # Kashan
    "35.7,50.9,35.8,51.1",  # Karaj
    "32.3,48.6,32.4,48.7",  # Khorramabad
    "36.5,52.6,36.6,52.7",  # Sari
    "27.1,56.2,27.2,56.3",  # Bandar Abbas
    "35.5,51.3,35.6,51.4",  # Eslamshahr
    "30.2,57.0,30.3,57.1",  # Kerman
    "38.0,46.2,38.1,46.3",  # Urmia
    "35.3,46.9,35.4,47.0",  # Sanandaj
    "36.3,59.5,36.4,59.6",  # Neyshabur
    "32.6,51.3,32.7,51.4",  # Najafabad
    "35.7,51.3,35.8,51.4",  # Qods
    "36.8,54.4,36.9,54.5",  # Gonbad-e Kavus
    "35.5,51.5,35.6,51.6",  # Varamin
    "32.3,50.8,32.4,50.9",  # Shahr-e Kord
    "37.4,57.3,37.5,57.4",  # Bojnord
    "33.6,46.4,33.7,46.5",  # Ilam
    "36.2,57.6,36.3,57.7",  # Sabzevar
    "32.3,50.8,32.4,50.9",  # Khomeyni Shahr
    "35.2,48.9,35.3,49.0",  # Malayer
    "32.6,51.6,32.7,51.7",  # Shahin Shahr
    "36.5,53.0,36.6,53.1",  # Amol
    "35.8,50.9,35.9,51.0",  # Qazvin
    "36.6,53.2,36.7,53.3",  # Babol
    "34.7,48.5,34.8,48.6",  # Hamadan
    "29.6,52.5,29.7,52.6",  # Marvdasht
    "32.6,51.3,32.7,51.4",  # Yazd
    "37.5,45.0,37.6,45.1",  # Khoy
    "36.8,54.4,36.9,54.5",  # Bandar-e Anzali
    "35.3,47.0,35.4,47.1",  # Qorveh
    "36.2,57.6,36.3,57.7",  # Neyshabur
    "32.3,50.8,32.4,50.9",  # Borujerd
    "36.5,52.6,36.6,52.7",  # Babol
    "35.7,51.3,35.8,51.4",  # Karaj
    "29.6,52.5,29.7,52.6",  # Jahrom
    "36.8,54.4,36.9,54.5",  # Gorgan
    "35.3,46.9,35.4,47.0",  # Marivan
    "32.6,51.6,32.7,51.7",  # Najafabad
    "36.2,59.5,36.3,59.6",  # Torbat-e Heydarieh
    "35.5,51.5,35.6,51.6",  # Pakdasht
    "32.3,50.8,32.4,50.9",  # Arak
    "37.4,57.3,37.5,57.4",  # Shirvan
    "33.6,46.4,33.7,46.5",  # Ilam
    "36.2,57.6,36.3,57.7",  # Sabzevar
    "32.3,50.8,32.4,50.9",  # Khomeyni Shahr
    "35.2,48.9,35.3,49.0",  # Malayer
    "32.6,51.6,32.7,51.7",  # Shahin Shahr
    "36.5,53.0,36.6,53.1",  # Amol
    "35.8,50.9,35.9,51.0",  # Qazvin
    "36.6,53.2,36.7,53.3"   # Babol
]


iran_city_districts = {
    "Tabriz": [
        "37.9,45.9,38.0,46.0",  # Central District
        "38.0,46.0,38.1,46.1",  # Baghmisheh District
        "38.1,46.1,38.2,46.2",  # Roshdieh District
        "37.9,46.2,38.0,46.3",  # Eram District
        "38.0,46.3,38.1,46.4"   # Vali Asr District
    ],
    "Karaj": [
        "35.7,50.9,35.8,51.0",  # Mehrshar District
        "35.8,51.0,35.9,51.1",  # Gohardasht District
        "35.7,51.1,35.8,51.2",  # Fardis District
        "35.8,51.2,35.9,51.3",  # Hesarak District
        "35.7,51.3,35.8,51.4"   # Azimiyeh District
    ],
    "Isfahan": [
        "32.6,51.6,32.7,51.7",  # Jolfa District
        "32.5,51.7,32.6,51.8",  # Zeinabieh District
        "32.6,51.8,32.7,51.9",  # Khaneh Isfahan District
        "32.5,51.9,32.6,52.0",  # Shahin Shahr District
        "32.6,52.0,32.7,52.1"   # Khomeini Shahr District
    ],
    "Qazvin": [
        "36.2,49.9,36.3,50.0",  # Minoodar District
        "36.3,50.0,36.4,50.1",  # Nokhbegan District
        "36.2,50.1,36.3,50.2",  # Azadegan District
        "36.3,50.2,36.4,50.3",  # Barajin District
        "36.2,50.3,36.3,50.4"   # Mehregan District
    ],
    "Kelardasht": [
        "36.5,51.1,36.6,51.2",  # Central District
        "36.6,51.2,36.7,51.3",  # Valroud District
        "36.5,51.3,36.6,51.4",  # Birun Bashm District
        "36.6,51.4,36.7,51.5",  # Kordkheyl District
        "36.5,51.5,36.6,51.6"   # Hasankif District
    ]
}
tehran_district_bboxes = ["35.7500,51.3500,35.8000,51.4000",  # District 1
                "35.7000,51.3500,35.7500,51.4000",  # District 2
                "35.7500,51.3000,35.8000,51.3500",  # District 3
                "35.7000,51.3000,35.7500,51.3500",  # District 4
                "35.7500,51.4000,35.8000,51.4500",  # District 5
                "35.7000,51.4000,35.7500,51.4500",  # District 6
                "35.6500,51.3500,35.7000,51.4000",  # District 7
                "35.6500,51.4000,35.7000,51.4500",  # District 8
                "35.6500,51.4500,35.7000,51.5000",  # District 9
                "35.7000,51.4500,35.7500,51.5000",  # District 10
                "35.6000,51.3500,35.6500,51.4000",  # District 11
                "35.6000,51.4000,35.6500,51.4500",  # District 12
                "35.6500,51.3000,35.7000,51.3500",  # District 13
                "35.7000,51.5000,35.7500,51.5500",  # District 14
                "35.6500,51.5000,35.7000,51.5500",  # District 15
                "35.6000,51.4500,35.6500,51.5000",  # District 16
                "35.6000,51.3000,35.6500,51.3500",  # District 17
                "35.5500,51.3500,35.6000,51.4000",  # District 18
                "35.5500,51.4000,35.6000,51.4500",  # District 19
                "35.5500,51.4500,35.6000,51.5000",  # District 20
                "35.7500,51.4500,35.8000,51.5000",  # District 21
                "35.5500,51.3000,35.6000,51.3500"]   # District 22] 
contacts=['mobile','contact:phone','phone']
b_phrase= ['بوتاکس','متخصص پوست','ژل فیلر','دکتر پوست','مزوتراپی','هایفوتراپی','زیگل تناسلی','تزریق واژن','کاشت مو','لیزر مو','derm']
medical=["clinic","doctor",'doctors','Dermatologists']

def generate_grid(bbox, step=0.036):
    west, south, east, north = map(float, bbox.split(','))
    yield from (f"{lat/100},{lon/100},{(lat+step*100)/100},{(lon+step*100)/100}"
                for lat in range(int(south*100), int(north*100), int(step*100))
                for lon in range(int(west*100), int(east*100), int(step*100)))

def fetch_data(query):
    overpass_url = "http://192.168.1.7:12345/api/interpreter"
    response = requests.get(overpass_url, params={'data': query})
    j = {}
    if response.status_code == 200:
        try:
            j = response.json()
            jj = [elem for elem in j['elements'] if elem['type'] == 'node']
            # print(response.url)
            return jj
        except Exception as e:
            print("eer",e,response.url)
            return {}
    else:
        print(f"Error: {response.url}")
        return []

results = []
tehran_bbox = "35.5,51.2,35.8,51.6"

shits=[]
for cc in list(iran_city_districts.values()):
    for b in cc:
# for b in [*iran_city_bboxes,*tehran_district_bboxes]:
        for a in [*b_phrase,*medical] :
            for c in contacts:
                

                # 
                f=f""" [out:json];
        node[~"name"~"{a}"]["{c}"]({b});
        out center;"""
                ff = f"""[out:json];node["amenity"~"{a}"]["{c}"]({b});out center;"""
                doctors = [*fetch_data(f),*fetch_data(ff)]            
                for doctor in doctors:
                    try:
                        doc = {
                            "lat": doctor.get('lat', None) or doctor.get('center', {}).get('lat'),
                            "lon": doctor.get('lon', None) or doctor.get('center', {}).get('lon'),
                            "osm_id": doctor['id'],
                            "type": doctor['type'],
                            **doctor.get('tags', {})
                        }
                        results.append(doc)
                        for k in list(doc.keys()):
                            if'mobile' in k or 'phone' in k:
                                with open(f"returns/json3/{doc['osm_id']}.json", "w") as f:
                                    json.dump(doc, f, ensure_ascii=False)
                            else:
                                shits.append(k)
                    except Exception as e:
                        print(f"Error processing doctor: {e}")

        print(f"Total results: {len(results)}",set(shits))