
__enzyme={
"access":"",
"addr":"address.street",
"address":"address.street",
"addr:city":"address.city",
"addr:country":"address.country",
"addr:floor":"address.street",
"addr:housenumber":"address.unit",
"addr:place":"address.unit",
"addr:postcode":"address.postcode",
"addr:street":"address.street",
"addr:unit":"address.unit",
"air_conditioning":"",
"amenity":"category",
"aparat":"url",
"building":"address.street",
"contact:aparat":"url",
"contact:email":"url",
"contact:instagram":"url",
"contact:linkedin":"url",
"contact:mobile":"phone",
"contact:phone":"phone",
"contact:website":"url",
"contact:youtube":"url",
"description":"note",
"dispensing":"",
"ele":"",
"email":"email",
"emergency":"",
"fax":"phone",
"healthcare":"healthcare",
"healthcare:speciality":"category",
"image":"photo",
"instagram":"url",
"internet_access":"",
"internet_access:fee":"",
"lat":"lat",
"level":"address.unit",
"lon":"lon",
"mobile":"phone",
"name":"name.fullname",
"name:ang":"name.name-en",
"name:ar":"name.fullname",
"name:az-Latn":"name.name-en",
"name:en":"name.name-en",
"name:fa":"name.fullname",
"name:hi-Latn":"name.name-en",
"note":"note",
"office":"note",
"opening_hours":"opening_hours",
"operator":"",
"operator:type":"",
"osm_id":"osm_id",
"parking":"",
"payment:cards":"",
"payment:cash":"",
"payment:credit_cards":"",
"payment:debit_cards":"",
"payment:mastercard":"",
"payment:visa":"",
"phone":"phone",
"photo":"photo",
"public":"",
"shop":"category",
"source":"",
"start_date":"",
"type":"",
"unit":"address.unit",
"website":"url",
"whatsapp":"phone",
"instagram":"url",
"telegram":"phone",
"wheelchair":"",
}
from pathlib import Path
import json 
from zto3.vcf.fvcf import OSM_VCF
from glob import glob
for f in glob('returns/json3/*.json'):
    j=json.loads(Path(f).read_text())
    s=str(OSM_VCF(__enzyme,**j))
    if len(s)>1:Path(f'vcf/{j['osm_id']}.vcf').write_text(s)

# j=json.loads(Path('r.json').read_text())
# Path('some.vcf').write_text(str(OSM_VCF(__enzyme,**j)))
# print(OSM_VCF(__enzyme,**j))