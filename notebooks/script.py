from esgf_stac_client.client import ESGFStacClient
import json

client = ESGFStacClient.open("https://api.stac.ceda.ac.uk")
instance_id = "CMIP6.HighResMIP.MOHC.HadGEM3-GC31-HH.highres-future.r1i1p1f1.day.tas.gn.v20191105"
res = client.search(instance_id=instance_id)
item = next(res.items())

with open('test_item.json', 'w') as f:
    f.write(json.dumps(item.to_dict()))
