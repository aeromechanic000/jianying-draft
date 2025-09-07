import os, time, json, uuid
from pathlib import Path
# from moviepy.editor import VideoFileClip
from moviepy import VideoFileClip


def generate_uuid():
    return str(uuid.uuid4()).upper()

def make_material(path):
    clip = VideoFileClip(path)
    mat = {
        "id": generate_uuid(),
        "path": path,
        "width": clip.w,
        "height": clip.h,
        "duration": int(clip.duration * 1_000_000)
    }
    clip.close()
    return mat

def write_json_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class DraftProject:
    def __init__(self, output_dir, materials):
        self.output_dir = Path(output_dir)
        self.draft_id = generate_uuid()
        self.materials = materials  # list of dicts with keys: id, path, width, height, duration
        self.tracks = []

    def save(self) :
        self.output_dir.mkdir(parents=True, exist_ok=True)
        if self.meta_info is not None : 
            write_json_file(self.output_dir / "draft_meta_info.json", self.meta_info)
            write_json_file(self.output_dir / "draft_virtual_store.json", self.virtual_store)
            write_json_file(self.output_dir / "draft_content.json", self.content)
            write_json_file(self.output_dir / "attachment_editing.json", {
                "edit_type": 0,
                "version": "1.0.0"
            })
            write_json_file(self.output_dir / "draft_agency_config.json", {
                "use_converter": False,
                "video_resolution": 720
            })
        else : 
            print("You need to generate content before saving.")

    def create_draft(self):
        # 1. draft_meta_info.json
        self.meta_info = self.generate_meta_info()

        # 2. draft_virtual_store.json
        material_ids = [m["id"] for m in self.materials]
        self.virtual_store = self.generate_virtual_store(material_ids)

        # 3. draft_content.json
        self.content = self.generate_draft_content(material_ids)

    def generate_meta_info(self):
        timestamp = int(time.time())
        return {
            "draft_id": self.draft_id,
            "draft_fold_path": str(self.output_dir),
            "draft_cover": "draft_cover.jpg",
            "draft_is_from_deeplink": "false",
            "draft_is_ai_packaging_used": False,
            "draft_is_ai_translate": False,
            "draft_materials": [
                {
                    "type": 0,
                    "value": [
                        {
                            "id": mat["id"],
                            "file_Path": mat["path"],
                            "width": mat["width"],
                            "height": mat["height"],
                            "duration": mat["duration"],
                            "create_time": timestamp,
                            "import_time": timestamp,
                            "item_source": 1,
                            "md5": "",
                            "metetype": "video",
                            "roughcut_time_range": {
                                "start": 0,
                                "duration": mat["duration"]
                            },
                            "extra_info": os.path.basename(mat["path"])
                        }
                        for mat in self.materials
                    ]
                }
            ]
        }

    def generate_virtual_store(self, material_ids):
        return {
            "draft_materials": [],
            "draft_virtual_store": [
                {"type": 0, "value": []},
                {"type": 1, "value": [{"child_id": mid, "parent_id": ""} for mid in material_ids]},
                {"type": 2, "value": []}
            ]
        }

    def generate_draft_content(self, material_ids):
        # We only use the first material to create one track segment
        material_id = material_ids[0]
        return {
            "canvas_config": {"width": 1080, "height": 1920, "ratio": "9:16"},
            "fps": 30.0,
            "duration": 5000000,
            "tracks": [
                {
                    "type": "video",
                    "id": generate_uuid(),
                    "segments": [
                        {
                            "material_id": material_id,
                            "source_timerange": {"start": 0, "duration": 5000000},
                            "target_timerange": {"start": 0, "duration": 5000000},
                            "volume": 1.0,
                            "speed": 1.0,
                            "visible": True,
                            "clip": {
                                "scale": {"x": 1.0, "y": 1.0},
                                "transform": {"x": 0.0, "y": 0.0},
                                "alpha": 1.0,
                                "rotation": 0.0,
                                "flip": {"horizontal": False, "vertical": False}
                            }
                        }
                    ]
                }
            ]
        }

    def add_track(self, track_type="video"):
        track_id = generate_uuid()
        track = {
            "type": track_type,
            "id": track_id,
            "segments": []
        }
        self.tracks.append(track)
        return track_id

    def add_segment(self, track_id, material_id, start=0, duration=None, speed=1.0):
        material = next((m for m in self.materials if m["id"] == material_id), None)
        if not material:
            raise ValueError(f"Material {material_id} not found")

        if duration is None:
            duration = material["duration"]

        segment = {
            "material_id": material_id,
            "source_timerange": {"start": start, "duration": duration},
            "target_timerange": {"start": 0, "duration": int(duration / speed)},
            "volume": 1.0,
            "speed": speed,
            "visible": True,
            "clip": {
                "scale": {"x": 1.0, "y": 1.0},
                "transform": {"x": 0.0, "y": 0.0},
                "alpha": 1.0,
                "rotation": 0.0,
                "flip": {"horizontal": False, "vertical": False}
            }
        }

        for track in self.tracks:
            if track["id"] == track_id:
                track["segments"].append(segment)
                return

        raise ValueError(f"Track {track_id} not found")

    def get_track_ids(self, track_type=None):
        if track_type:
            return [t["id"] for t in self.tracks if t["type"] == track_type]
        return [t["id"] for t in self.tracks]

    def generate_draft_content(self, material_ids=None):
        total_duration = sum(
            s["target_timerange"]["duration"]
            for t in self.tracks for s in t["segments"]
        ) or 5_000_000

        return {
            "canvas_config": {"width": 1080, "height": 1920, "ratio": "9:16"},
            "fps": 30.0,
            "duration": total_duration,
            "tracks": self.tracks
        }

