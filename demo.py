
from jydraft import * 

def main() :

    materials = [
        make_material(os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips/space.mp4")),
        make_material(os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips/mc.mp4")),
    ]

    project = DraftProject("demo", materials)
    project.create_draft()

    video_track = project.add_track("video")

    for mat in materials:
        project.add_segment(
            track_id=video_track,
            material_id=mat["id"],
            start=0,
            duration=mat["duration"],
            speed=1.0
        )

    project.save()

if __name__ == "__main__" : 
    main()