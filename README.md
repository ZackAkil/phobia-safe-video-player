# phobia-safe-video-player
A video player that will not show things that could trigger a phobia. Using Google Cloud Video Intelligence API 

``` bash
 gcloud ml video detect-labels gs://scary-videos/5-generation-bakers.mp4 --async --detection-mode=frame --region=europe-west1 --output-uri="gs://scary-videos/output.json"
```