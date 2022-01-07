import json
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def daterange(start_date, end_date):
    ldt=[]
    for n in range(int((end_date - start_date).days)):
        ldt.append(start_date + timedelta(n))

    for n in ldt[::3]:
        yield n


three_months = date.today() - relativedelta(months=3)

stats_start_date = three_months
stats_end_date = date.today()

list_pair_days=[]
for single_date in daterange(stats_start_date, stats_end_date + relativedelta(days=3)):
    start_date = single_date.strftime("%Y-%m-%d")
    end_date=single_date + relativedelta(days=2)
    list_pair_days.append(start_date + " --endtime " + end_date.strftime("%Y-%m-%d"))


with open('metrics.json') as f:
  data = json.load(f)

print ("rm *tab")

hostname= []
for d in data:
    hostname.append(d['dimensions']['hostname'])

unique_hostname=list(set(hostname))


for i in data:
    keys=[]
    
    if 'hostname' in i['dimensions']:
        keys.append("hostname="+i['dimensions']['hostname'])
    if 'device' in i['dimensions']:
        keys.append("device="+i['dimensions']['device'])

    with open('run__' + i['dimensions']['hostname'],"a+") as f:
        for pair_day in list_pair_days:
            f.write ("echo \"# monasca measurement-list "+ i['name'] +" "+ pair_day +" --dimensions " + ",".join(keys) + " | sed -e '1,3d' |  awk -F\| '{print "+"\$"+"4, "+"\$"+"5}' |  sed '"+"\$"+"d' >> " + "__".join(keys).replace("=","__")+"__"+i['name'] + ".tab\"\n")    
            f.write ("monasca measurement-list "+ i['name'] +" "+pair_day+" --dimensions " + ",".join(keys) + " | sed -e '1,3d' |  awk -F\| '{print "+"$"+"4, "+"$" +"5}' | sed '"+ "$" +"d'  >> " + "__".join(keys).replace("=","__")+"__"+i['name'] + ".tab\n" )

