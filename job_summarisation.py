# load dependencies
import json
import pandas as pd
import os

# run oci-cli job

os.system('oci data-science job-run list --compartment-id  $compartmentid  >> results.json')

# read json
dat = pd.read_json('results.json')


compartment_id = []
created_by = []
freeform_tags = []
id = []
lifecycle_state = []
lifecycle_details = []
display_name = []
project_id = []
time_created = []
time_started = []
time_finished = []
file = []
job_type = []

# parse results
for i in range(len(dat)):
    try:
        created_by.append(dat['data'][i]['created-by'])
        
    except:
        created_by.append('')
    try: 
        freeform_tags.append(dat['data'][i]['freeform-tags'])
    except:
        freeform_tags.append('')
        
    try:
        file.append(dat['data'][i]['freeform-tags']['file'])
    except:
        file.append('')
    
    try:
        job_type.append(dat['data'][i]['freeform-tags']['job_type'])
    except:
        job_type.append('')        
    try:
        id.append(dat['data'][i]['id'])
    except:
        id.append('')
        
    try:
        lifecycle_state.append(dat['data'][i]['lifecycle-state'])
    except:
        lifecycle_state.append('')
    try: 
        project_id.append(dat['data'][i]['project-id'])
        
    except:
        project_id.append('')
    try:
        time_created.append(dat['data'][i]['time-created'])
    except:
        time_created.append('')
    try:
        time_started.append(dat['data'][i]['time-started'])
    except:
        time_started.append('')
    try:
        time_finished.append(dat['data'][i]['time-finished'])
    except:
        time_finished.append('')
    try:
        
        display_name.append(dat['data'][i]['display-name'])
    except:
        display_name.append('')
    
    try:
        lifecycle_details.append(dat['data'][i]['lifecycle-details'])
    except:
        lifecycle_details.append('')
        
results = pd.DataFrame({'project_id':project_id,'id':id,'display_name':display_name,'created_by':created_by,'time_created':time_created,'time_started':time_started,'time_finished':time_finished,'lifecycle_state':lifecycle_state,'freeform_tags':freeform_tags,'file':file,'job_type':job_type})

filterred_results =  results[results['job_type']!='']
filterred_results.to_csv('results.csv',index=False)

# drop json file
os.system('rm results.json')