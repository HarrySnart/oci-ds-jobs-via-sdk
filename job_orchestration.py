# load dependencies
import oci
import json

# defineconfig
config = oci.config.from_file()
signer = oci.signer.Signer(
    tenancy=config["tenancy"],
    user=config["user"],
    fingerprint=config["fingerprint"],
    private_key_file_location=config.get("key_file"),
    pass_phrase=oci.config.get_config_value_or_default(config, "pass_phrase"),
    private_key_content=config.get("key_content"),
)

# list items from object storage

def listBucketFiles(bucket_name,namespace, config,signer,prefix=None):
    ''' function to return list of files in object storage '''
    object_storage_client = oci.object_storage.ObjectStorageClient(config, signer=signer)

    if prefix != None:

        list_objects_response = object_storage_client.list_objects(
            namespace,
            bucket_name,
            prefix=prefix
        )


    else:
            list_objects_response = object_storage_client.list_objects(
            namespace,
            bucket_name)

    data = list_objects_response.data.objects

    files_list = []

    for i in range(1,len(data)):
        files_list.append(data[i].name)
        
    return files_list


bucket_name = '<your-oci-bucket>'
namespace = '<your-namespace>'
prefix = '<folder-prefix>'

files = listBucketFiles(bucket_name,namespace,config,signer,prefix=prefix)


# define data science job client
data_science_client = oci.data_science.DataScienceClient(config)

# set project and job ids
project_id = '<your-oci-data-science-project-id>'
job_id = '<your-oci-data-science-job-id>'
compartment_id = '<your-compartment-id>'

# function to trigger job run

def ociDSJobRun(file):
     ''' function to trigger oci data science job run with parameter input '''
     create_job_run_response = data_science_client.create_job_run(
    create_job_run_details=oci.data_science.models.CreateJobRunDetails(
        project_id=project_id,
        compartment_id=compartment_id,
        job_id=job_id,
        display_name="ran-from-python-sdk-demo",
        job_configuration_override_details=oci.data_science.models.DefaultJobConfigurationDetails(
            job_type="DEFAULT",
            environment_variables={
                'FILE': file}),freeform_tags = {'job_type':'python sdk run','file':file}))

# create jobs for each file
for file in files:
     print('creating OCI Data Science Job for ',file)
     ociDSJobRun(file)
