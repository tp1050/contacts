from glob import glob
import json
from pathlib import Path

from numpy import sort
def getjs(path):
    files = glob(str(Path(path)/"*.json"))
    j=[]
    for f in files:
        try:
            j.append(json.loads(Path(f).read_text()))
        except:
            print(f"Failed to load {f}")
    return j
def get_tags(path="returns/json/"):
    keys=[]
    cd=dict()
    for j in getjs(path=path):
        keys.extend(list(j.keys()))
        for k in j.keys():
            
            cd.setdefault(k,0)
            cd[k]+=1
    
    return cd
# print(get_tags())

def get_sp():
    j=getjs(path="returns/json/")
    sp=[]
    for jj in j:
        sp.extend(str(jj.get("healthcare:speciality",None)).split(';'))
    return sp


def count_list(list1):
    cd = dict()
    for item in list1:
        cd[item] = cd.get(item,0) + 1
    cd2=dict(sorted(cd.items(), key=lambda item: item[1], reverse=True))
    return cd,cd2
# Path('r.json').write_text(str(count_list(get_sp())))


def big_j():
    ret={}
    j=getjs('returns/json3/')
    j.extend(getjs('returns/json2/'))
    j.extend(getjs('returns/json/'))
    for jj in j:ret.update(jj)
    return ret
def getHEALTH():
    ret=[]
    j=getjs('returns/json3/')
    j.extend(getjs('returns/json2/'))
    j.extend(getjs('returns/json/'))
    for jj in j:ret.extend(jj.get('healthcare:speciality',"").split(';'))
    return set(ret)
from collections import OrderedDict
big=big_j()
with open('r.json','w') as f:
    json.dump(big,f,ensure_ascii=False)
with open('keys.json','w') as f:
    json.dump(sorted(getHEALTH()),f,ensure_ascii=False)

