import os
import ads
import oci
import pandas as pd
from ads.common.auth import default_signer

''' A very simple BYOC Job to move single CSV files from one directory to another. '''

# get file name
file = os.getenv('FILE')

print('starting job for file:',file)

# setup auth
ads.set_auth(auth='resource_principal')
bucket_name = '<your-oci-bucket>'
namespace = '<your-namespace>'

# load object
data = pd.read_csv(f"oci://{bucket_name}@{namespace}/{file}", storage_options=default_signer())

# write object back to different directory
file_out = file.replace('data','test')
data.to_csv(f"oci://{bucket_name}@{namespace}/{file_out}", index=False, storage_options=default_signer())

print('end of job for file:',file)