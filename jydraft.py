# jianying_draft.py

import json
import uuid
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class TimeRange:
    duration: int
    start: int = 0

@dataclass
class Transform:
    x: float = 0.0
    y: float = 0.0

@dataclass
class Scale:
    x: float = 1.0
    y: float = 1.0

@dataclass
class Flip:
    horizontal: bool = False
    vertical: bool = False

@dataclass
class Clip:
    alpha: float = 1.0
    flip: Flip = None
    rotation: float = 0.0
    scale: Scale = None
    transform: Transform = None
    
    def __post_init__(self):
        if self.flip is None:
            self.flip = Flip()
        if self.scale is None:
            self.scale = Scale()
        if self.transform is None:
            self.transform = Transform()

class JianyingDraft:
    def __init__(self, name: str = "New Project", width: int = 1920, height: int = 1080, fps: float = 30.0):
        self.name = name
        self.width = width
        self.height = height
        self.fps = fps
        self.draft_id = str(uuid.uuid4()).upper()
        self.project_id = str(uuid.uuid4()).upper()
        
        # Initialize basic structure
        self.materials = {
            "videos": [],  # For videos and photos
            "audios": [],  # For audio/music files
        }
        self.tracks = []
        self.duration = 0
        
        # Create default video track
        self.add_track("video")
    
    def add_video_material(self, file_path: str, duration: Optional[int] = None, 
                          width: Optional[int] = None, height: Optional[int] = None) -> str:
        """Add a video material"""
        material_id = str(uuid.uuid4()).lower().replace("-", "")
        current_time = int(time.time())
        
        ext = Path(file_path).suffix.lower()
        is_video = ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        
        if not is_video:
            raise ValueError(f"File {file_path} is not a video file. Use add_image_material() for images.")
        
        # Default duration for videos (should be detected from actual file)
        if duration is None:
            duration = 10000000  # 10 seconds default
        
        if width is None:
            width = 1920
        if height is None:
            height = 1080
        
        material = {
            "id": material_id,
            "file_Path": file_path,
            "duration": duration,
            "width": width,
            "height": height,
            "type": 0,
            "metetype": "video",
            "create_time": current_time,
            "import_time": current_time,
            "import_time_ms": current_time * 1000000,
            "extra_info": Path(file_path).name,
            "item_source": 1,
            "md5": "",
            "roughcut_time_range": {"duration": duration, "start": 0},
            "sub_time_range": {"duration": -1, "start": -1}
        }
        
        # Add to draft_info materials
        video_material = {
            "aigc_type": "none",
            "audio_fade": None,
            "cartoon_path": "",
            "category_id": "",
            "category_name": "",
            "check_flag": 63487,
            "crop": {
                "lower_left_x": 0.0, "lower_left_y": 1.0,
                "lower_right_x": 1.0, "lower_right_y": 1.0,
                "upper_left_x": 0.0, "upper_left_y": 0.0,
                "upper_right_x": 1.0, "upper_right_y": 0.0
            },
            "crop_ratio": "free",
            "crop_scale": 1.0,
            "duration": duration,
            "extra_type_option": 0,
            "formula_id": "",
            "freeze": None,
            "gameplay": None,
            "has_audio": True,  # Videos typically have audio
            "height": height,
            "id": material_id.upper(),
            "intensifies_audio_path": "",
            "intensifies_path": "",
            "is_ai_generate_content": False,
            "is_copyright": False,
            "is_unified_beauty_mode": False,
            "local_id": "",
            "local_material_id": "",
            "material_id": "",
            "material_name": Path(file_path).name,
            "material_url": "",
            "matting": {
                "flag": 0,
                "has_use_quick_brush": False,
                "has_use_quick_eraser": False,
                "interactiveTime": [],
                "path": "",
                "strokes": []
            },
            "media_path": "",
            "object_locked": None,
            "origin_material_id": "",
            "path": file_path,
            "picture_from": "none",
            "picture_set_category_id": "",
            "picture_set_category_name": "",
            "request_id": "",
            "reverse_intensifies_path": "",
            "reverse_path": "",
            "smart_motion": None,
            "source": 0,
            "source_platform": 0,
            "stable": {
                "matrix_path": "",
                "stable_level": 0,
                "time_range": {"duration": 0, "start": 0}
            },
            "team_id": "",
            "type": "video",
            "video_algorithm": {
                "algorithms": [],
                "deflicker": None,
                "motion_blur_config": None,
                "noise_reduction": None,
                "path": "",
                "quality_enhance": None,
                "time_range": None
            },
            "width": width
        }
        
        self.materials["videos"].append({
            "meta": material,
            "draft_info": video_material
        })
        
        return material_id.upper()
    
    def add_image_material(self, file_path: str, duration: Optional[int] = None, 
                          width: Optional[int] = None, height: Optional[int] = None) -> str:
        """Add an image/photo material"""
        material_id = str(uuid.uuid4()).lower().replace("-", "")
        current_time = int(time.time())
        
        ext = Path(file_path).suffix.lower()
        is_image = ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
        
        if not is_image:
            raise ValueError(f"File {file_path} is not an image file. Use add_video_material() for videos.")
        
        # Default duration for images (5 seconds)
        if duration is None:
            duration = 5000000  # 5 seconds
        
        # Default dimensions (should be detected from actual image)
        if width is None:
            width = 1920
        if height is None:
            height = 1080
        
        material = {
            "id": material_id,
            "file_Path": file_path,
            "duration": duration,
            "width": width,
            "height": height,
            "type": 0,
            "metetype": "photo",
            "create_time": current_time,
            "import_time": current_time,
            "import_time_ms": current_time * 1000000,
            "extra_info": Path(file_path).name,
            "item_source": 1,
            "md5": "",
            "roughcut_time_range": {"duration": -1, "start": -1},
            "sub_time_range": {"duration": -1, "start": -1}
        }
        
        # Add to draft_info materials
        image_material = {
            "aigc_type": "none",
            "audio_fade": None,
            "cartoon_path": "",
            "category_id": "",
            "category_name": "",
            "check_flag": 63487,
            "crop": {
                "lower_left_x": 0.0, "lower_left_y": 1.0,
                "lower_right_x": 1.0, "lower_right_y": 1.0,
                "upper_left_x": 0.0, "upper_left_y": 0.0,
                "upper_right_x": 1.0, "upper_right_y": 0.0
            },
            "crop_ratio": "free",
            "crop_scale": 1.0,
            "duration": 10800000000,  # Very large duration for images (3 hours)
            "extra_type_option": 0,
            "formula_id": "",
            "freeze": None,
            "gameplay": None,
            "has_audio": False,  # Images don't have audio
            "height": height,
            "id": material_id.upper(),
            "intensifies_audio_path": "",
            "intensifies_path": "",
            "is_ai_generate_content": False,
            "is_copyright": False,
            "is_unified_beauty_mode": False,
            "local_id": "",
            "local_material_id": "",
            "material_id": "",
            "material_name": Path(file_path).name,
            "material_url": "",
            "matting": {
                "flag": 0,
                "has_use_quick_brush": False,
                "has_use_quick_eraser": False,
                "interactiveTime": [],
                "path": "",
                "strokes": []
            },
            "media_path": "",
            "object_locked": None,
            "origin_material_id": "",
            "path": file_path,
            "picture_from": "none",
            "picture_set_category_id": "",
            "picture_set_category_name": "",
            "request_id": "",
            "reverse_intensifies_path": "",
            "reverse_path": "",
            "smart_motion": None,
            "source": 0,
            "source_platform": 0,
            "stable": {
                "matrix_path": "",
                "stable_level": 0,
                "time_range": {"duration": 0, "start": 0}
            },
            "team_id": "",
            "type": "photo",
            "video_algorithm": {
                "algorithms": [],
                "deflicker": None,
                "motion_blur_config": None,
                "noise_reduction": None,
                "path": "",
                "quality_enhance": None,
                "time_range": None
            },
            "width": width
        }
        
        self.materials["videos"].append({
            "meta": material,
            "draft_info": image_material
        })
        
        return material_id.upper()
    
    def add_material(self, file_path: str, material_type: str = "auto", duration: Optional[int] = None,
                    width: Optional[int] = None, height: Optional[int] = None) -> str:
        """Add any type of material (auto-detects type or use specified type)"""
        if material_type == "auto":
            ext = Path(file_path).suffix.lower()
            if ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                return self.add_video_material(file_path, duration, width, height)
            elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
                return self.add_image_material(file_path, duration, width, height)
            elif ext in ['.mp3', '.wav', '.aac', '.m4a']:
                return self.add_audio_material(file_path, duration)
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        elif material_type == "video":
            return self.add_video_material(file_path, duration, width, height)
        elif material_type == "image" or material_type == "photo":
            return self.add_image_material(file_path, duration, width, height)
        elif material_type == "audio" or material_type == "music":
            return self.add_audio_material(file_path, duration)
        else:
            raise ValueError(f"Unknown material type: {material_type}")
    
    def add_audio_material(self, file_path: str, duration: Optional[int] = None, 
                          music_id: str = None, name: str = None) -> str:
        """Add an audio/music material with proper JianyingPro structure"""
        material_id = str(uuid.uuid4()).upper()
        current_time = int(time.time())
        
        if duration is None:
            duration = 28000000  # Default 28 seconds, should be detected from actual file
        
        if music_id is None:
            music_id = str(int(time.time() * 1000000))  # Generate a unique music ID
        
        if name is None:
            name = Path(file_path).stem
        
        # Structure for draft_meta_info.json
        meta_material = {
            "id": material_id,
            "file_Path": file_path,
            "duration": duration,
            "height": 0,
            "width": 0,
            "type": 8,
            "metetype": "none",
            "create_time": current_time,
            "import_time": current_time,
            "import_time_ms": current_time * 1000000,
            "extra_info": json.dumps({
                "musicPanelType": "musictype_audio",
                "resouceType": "Local_Import",
                "resourceID": music_id,
                "signHeader": False,
                "url": file_path
            }, separators=(',', ': ')),
            "item_source": 1,
            "md5": "",
            "roughcut_time_range": {"duration": -1, "start": -1},
            "sub_time_range": {"duration": -1, "start": -1}
        }
        
        # Structure for draft_info.json materials.audios
        draft_info_material = {
            "app_id": 1775,
            "category_id": "local_music",
            "category_name": "local_music",
            "check_flag": 1,
            "duration": duration,
            "effect_id": "",
            "formula_id": "",
            "id": material_id,
            "intensifies_path": "",
            "is_ugc": False,
            "local_material_id": "",
            "music_id": music_id,
            "name": name,
            "path": file_path,
            "query": "",
            "request_id": "",
            "resource_id": "",
            "search_id": "",
            "source_platform": 0,
            "team_id": "",
            "text_id": "",
            "tone_category_id": "",
            "tone_category_name": "",
            "tone_effect_id": "",
            "tone_effect_name": "",
            "tone_speaker": "",
            "tone_type": "",
            "type": "music",
            "video_id": "",
            "wave_points": []
        }
        
        self.materials["audios"].append({
            "meta": meta_material,
            "draft_info": draft_info_material
        })
        
        return material_id
    
    def add_track(self, track_type: str = "video") -> str:
        """Add a new track and return its ID"""
        track_id = str(uuid.uuid4()).upper()
        
        track = {
            "id": track_id,
            "type": track_type,
            "attribute": 0,
            "flag": 0,
            "is_default_name": True,
            "name": "",
            "segments": []
        }
        
        self.tracks.append(track)
        return track_id
    
    def add_segment_to_track(self, track_id: str, material_id: str, start_time: int = 0, 
                           duration: Optional[int] = None, scale: float = 1.0,
                           transform_x: float = 0.0, transform_y: float = 0.0) -> str:
        """Add a segment to a specific track"""
        segment_id = str(uuid.uuid4()).upper()
        
        # Find the material
        material = None
        material_type = None
        
        # Check video materials (includes both videos and images)
        for mat in self.materials["videos"]:
            if mat["draft_info"]["id"] == material_id:
                material = mat["draft_info"]
                material_type = "video"
                break
        
        # Check audio materials
        if not material:
            for mat in self.materials["audios"]:
                if mat["draft_info"]["id"] == material_id:
                    material = mat["draft_info"]
                    material_type = "audio"
                    break
        
        if not material:
            raise ValueError(f"Material with ID {material_id} not found")
        
        # For images, use the provided duration, for videos use actual or provided duration
        if material["type"] == "photo":
            if duration is None:
                duration = 5000000  # Default 5 seconds for images
            source_duration = duration
        else:
            if duration is None:
                duration = material["duration"]
            source_duration = duration
        
        # Find the track
        track = None
        for t in self.tracks:
            if t["id"] == track_id:
                track = t
                break
        
        if not track:
            raise ValueError(f"Track with ID {track_id} not found")
        
        # Calculate position on timeline
        if track["segments"]:
            last_segment = max(track["segments"], 
                             key=lambda s: s["target_timerange"]["start"] + s["target_timerange"]["duration"])
            timeline_start = (last_segment["target_timerange"]["start"] + 
                            last_segment["target_timerange"]["duration"])
        else:
            timeline_start = 0
        
        # Generate supporting materials
        speed_id = str(uuid.uuid4()).upper()
        canvas_id = str(uuid.uuid4()).upper()
        sound_mapping_id = str(uuid.uuid4()).upper()
        vocal_sep_id = str(uuid.uuid4()).upper()
        material_animation_id = str(uuid.uuid4()).upper()
        
        extra_material_refs = [speed_id, canvas_id, sound_mapping_id, vocal_sep_id]
        if material["type"] == "photo":
            extra_material_refs.append(material_animation_id)
        
        # Base segment structure
        segment = {
            "id": segment_id,
            "material_id": material_id,
            "source_timerange": {"start": start_time, "duration": source_duration},
            "target_timerange": {"start": timeline_start, "duration": duration},
            "speed": 1.0,
            "visible": True,
            "volume": 1.0,
            "cartoon": False,
            "common_keyframes": [],
            "enable_adjust": track["type"] == "video",
            "enable_color_curves": True,
            "enable_color_match_adjust": False,
            "enable_color_wheels": True,
            "enable_lut": track["type"] == "video",
            "enable_smart_color_adjust": False,
            "extra_material_refs": extra_material_refs,
            "group_id": "",
            "intensifies_audio": False,
            "is_placeholder": False,
            "is_tone_modify": False,
            "keyframe_refs": [],
            "last_nonzero_volume": 1.0,
            "render_index": 0,
            "responsive_layout": {
                "enable": False,
                "horizontal_pos_layout": 0,
                "size_layout": 0,
                "target_follow": "",
                "vertical_pos_layout": 0
            },
            "reverse": False,
            "template_id": "",
            "template_scene": "default",
            "track_attribute": 0,
            "track_render_index": 0,
            "uniform_scale": {"on": True, "value": 1.0} if track["type"] == "video" else None
        }
        
        # Add clip properties for video segments
        if track["type"] == "video":
            segment["clip"] = {
                "alpha": 1.0,
                "flip": {"horizontal": False, "vertical": False},
                "rotation": 0.0,
                "scale": {"x": scale, "y": scale},
                "transform": {"x": transform_x, "y": transform_y}
            }
            segment["hdr_settings"] = {"intensity": 1.0, "mode": 1, "nits": 1000}
        else:
            segment["clip"] = None
            segment["hdr_settings"] = None
        
        track["segments"].append(segment)
        
        # Update total duration
        new_end = timeline_start + duration
        if new_end > self.duration:
            self.duration = new_end
        
        return segment_id
    
    def add_video_segment(self, track_id: str, video_path: str, start_time: int = 0, 
                         duration: Optional[int] = None, scale: float = 1.0,
                         transform_x: float = 0.0, transform_y: float = 0.0) -> str:
        """Convenience method to add a video segment"""
        material_id = self.add_video_material(video_path, duration)
        return self.add_segment_to_track(track_id, material_id, start_time, duration, scale, transform_x, transform_y)
    
    def add_image_segment(self, track_id: str, image_path: str, duration: int = 5000000,
                         scale: float = 1.0, transform_x: float = 0.0, transform_y: float = 0.0) -> str:
        """Convenience method to add an image segment"""
        material_id = self.add_image_material(image_path, duration)
        return self.add_segment_to_track(track_id, material_id, 0, duration, scale, transform_x, transform_y)
    
    def add_audio_segment(self, audio_path: str, start_time: int = 0, 
                         duration: Optional[int] = None, track_id: str = None) -> str:
        """Convenience method to add an audio segment"""
        if track_id is None:
            track_id = self.add_track("audio")
        material_id = self.add_audio_material(audio_path, duration)
        return self.add_segment_to_track(track_id, material_id, start_time, duration)
    
    def generate_draft_meta_info(self) -> Dict[str, Any]:
        """Generate the draft_meta_info.json structure"""
        current_time = int(time.time() * 1000000)  # microseconds
        
        draft_materials = []
        
        # Videos and photos (type 0)
        video_materials = [mat["meta"] for mat in self.materials["videos"]]
        draft_materials.append({"type": 0, "value": video_materials})
        
        # Empty categories (types 1, 3, 6, 7)
        for i in [1, 3, 6, 7]:
            draft_materials.append({"type": i, "value": []})
        
        # Audio materials (type 8)
        audio_materials = [mat["meta"] for mat in self.materials["audios"]]
        draft_materials.append({"type": 8, "value": audio_materials})
        
        return {
            "cloud_package_completed_time": "",
            "draft_cloud_capcut_purchase_info": "",
            "draft_cloud_last_action_download": False,
            "draft_cloud_materials": [],
            "draft_cloud_purchase_info": "",
            "draft_cloud_template_id": "",
            "draft_cloud_tutorial_info": "",
            "draft_cloud_videocut_purchase_info": "",
            "draft_cover": "draft_cover.jpg",
            "draft_deeplink_url": "",
            "draft_enterprise_info": {
                "draft_enterprise_extra": "",
                "draft_enterprise_id": "",
                "draft_enterprise_name": "",
                "enterprise_material": []
            },
            "draft_fold_path": f"/Users/user/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/{self.name}",
            "draft_id": self.draft_id,
            "draft_is_ai_packaging_used": False,
            "draft_is_ai_shorts": False,
            "draft_is_article_video_draft": False,
            "draft_is_from_deeplink": "false",
            "draft_is_invisible": False,
            "draft_materials": draft_materials,
            "draft_materials_copied_info": [],
            "draft_name": self.name,
            "draft_new_version": "",
            "draft_removable_storage_device": "",
            "draft_root_path": "/Users/user/Movies/JianyingPro/User Data/Projects/com.lveditor.draft",
            "draft_segment_extra_info": [],
            "draft_timeline_materials_size_": sum(mat["meta"]["duration"] for mat_list in self.materials.values() for mat in mat_list),
            "draft_type": "",
            "tm_draft_cloud_completed": "",
            "tm_draft_cloud_modified": 0,
            "tm_draft_create": current_time,
            "tm_draft_modified": current_time,
            "tm_draft_removed": 0,
            "tm_duration": self.duration
        }
    
    def generate_draft_info(self) -> Dict[str, Any]:
        """Generate the draft_info.json structure"""
        current_time = int(time.time())
        
        # Extract materials for draft_info
        videos = [mat["draft_info"] for mat in self.materials["videos"]]
        audios = [mat["draft_info"] for mat in self.materials["audios"]]
        
        # Generate additional required materials
        audio_fades = []
        speeds = []
        sound_channel_mappings = []
        vocal_separations = []
        canvases = []
        material_animations = []
        
        # Create supporting materials for each segment
        for track in self.tracks:
            for segment in track["segments"]:
                # Generate IDs for this segment's supporting materials
                speed_id = segment["extra_material_refs"][0] if len(segment["extra_material_refs"]) > 0 else str(uuid.uuid4()).upper()
                canvas_id = segment["extra_material_refs"][1] if len(segment["extra_material_refs"]) > 1 else str(uuid.uuid4()).upper()
                sound_mapping_id = segment["extra_material_refs"][2] if len(segment["extra_material_refs"]) > 2 else str(uuid.uuid4()).upper()
                vocal_sep_id = segment["extra_material_refs"][3] if len(segment["extra_material_refs"]) > 3 else str(uuid.uuid4()).upper()
                
                # Speed control
                speeds.append({
                    "curve_speed": None,
                    "id": speed_id,
                    "mode": 0,
                    "speed": 1.0,
                    "type": "speed"
                })
                
                # Canvas
                canvases.append({
                    "album_image": "",
                    "blur": 0.0,
                    "color": "",
                    "id": canvas_id,
                    "image": "",
                    "image_id": "",
                    "image_name": "",
                    "source_platform": 0,
                    "team_id": "",
                    "type": "canvas_color"
                })
                
                # Sound channel mapping
                sound_channel_mappings.append({
                    "audio_channel_mapping": 0,
                    "id": sound_mapping_id,
                    "is_config_open": False,
                    "type": ""
                })
                
                # Vocal separation
                vocal_separations.append({
                    "choice": 0,
                    "id": vocal_sep_id,
                    "production_path": "",
                    "time_range": None,
                    "type": "vocal_separation"
                })
                
                # Material animation for images
                if len(segment["extra_material_refs"]) > 4:
                    material_animation_id = segment["extra_material_refs"][4]
                    material_animations.append({
                        "animations": [],
                        "id": material_animation_id,
                        "type": "sticker_animation"
                    })
        
        # Audio fade for audio tracks
        for track in self.tracks:
            if track["type"] == "audio" and track["segments"]:
                fade_id = str(uuid.uuid4()).upper()
                audio_fades.append({
                    "fade_in_duration": 0,
                    "fade_out_duration": 233333,
                    "fade_type": 0,
                    "id": fade_id,
                    "type": "audio_fade"
                })
        
        return {
            "canvas_config": {
                "height": self.height,
                "ratio": "original",
                "width": self.width
            },
            "color_space": 0,
            "config": {
                "adjust_max_index": 1,
                "attachment_info": [],
                "combination_max_index": 1,
                "export_range": None,
                "extract_audio_last_index": 1,
                "lyrics_recognition_id": "",
                "lyrics_sync": True,
                "lyrics_taskinfo": [],
                "maintrack_adsorb": True,
                "material_save_mode": 0,
                "original_sound_last_index": 1,
                "record_audio_last_index": 1,
                "sticker_max_index": 1,
                "subtitle_recognition_id": "",
                "subtitle_sync": True,
                "subtitle_taskinfo": [],
                "system_font_list": [],
                "video_mute": False,
                "zoom_info_params": None
            },
            "cover": None,
            "create_time": 0,
            "duration": self.duration,
            "extra_info": None,
            "fps": self.fps,
            "free_render_index_mode_on": False,
            "group_container": None,
            "id": self.project_id,
            "keyframe_graph_list": [],
            "keyframes": {
                "adjusts": [],
                "audios": [],
                "effects": [],
                "filters": [],
                "handwrites": [],
                "stickers": [],
                "texts": [],
                "videos": []
            },
            "last_modified_platform": {
                "app_id": 3704,
                "app_source": "lv",
                "app_version": "5.1.8-beta1",
                "device_id": "generated_device_id",
                "hard_disk_id": "generated_disk_id",
                "mac_address": "generated_mac_address",
                "os": "mac",
                "os_version": "14.3"
            },
            "materials": {
                "audio_balances": [],
                "audio_effects": [],
                "audio_fades": audio_fades,
                "audio_track_indexes": [],
                "audios": audios,
                "beats": [],
                "canvases": canvases,
                "chromas": [],
                "color_curves": [],
                "digital_humans": [],
                "drafts": [],
                "effects": [],
                "flowers": [],
                "green_screens": [],
                "handwrites": [],
                "hsl": [],
                "images": [],
                "log_color_wheels": [],
                "loudnesses": [],
                "manual_deformations": [],
                "masks": [],
                "material_animations": material_animations,
                "material_colors": [],
                "placeholders": [],
                "plugin_effects": [],
                "primary_color_wheels": [],
                "realtime_denoises": [],
                "shapes": [],
                "smart_crops": [],
                "smart_relights": [],
                "sound_channel_mappings": sound_channel_mappings,
                "speeds": speeds,
                "stickers": [],
                "tail_leaders": [],
                "text_templates": [],
                "texts": [],
                "transitions": [],
                "video_effects": [],
                "video_trackings": [],
                "videos": videos,
                "vocal_beautifys": [],
                "vocal_separations": vocal_separations
            },
            "mutable_config": None,
            "name": "",
            "new_version": "97.0.0",
            "platform": {
                "app_id": 3704,
                "app_source": "lv",
                "app_version": "5.1.8-beta1",
                "device_id": "generated_device_id",
                "hard_disk_id": "generated_disk_id",
                "mac_address": "generated_mac_address",
                "os": "mac",
                "os_version": "14.3"
            },
            "relationships": [],
            "render_index_track_mode_on": True,
            "retouch_cover": None,
            "source": "default",
            "static_cover_image_path": "",
            "tracks": self.tracks,
            "update_time": 0,
            "version": 360000
        }
    
    def save_draft(self, output_dir: str):
        """Save the draft to the specified directory"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save draft_meta_info.json
        meta_info = self.generate_draft_meta_info()
        with open(output_path / "draft_meta_info.json", "w", encoding="utf-8") as f:
            json.dump(meta_info, f, ensure_ascii=False, indent=2)
        
        # Save draft_info.json
        draft_info = self.generate_draft_info()
        with open(output_path / "draft_info.json", "w", encoding="utf-8") as f:
            json.dump(draft_info, f, ensure_ascii=False, indent=2)
        
        print(f"Draft saved to {output_path}")
