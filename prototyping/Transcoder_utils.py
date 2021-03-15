
from google.cloud.video import transcoder
from google.protobuf.duration_pb2 import Duration


OVERLAY_IMAGE_URI = 'gs://scary-videos/no_see.jpg'

# create overlay image object
no_see_image = transcoder.Overlay.Image(
    uri = OVERLAY_IMAGE_URI, 
    alpha=1, 
    resolution= transcoder.Overlay.NormalizedCoordinate(x=1., y=1.)
)


def get_nanos_from_seconds(seconds):
    return int ((seconds - int(seconds)) / 1e-9) 

def create_static_overlay_segment(start_time_seconds, end_time_seconds):
    
    animation_start = transcoder.Overlay.Animation()
    animation_start.animation_static = transcoder.Overlay.AnimationStatic()
    animation_start.animation_static.start_time_offset = Duration(seconds = int(start_time_seconds), 
                                                                  nanos = get_nanos_from_seconds(start_time_seconds) )
    animation_start.animation_static.xy = transcoder.Overlay.NormalizedCoordinate(x=0., y=0.)
    animation_start
    
    animation_end = transcoder.Overlay.Animation()
    animation_end.animation_end = transcoder.Overlay.AnimationEnd()
    animation_end.animation_end.start_time_offset = Duration(seconds = int(end_time_seconds), 
                                                             nanos = get_nanos_from_seconds(end_time_seconds))
    animation_end
    
    return [animation_start, animation_end]


def create_fade_overlay_segment(start_time_seconds, end_time_seconds, fade_duration = 0.5):
    
    # create fade in animation     
    animation_start = transcoder.Overlay.Animation()
    animation_start.animation_fade = transcoder.Overlay.AnimationFade()
    
    animation_start.animation_fade.start_time_offset = Duration(seconds = int(start_time_seconds - fade_duration), 
                                                                nanos = get_nanos_from_seconds(start_time_seconds - fade_duration) )
    
    animation_start.animation_fade.end_time_offset = Duration(seconds = int(start_time_seconds ), 
                                                                nanos = get_nanos_from_seconds(start_time_seconds))
    
    animation_start.animation_fade.fade_type = transcoder.Overlay.FadeType.FADE_IN
    animation_start.animation_fade.xy = transcoder.Overlay.NormalizedCoordinate(x=0., y=0.)
    
    
    # create fade out animation  
    animation_end = transcoder.Overlay.Animation()
    animation_end.animation_fade = transcoder.Overlay.AnimationFade()
    animation_end.animation_fade.start_time_offset = Duration(seconds = int(end_time_seconds), 
                                                              nanos = get_nanos_from_seconds(end_time_seconds))
    
    animation_end.animation_fade.end_time_offset = Duration(seconds = int(end_time_seconds + fade_duration), 
                                                            nanos = get_nanos_from_seconds(end_time_seconds + fade_duration))
    animation_end.animation_fade.fade_type = transcoder.Overlay.FadeType.FADE_OUT
    
    animation_end.animation_fade.xy = transcoder.Overlay.NormalizedCoordinate(x=0., y=0.)
    
    
    return [animation_start, animation_end]


def create_video_overlay_job(input_url, output_folder, output_file_name, overlay_segments):

    # creaet overlays     
    overlay = transcoder.Overlay(image = no_see_image)
    overlay.animations = overlay_segments
    
    # create job configuration     
    job_config = transcoder.JobConfig()
    job_config.overlays = [overlay]
    
    # get video stream     
    elementary_video_stream = transcoder.ElementaryStream()
    elementary_video_stream.key = 'video1'
    elementary_video_stream.video_stream = transcoder.VideoStream(frame_rate=30, bitrate_bps=550000)
    
    # get audio stream     
    elementary_audio_stream = transcoder.ElementaryStream()
    elementary_audio_stream.key = 'audio1'
    elementary_audio_stream.audio_stream = transcoder.AudioStream(bitrate_bps=64000)
    
    # include video and audio streams     
    job_config.elementary_streams = [elementary_video_stream, elementary_audio_stream]
   
    # create output video + audio     
    mux_stream = transcoder.MuxStream(
        key = output_file_name,
        elementary_streams = ['video1', 'audio1']
    )
    job_config.mux_streams = [mux_stream]
    
    # create job     
    job = transcoder.Job()
    job.input_uri = input_url
    job.output_uri = output_folder
    job.config = job_config
    
    return job
    
