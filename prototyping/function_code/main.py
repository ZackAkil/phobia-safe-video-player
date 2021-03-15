
import json

from google.cloud import storage
from google.cloud.video import transcoder

from Annotations_util import get_segments_for_labels
from Transcoder_utils import create_fade_overlay_segment, create_video_overlay_job, create_static_overlay_segment


OUTPUT_BUCKET = 'gs://scary-videos-fixed/'
parent_location ='projects/320823659895/locations/europe-west1'

transcoder_client = transcoder.TranscoderServiceClient()
storage_client = storage.Client()


def create_safe_video(event, context):
    
    file_name = event['name']
    bucket_name = event['bucket']
    print(file_name)
    
    # split the fears off the end of the file name name after 🙈 and separate on '&'    
    fears = set(file_name.split('.')[-2].split('🙈')[-1].split('+'))
    print('look for fears', fears)
    fears = set({'bird'})
    
    annotaion_bucket = storage_client.get_bucket(bucket_name)
    
    # downalod annotations from GCS     
    source_blob_name = file_name
    blob = annotaion_bucket.blob(source_blob_name)
    text = blob.download_as_string()
    annotation_results = json.loads(text)
    
    # get original file name     
    input_uri = 'gs:/' + annotation_results['annotation_results'][0]['input_uri']
    file_name = input_uri.split('/')[-1].split('.')[0]
    
    
    # print(annotation_results)
    segments = get_segments_for_labels(fears, annotation_results['annotation_results'][0]['shot_label_annotations'])
    
    print(segments)
    
    
    # create all the overlay segments     
    overlay_segments = []
    for seg in segments:
        overlay_segments += create_static_overlay_segment(*seg)
    
    print(overlay_segments)
    
    job = create_video_overlay_job(input_url=input_uri, 
                                   output_folder=OUTPUT_BUCKET, 
                                   output_file_name=file_name, 
                                   overlay_segments = overlay_segments)

    job_request = transcoder.CreateJobRequest(parent = parent_location, job = job)
    
    transcoder_client.create_job(job_request)
    
