
import os
from jydraft import * 

def get_resource_abspath(filename) : 
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", filename)  

def main() :

    draft = JianyingDraft("My Video Project", width=1920, height=1080)
    video_track_id = draft.tracks[0]["id"]
    
    # Add video segments
    draft.add_video_segment(video_track_id, get_resource_abspath("space.mp4"), duration=5000000)
    draft.add_video_segment(video_track_id, get_resource_abspath("mc.mp4"), duration=5000000)
    draft.add_video_segment(video_track_id, get_resource_abspath("space.mp4"), duration=3000000)
    
    # Add audio
    draft.add_audio_segment(get_resource_abspath("fire.mp3"), duration = 5000000)
    
    # Save the draft
    draft.save_draft("./demo_draft")

if __name__ == "__main__" : 
    main()