import os
from typing import Callable, List, Set
import bpy
import bmesh
import random
import numpy as np
import json
import math
import pathlib
import time
import datetime
import csv
import mathutils
from bpy_extras.io_utils import ImportHelper


class DataLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLogger, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        # Scene
        self.scene_index = 0
        self.scene_datetime = datetime.datetime.now()
        self.scene_seed = 0
        self.scene_render_time = 0
        self.start_exec_render_time = 0

        # Camera
        self.camera_height = 0
        self.camera_pos_seed = 0
        self.camera_focal_length = 0
        self.camera_exposure = 0

        # Lighting
        self.light_indoor_lighting = False
        self.light_amount_of_lights = 0
        self.light_dist_seed = 0
        self.light_lamp_temp = 0
        self.sun_intensity = 0
        self.sun_elevation = 0
        self.sun_rotation = 0
        self.air_density = 0
        self.dust_density = 0
        self.ozone_density = 0

        # Room
        self.room_area = 0
        self.room_generator_seed = 0
        self.room_wall_height = 0
        self.room_wall_thickness = 0
        self.room_baseboard_height = 0
        self.room_baseboard_width = 0
        self.room_table_location_seed = 0
        self.room_amount_of_windows = 0
        self.room_window_height = 0
        self.room_window_width = 0
        self.room_window_frame_thickness = 0
        self.room_window_frame_depth = 0
        self.room_window_thickness = 0
        self.room_window_depth = 0
        self.room_glass_thickness = 0
        self.room_window_height_pos = 0
        self.room_window_dist_seed = 0
        self.room_wall_mat = ""
        self.room_wall_col_palette = ""
        self.room_wall_mat_rot = (0, 0, 0)
        self.room_floor_mat = ""
        self.room_floor_col_palette = ""
        self.room_floor_mat_rot = (0, 0, 0)

        # Table Distribution
        self.table_dist_amount_of_knives = 0
        self.table_dist_amount_of_spoons = 0
        self.table_dist_amount_of_forks = 0
        self.table_dist_amount_of_glasses = 0
        self.table_dist_amount_of_plates = 0
        self.table_dist_amount_of_distractors = 0
        self.table_dist_amount_of_napkins = 0
        self.table_dist_tableware_dist_seed = 0
        self.table_dist_tableware_rot_seed = 0
        self.table_dist_chair_loc_seed = 0
        self.table_dist_chair_rot_seed = 0

        # Table
        self.table_round_table = False
        self.table_round_apron = False
        self.table_height = 0
        self.table_width = 0
        self.table_depth = 0
        self.table_top_thickness = 0
        self.table_top_curvature = 0
        self.table_apron_size_reduction = 0
        self.table_apron_thickness = 0
        self.table_leg_width = 0
        self.table_leg_thickness = 0
        self.table_leg_angle = 0
        self.table_top_mat = ""
        self.table_top_col_palette = ""
        self.table_top_mat_rot = (0, 0, 0)
        self.table_bot_mat = ""
        self.table_bot_col_palette = ""
        self.table_bot_mat_rot = (0, 0, 0)

        # Chair
        self.chair_curved_backrest = False
        self.chair_round_seat = False
        self.chair_round_rail = False
        self.chair_height = 0
        self.chair_width = 0
        self.chair_depth = 0
        self.chair_backrest_angle = 0
        self.chair_top_rail_height = 0
        self.chair_top_rail_thickness = 0
        self.chair_backpost_width = 0
        self.chair_backpost_thickness = 0
        self.chair_amount_of_crossrails = 0
        self.chair_crossrail_height = 0
        self.chair_crossrail_thickness = 0
        self.chair_amount_of_slats = 0
        self.chair_slat_width = 0
        self.chair_slat_thickness = 0
        self.chair_seat_height = 0
        self.chair_seat_thickness = 0
        self.chair_seat_curvature = 0
        self.chair_seat_rail_reduction = 0
        self.chair_seat_rail_thickness = 0
        self.chair_leg_width = 0
        self.chair_leg_thickness = 0
        self.chair_leg_angle = 0
        self.chair_seat_mat = ""
        self.chair_seat_col_palette = ""
        self.chair_seat_mat_rot = (0, 0, 0)
        self.chair_rail_mat = ""
        self.chair_rail_col_palette = ""
        self.chair_rail_mat_rot = (0, 0, 0)

        # Fork
        self.fork_length = 0
        self.fork_thickness = 0
        self.fork_amount_of_prongs = 0
        self.fork_prong_length = 0
        self.fork_prong_tip_curvature = 0
        self.fork_eyes_curvature = 0
        self.fork_bowl_length = 0
        self.fork_bowl_width = 0
        self.fork_bowl_curvature = 0
        self.fork_neck_length = 0
        self.fork_neck_height = 0
        self.fork_handle_width = 0
        self.fork_handle_end_height = 0
        self.fork_handle_end_width = 0
        self.fork_handle_end_curvature = 0

        # Glass
        self.glass_lod = 0
        self.glass_height = 0
        self.glass_thickness = 0
        self.glass_base_diameter = 0
        self.glass_base_curvature = 0
        self.glass_base_thickness = 0
        self.glass_mid_curvature_height = 0
        self.glass_mid_curvature_diameter = 0
        self.glass_rim_diameter = 0
        self.glass_rim_curvature = 0
        self.glass_bowl_curvature = 0

        # Knife
        self.knife_length = 0
        self.knife_width = 0
        self.knife_thickness = 0
        self.knife_blade_length = 0
        self.knife_blade_thickness = 0
        self.knife_blade_tip_curvature = 0
        self.knife_blade_tip_intensity = 0
        self.knife_blade_base_curvature = 0
        self.knife_blade_base_intensity = 0
        self.knife_handle_width = 0
        self.knife_handle_end_width = 0
        self.knife_handle_end_curvature = 0

        # Plate
        self.plate_diameter = 0
        self.plate_height = 0
        self.plate_thickness = 0
        self.plate_well_coor = (0, 0)
        self.plate_lip_coor = (0, 0)
        self.plate_rim_coor = (0, 0)
        self.plate_base = False
        self.plate_base_radius = 0
        self.plate_base_height = 0
        self.plate_base_width = 0
        self.plate_dirt_pattern_seed = 0
        self.plate_crumb_geometry_seed = 0
        self.plate_crumb_distribution_seed = 0
        self.plate_crumb_scale_seed = 0

        ## WIP: PLATE ALTERNATIVES ARE MISSING
        ## WIP: RANDOM OBJECTS ON PLATE ARE MISSING

        # Spoon
        self.spoon_length = 0
        self.spoon_thickness = 0
        self.spoon_lod = 0
        self.spoon_bowl_length = 0
        self.spoon_bowl_width = 0
        self.spoon_bowl_depth = 0
        self.spoon_neck_length = 0
        self.spoon_neck_height = 0
        self.spoon_handle_width = 0
        self.spoon_handle_end_height = 0
        self.spoon_handle_end_width = 0
        self.spoon_handle_end_curvature = 0

        # Distractor
        self.distractor_max_lenghts = [0, 0, 0, 0, 0]
        self.distractor_max_heights = [0, 0, 0, 0, 0]
        self.distractor_max_segments = [0, 0, 0, 0, 0]
        self.distractor_random_seeds = [0, 0, 0, 0, 0]
        self.distractor_material_random_seeds = [0, 0, 0, 0, 0]
        self.distractor_material_colors1 = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]
        self.distractor_material_colors2 = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]
        self.distractor_material_colors3 = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]
        self.distractor_material_rotations = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]

        # Napkin
        self.napkin_random_colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]

        self.csv_file_name = bpy.context.scene.datalogger_name

        self.scene_attribute_keys = [
            "index",
            "datetime",
            "scene_seed",
            "render_time",
            "camera_height",
            "camera_position_seed",
            "camera_focal_length",
            "camera_exposure",
            "indoor_lighting",
            "amount_of_lights",
            "light_distribution_seed",
            "lamp_temperature",
            "sun_intensity",
            "sun_elevation",
            "sun_rotation",
            "air_density",
            "dust_density",
            "ozone_density",
            "room_area",
            "room_generator_seed",
            "wall_height",
            "wall_thickness",
            "baseboard_height",
            "baseboard_width",
            "table_location_seed",
            "amount_of_windows",
            "window_height",
            "window_width",
            "window_frame_thickness",
            "window_frame_depth",
            "window_thickness",
            "window_depth",
            "glass_thickness",
            "window_height_position",
            "window_distribution_seed",
            "wall_material",
            "wall_material_color_palette",
            "wall_material_rotation",
            "floor_material",
            "floor_material_color_palette",
            "floor_material_rotation",
            "table_distribution_amount_of_knives",
            "table_distribution_amount_of_spoons",
            "table_distribution_amount_of_forks",
            "table_distribution_amount_of_glasses",
            "table_distribution_amount_of_plates",
            "table_distribution_amount_of_distractors",
            "table_distribution_amount_of_napkins",
            "tableware_distribution_placement_seed",
            "tableware_distribution_rotation_seed",
            "table_distribution_chair_placement_seed",
            "table_distribution_chair_rotation_seed",
            "round_table",
            "table_round_apron",
            "table_height",
            "table_width",
            "table_depth",
            "table_top_thickness",
            "table_top_curvature",
            "table_apron_size_reduction",
            "table_apron_thickness",
            "table_leg_width",
            "table_leg_thickness",
            "table_leg_angle",
            "table_top_material",
            "table_top_color_palette",
            "table_top_material_rotation",
            "table_bottom_material",
            "table_bottom_color_palette",
            "table_bottom_material_rotation",
            "chair_curved_backrest",
            "chair_round_seat",
            "chair_round_rail",
            "chair_height",
            "chair_width",
            "chair_depth",
            "chair_backrest_angle",
            "chair_top_rail_height",
            "chair_top_rail_thickness",
            "chair_backpost_width",
            "chair_backpost_thickness",
            "chair_amount_of_crossrails",
            "chair_crossrail_height",
            "chair_crossrail_thickness",
            "chair_amount_of_slats",
            "chair_slat_width",
            "chair_slat_thickness",
            "chair_seat_height",
            "chair_seat_thickness",
            "chair_seat_curvature",
            "chair_seat_rail_reduction",
            "chair_seat_rail_thickness",
            "chair_leg_width",
            "chair_leg_thickness",
            "chair_leg_angle",
            "chair_seat_material",
            "chair_seat_color_palette",
            "chair_seat_material_rotation",
            "chair_rail_material",
            "chair_rail_color_palette",
            "chair_rail_material_rotation",
            "fork_length",
            "fork_thickness",
            "fork_amount_of_prongs",
            "fork_prong_length",
            "fork_prong_tip_curvature",
            "fork_eyes_curvature",
            "fork_bowl_length",
            "fork_bowl_width",
            "fork_bowl_curvature",
            "fork_neck_length",
            "fork_neck_height",
            "fork_handle_width",
            "fork_handle_end_height",
            "fork_handle_end_width",
            "fork_handle_end_curvature",
            "glass_lod",
            "glass_height",
            "glass_thickness",
            "glass_base_diameter",
            "glass_base_curvature",
            "glass_base_thickness",
            "glass_mid_curvature_height",
            "glass_mid_curvature_diameter",
            "glass_rim_diameter",
            "glass_rim_curvature",
            "glass_bowl_curvature",
            "knife_length",
            "knife_width",
            "knife_thickness",
            "knife_blade_length",
            "knife_blade_thickness",
            "knife_blade_tip_curvature",
            "knife_blade_tip_intensity",
            "knife_blade_base_curvature",
            "knife_blade_base_intensity",
            "knife_handle_width",
            "knife_handle_end_width",
            "knife_handle_end_curvature",
            "plate_diameter",
            "plate_height",
            "plate_thickness",
            "plate_well_coordinate",
            "plate_lip_coordinate",
            "plate_rim_coordinate",
            "plate_base",
            "plate_base_radius",
            "plate_base_height",
            "plate_base_width",
            "plate_dirt_pattern_seed",
            "plate_crumb_geometry_seed",
            "plate_crumb_distribution_seed",
            "plate_crumb_scale_seed",
            "spoon_length",
            "spoon_thickness",
            "spoon_lod",
            "spoon_bowl_length",
            "spoon_bowl_width",
            "spoon_bowl_depth",
            "spoon_neck_length",
            "spoon_neck_height",
            "spoon_handle_width",
            "spoon_handle_end_height",
            "spoon_handle_end_width",
            "spoon_handle_end_curvature",
            "distractor_max_lengths",
            "distractor_max_heights",
            "distractor_max_segments",
            "distractor_random_seeds",
            "distractor_material_random_seeds",
            "distractor_material_rotations",
            "distractor_material_colors1",
            "distractor_material_colors2",
            "distractor_material_colors3",
            "napkin_random_colors",
        ]

    def add_entry_to_csv(self):

        scene_attribute_values = [
            self.scene_index,
            self.scene_datetime,
            self.scene_seed,
            self.scene_render_time,
            self.camera_height,
            self.camera_pos_seed,
            self.camera_focal_length,
            self.camera_exposure,
            self.light_indoor_lighting,
            self.light_amount_of_lights,
            self.light_dist_seed,
            self.light_lamp_temp,
            self.sun_intensity,
            self.sun_elevation,
            self.sun_rotation,
            self.air_density,
            self.dust_density,
            self.ozone_density,
            self.room_area,
            self.room_generator_seed,
            self.room_wall_height,
            self.room_wall_thickness,
            self.room_baseboard_height,
            self.room_baseboard_width,
            self.room_table_location_seed,
            self.room_amount_of_windows,
            self.room_window_height,
            self.room_window_width,
            self.room_window_frame_thickness,
            self.room_window_frame_depth,
            self.room_window_thickness,
            self.room_window_depth,
            self.room_glass_thickness,
            self.room_window_height_pos,
            self.room_window_dist_seed,
            self.room_wall_mat,
            self.room_wall_col_palette,
            self.room_wall_mat_rot,
            self.room_floor_mat,
            self.room_floor_col_palette,
            self.room_floor_mat_rot,
            self.table_dist_amount_of_knives,
            self.table_dist_amount_of_spoons,
            self.table_dist_amount_of_forks,
            self.table_dist_amount_of_glasses,
            self.table_dist_amount_of_plates,
            self.table_dist_amount_of_distractors,
            self.table_dist_amount_of_napkins,
            self.table_dist_tableware_dist_seed,
            self.table_dist_tableware_rot_seed,
            self.table_dist_chair_loc_seed,
            self.table_dist_chair_rot_seed,
            self.table_round_table,
            self.table_round_apron,
            self.table_height,
            self.table_width,
            self.table_depth,
            self.table_top_thickness,
            self.table_top_curvature,
            self.table_apron_size_reduction,
            self.table_apron_thickness,
            self.table_leg_width,
            self.table_leg_thickness,
            self.table_leg_angle,
            self.table_top_mat,
            self.table_top_col_palette,
            self.table_top_mat_rot,
            self.table_bot_mat,
            self.table_bot_col_palette,
            self.table_bot_mat_rot,
            self.chair_curved_backrest,
            self.chair_round_seat,
            self.chair_round_rail,
            self.chair_height,
            self.chair_width,
            self.chair_depth,
            self.chair_backrest_angle,
            self.chair_top_rail_height,
            self.chair_top_rail_thickness,
            self.chair_backpost_width,
            self.chair_backpost_thickness,
            self.chair_amount_of_crossrails,
            self.chair_crossrail_height,
            self.chair_crossrail_thickness,
            self.chair_amount_of_slats,
            self.chair_slat_width,
            self.chair_slat_thickness,
            self.chair_seat_height,
            self.chair_seat_thickness,
            self.chair_seat_curvature,
            self.chair_seat_rail_reduction,
            self.chair_seat_rail_thickness,
            self.chair_leg_width,
            self.chair_leg_thickness,
            self.chair_leg_angle,
            self.chair_seat_mat,
            self.chair_seat_col_palette,
            self.chair_seat_mat_rot,
            self.chair_rail_mat,
            self.chair_rail_col_palette,
            self.chair_rail_mat_rot,
            self.fork_length,
            self.fork_thickness,
            self.fork_amount_of_prongs,
            self.fork_prong_length,
            self.fork_prong_tip_curvature,
            self.fork_eyes_curvature,
            self.fork_bowl_length,
            self.fork_bowl_width,
            self.fork_bowl_curvature,
            self.fork_neck_length,
            self.fork_neck_height,
            self.fork_handle_width,
            self.fork_handle_end_height,
            self.fork_handle_end_width,
            self.fork_handle_end_curvature,
            self.glass_lod,
            self.glass_height,
            self.glass_thickness,
            self.glass_base_diameter,
            self.glass_base_curvature,
            self.glass_base_thickness,
            self.glass_mid_curvature_height,
            self.glass_mid_curvature_diameter,
            self.glass_rim_diameter,
            self.glass_rim_curvature,
            self.glass_bowl_curvature,
            self.knife_length,
            self.knife_width,
            self.knife_thickness,
            self.knife_blade_length,
            self.knife_blade_thickness,
            self.knife_blade_tip_curvature,
            self.knife_blade_tip_intensity,
            self.knife_blade_base_curvature,
            self.knife_blade_base_intensity,
            self.knife_handle_width,
            self.knife_handle_end_width,
            self.knife_handle_end_curvature,
            self.plate_diameter,
            self.plate_height,
            self.plate_thickness,
            self.plate_well_coor,
            self.plate_lip_coor,
            self.plate_rim_coor,
            self.plate_base,
            self.plate_base_radius,
            self.plate_base_height,
            self.plate_base_width,
            self.plate_dirt_pattern_seed,
            self.plate_crumb_geometry_seed,
            self.plate_crumb_distribution_seed,
            self.plate_crumb_scale_seed,
            self.spoon_length,
            self.spoon_thickness,
            self.spoon_lod,
            self.spoon_bowl_length,
            self.spoon_bowl_width,
            self.spoon_bowl_depth,
            self.spoon_neck_length,
            self.spoon_neck_height,
            self.spoon_handle_width,
            self.spoon_handle_end_height,
            self.spoon_handle_end_width,
            self.spoon_handle_end_curvature,
            self.distractor_max_lenghts,
            self.distractor_max_heights,
            self.distractor_max_segments,
            self.distractor_random_seeds,
            self.distractor_material_random_seeds,
            self.distractor_material_rotations,
            self.distractor_material_colors1,
            self.distractor_material_colors2,
            self.distractor_material_colors3,
            self.napkin_random_colors,
        ]

        datapoint_entry_dict = {
            self.scene_attribute_keys[i]: scene_attribute_values[i]
            for i in range(len(self.scene_attribute_keys))
        }

        with open(
            f"{bpy.context.scene.render_filepath}/{self.csv_file_name}.csv",
            "a",
            newline="",
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.scene_attribute_keys)
            writer.writerow(datapoint_entry_dict)

    def create_csv(self):
        with open(
            f"{bpy.context.scene.render_filepath}/{self.csv_file_name}.csv",
            "w",
            newline="",
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.scene_attribute_keys)
            writer.writeheader()

        self.add_entry_to_csv()

    def create_or_append_csv(self):
        if pathlib.Path(
            f"{bpy.context.scene.render_filepath}/{self.csv_file_name}.csv"
        ).exists():
            self.add_entry_to_csv()
        else:
            self.create_csv()

    def datalog_camera(self, camera_randomizer):
        self.camera_height = camera_randomizer.camera_height
        self.camera_pos_seed = camera_randomizer.camera_position_random_seed
        self.camera_focal_length = camera_randomizer.focal_length
        self.camera_exposure = camera_randomizer.exposure

    def datalog_lighting(self, procedural_room, lighting_randomizer):
        self.light_indoor_lighting = procedural_room.indoor_lighting
        self.light_amount_of_lights = procedural_room.amount_of_lights
        self.light_dist_seed = procedural_room.light_distribution_random_seed
        self.light_lamp_temp = lighting_randomizer.lamp_temperature
        self.sun_intensity = lighting_randomizer.sun_intensity
        self.sun_elevation = lighting_randomizer.sun_elevation
        self.sun_rotation = lighting_randomizer.sun_rotation
        self.air_density = lighting_randomizer.air_density
        self.dust_density = lighting_randomizer.dust_density
        self.ozone_density = lighting_randomizer.ozone_density

    def datalog_room(self, procedural_room):
        self.room_area = procedural_room.room_area
        self.room_generator_seed = procedural_room.construct_floor_random_seed
        self.room_wall_height = procedural_room.wall_height
        self.room_wall_thickness = procedural_room.wall_thickness
        self.room_baseboard_height = procedural_room.baseboard_height
        self.room_baseboard_width = procedural_room.baseboard_width
        self.room_table_location_seed = procedural_room.table_location_random_seed
        self.room_amount_of_windows = procedural_room.amount_of_windows
        self.room_window_height = procedural_room.window_height
        self.room_window_width = procedural_room.window_width
        self.room_window_frame_thickness = procedural_room.window_frame_thickness
        self.room_window_frame_depth = procedural_room.window_frame_depth
        self.room_window_thickness = procedural_room.window_thickness
        self.room_window_depth = procedural_room.window_depth
        self.room_glass_thickness = procedural_room.glass_thickness
        self.room_window_height_pos = procedural_room.window_height_pos
        self.room_window_dist_seed = procedural_room.window_distribution_random_seed
        self.room_wall_mat = procedural_room.room_wall_mat
        self.room_wall_col_palette = procedural_room.room_wall_col_palette
        self.room_wall_mat_rot = procedural_room.room_wall_mat_rot
        self.room_floor_mat = procedural_room.room_floor_mat
        self.room_floor_col_palette = procedural_room.room_floor_col_palette
        self.room_floor_mat_rot = procedural_room.room_floor_mat_rot

    def datalog_table_distribution(self, dining_room_distributor):
        self.table_dist_amount_of_knives = dining_room_distributor.amount_of_knives
        self.table_dist_amount_of_spoons = dining_room_distributor.amount_of_spoons
        self.table_dist_amount_of_forks = dining_room_distributor.amount_of_forks
        self.table_dist_amount_of_glasses = dining_room_distributor.amount_of_glasses
        self.table_dist_amount_of_plates = dining_room_distributor.amount_of_plates
        self.table_dist_amount_of_distractors = (
            dining_room_distributor.amount_of_distractors
        )
        self.table_dist_amount_of_napkins = dining_room_distributor.amount_of_napkins
        self.table_dist_tableware_dist_seed = (
            dining_room_distributor.distribution_random_seed
        )
        self.table_dist_tableware_rot_seed = (
            dining_room_distributor.tableware_rotation_random_seed
        )
        self.table_dist_chair_loc_seed = (
            dining_room_distributor.chair_location_random_seed
        )
        self.table_dist_chair_rot_seed = (
            dining_room_distributor.chair_rotation_random_seed
        )

    def datalog_chair(self, procedural_chair):
        self.chair_curved_backrest = procedural_chair.curved_backrest
        self.chair_round_seat = procedural_chair.round_seat
        self.chair_round_rail = procedural_chair.round_rail
        self.chair_height = procedural_chair.height
        self.chair_width = procedural_chair.width
        self.chair_depth = procedural_chair.depth
        self.chair_backrest_angle = procedural_chair.backrest_angle
        self.chair_top_rail_height = procedural_chair.top_rail_height
        self.chair_top_rail_thickness = procedural_chair.top_rail_thickness
        self.chair_backpost_width = procedural_chair.backpost_width
        self.chair_backpost_thickness = procedural_chair.backpost_thickness
        self.chair_amount_of_crossrails = procedural_chair.amount_of_crossrails
        self.chair_crossrail_height = procedural_chair.crossrail_height
        self.chair_crossrail_thickness = procedural_chair.crossrail_thickness
        self.chair_amount_of_slats = procedural_chair.amount_of_slats
        self.chair_slat_width = procedural_chair.slat_width
        self.chair_slat_thickness = procedural_chair.slat_thickness
        self.chair_seat_height = procedural_chair.seat_height
        self.chair_seat_thickness = procedural_chair.seat_thickness
        self.chair_seat_curvature = procedural_chair.seat_curvature
        self.chair_seat_rail_reduction = procedural_chair.seat_rail_reduction
        self.chair_seat_rail_thickness = procedural_chair.seat_rail_thickness
        self.chair_leg_width = procedural_chair.leg_width
        self.chair_leg_thickness = procedural_chair.leg_thickness
        self.chair_leg_angle = procedural_chair.leg_angle
        self.chair_seat_mat = procedural_chair.chair_seat_mat
        self.chair_seat_col_palette = procedural_chair.chair_seat_col_palette
        self.chair_seat_mat_rot = procedural_chair.chair_seat_mat_rot
        self.chair_rail_mat = procedural_chair.chair_rail_mat
        self.chair_rail_col_palette = procedural_chair.chair_rail_col_palette
        self.chair_rail_mat_rot = procedural_chair.chair_rail_mat_rot

    def datalog_table(self, procedural_table):
        self.table_round_table = procedural_table.round_table
        self.table_round_apron = procedural_table.round_apron
        self.table_height = procedural_table.height
        self.table_width = procedural_table.width
        self.table_depth = procedural_table.depth
        self.table_top_thickness = procedural_table.top_thickness
        self.table_top_curvature = procedural_table.top_curvature
        self.table_apron_size_reduction = procedural_table.apron_size_reduction
        self.table_apron_thickness = procedural_table.apron_thickness
        self.table_leg_width = procedural_table.leg_width
        self.table_leg_thickness = procedural_table.leg_thickness
        self.table_leg_angle = procedural_table.leg_angle
        self.table_top_mat = procedural_table.table_top_mat
        self.table_top_col_palette = procedural_table.table_top_col_palette
        self.table_top_mat_rot = procedural_table.table_top_mat_rot
        self.table_bot_mat = procedural_table.table_bot_mat
        self.table_bot_col_palette = procedural_table.table_bot_col_palette
        self.table_bot_mat_rot = procedural_table.table_bot_mat_rot

    def datalog_fork(self, procedural_fork):
        self.fork_length = procedural_fork.length
        self.fork_thickness = procedural_fork.thickness
        self.fork_amount_of_prongs = procedural_fork.amount_of_prongs
        self.fork_prong_length = procedural_fork.prong_length
        self.fork_prong_tip_curvature = procedural_fork.prong_tip_curvature
        self.fork_eyes_curvature = procedural_fork.eyes_curvature
        self.fork_bowl_length = procedural_fork.bowl_length
        self.fork_bowl_width = procedural_fork.bowl_width
        self.fork_bowl_curvature = procedural_fork.bowl_curvature
        self.fork_neck_length = procedural_fork.neck_length
        self.fork_neck_height = procedural_fork.neck_height
        self.fork_handle_width = procedural_fork.handle_width
        self.fork_handle_end_height = procedural_fork.handle_end_height
        self.fork_handle_end_width = procedural_fork.handle_end_width
        self.fork_handle_end_curvature = procedural_fork.handle_end_curvature

    def datalog_glass(self, procedural_glass):
        self.glass_lod = procedural_glass.lod
        self.glass_height = procedural_glass.height
        self.glass_thickness = procedural_glass.thickness
        self.glass_base_diameter = procedural_glass.base_diameter
        self.glass_base_curvature = procedural_glass.base_curvature
        self.glass_base_thickness = procedural_glass.base_thickness
        self.glass_mid_curvature_height = procedural_glass.mid_curvature_height
        self.glass_mid_curvature_diameter = procedural_glass.mid_curvature_diameter
        self.glass_rim_diameter = procedural_glass.rim_diameter
        self.glass_rim_curvature = procedural_glass.rim_curvature
        self.glass_bowl_curvature = procedural_glass.bowl_curvature

    def datalog_knife(self, procedural_knife):
        self.knife_length = procedural_knife.length
        self.knife_width = procedural_knife.width
        self.knife_thickness = procedural_knife.thickness
        self.knife_blade_length = procedural_knife.blade_length
        self.knife_blade_thickness = procedural_knife.blade_thickness
        self.knife_blade_tip_curvature = procedural_knife.blade_tip_curvature
        self.knife_blade_tip_intensity = procedural_knife.blade_tip_intensity
        self.knife_blade_base_curvature = procedural_knife.blade_base_curvature
        self.knife_blade_base_intensity = procedural_knife.blade_base_intensity
        self.knife_handle_width = procedural_knife.handle_width
        self.knife_handle_end_width = procedural_knife.handle_end_width
        self.knife_handle_end_curvature = procedural_knife.handle_end_curvature

    def datalog_plate(self, procedural_plate):
        self.plate_diameter = procedural_plate.plate_diameter
        self.plate_height = procedural_plate.plate_height
        self.plate_thickness = procedural_plate.plate_thickness
        self.plate_well_coor = procedural_plate.well_coor
        self.plate_lip_coor = procedural_plate.lip_coor
        self.plate_rim_coor = procedural_plate.rim_coor
        self.plate_base = procedural_plate.base
        self.plate_base_radius = procedural_plate.base_radius
        self.plate_base_height = procedural_plate.base_height
        self.plate_base_width = procedural_plate.base_width
        self.plate_dirt_pattern_seed = procedural_plate.dirt_pattern_seed
        self.plate_crumb_geometry_seed = procedural_plate.crumb_geometry_seed
        self.plate_crumb_distribution_seed = procedural_plate.crumb_distribution_seed
        self.plate_crumb_scale_seed = procedural_plate.crumb_scale_seed

    def datalog_spoon(self, procedural_spoon):
        self.spoon_length = procedural_spoon.length
        self.spoon_thickness = procedural_spoon.thickness
        self.spoon_lod = procedural_spoon.lod
        self.spoon_bowl_length = procedural_spoon.bowl_length
        self.spoon_bowl_width = procedural_spoon.bowl_width
        self.spoon_bowl_depth = procedural_spoon.bowl_depth
        self.spoon_neck_length = procedural_spoon.neck_length
        self.spoon_neck_height = procedural_spoon.neck_height
        self.spoon_handle_width = procedural_spoon.handle_width
        self.spoon_handle_end_height = procedural_spoon.handle_end_height
        self.spoon_handle_end_width = procedural_spoon.handle_end_width
        self.spoon_handle_end_curvature = procedural_spoon.handle_end_curvature

    def datalog_distractor(self, procedural_distractor, i):
        self.distractor_max_lenghts[i] = procedural_distractor.max_length
        self.distractor_max_heights[i] = procedural_distractor.max_height
        self.distractor_max_segments[i] = procedural_distractor.max_segments
        self.distractor_random_seeds[i] = procedural_distractor.random_seed
        self.distractor_material_random_seeds[i] = (
            procedural_distractor.distractor_mat_random_seed
        )
        self.distractor_material_colors1[i] = (
            procedural_distractor.distractor_mat_color1
        )
        self.distractor_material_colors2[i] = (
            procedural_distractor.distractor_mat_color2
        )
        self.distractor_material_colors3[i] = (
            procedural_distractor.distractor_mat_color3
        )
        self.distractor_material_rotations[i] = (
            procedural_distractor.distractor_mat_rotation
        )

    def datalog_napkin_mat(self, random_col, i):
        self.napkin_random_colors[i] = random_col


class ColorPaletteRandomizer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ColorPaletteRandomizer, cls).__new__(cls)

        return cls._instance

    def __init__(self):

        file_path = ""

        if (
            bpy.context.space_data != None
            and bpy.context.space_data.type == "TEXT_EDITOR"
        ):
            file_path = bpy.context.space_data.text.filepath
        else:
            file_path = __file__

        folder_path = pathlib.Path(file_path).resolve().parent

        self.material_list_url = str(
            folder_path / "material_color_palettes/material_list.json"
        )
        self.material_folder_url = str(folder_path / "material_color_palettes/")

    def hex_color_str_to_rgba(self, hex_color: str):
        """
        Converting from a color in the form of a hex triplet string ((en.wikipedia.org/wiki/Web_colors#Hex_triplet))
        to Linear RGB with an Alpha of 1.0

        Args:
        - hex_color (str): The hex color string in the format "#RRGGBB" or "RRGGBB"

        Returns:
        - rgba_color (tuple): The Linear RGB color with an Alpha of 1.0
        """

        # remove '#' symbol if present
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]

        assert len(hex_color) == 6, "RRGGBB is the supported hex color format"

        # extracting the red color component - RRxxxx
        red = int(hex_color[:2], 16)
        # divding by 255 to get a number between 0.0 and 1.0
        srgb_red = red / 255
        linear_red = self.convert_srgb_to_linear_rgb(srgb_red)

        # extracting the green color component - xxGxx
        green = int(hex_color[2:4], 16)
        # dividing by 255 to get a number between 0.0 and 1.0
        srgb_green = green / 255
        linear_green = self.convert_srgb_to_linear_rgb(srgb_green)

        # extracting the blue color component - xxxxBB
        blue = int(hex_color[4:6], 16)
        # diving by 255 to get a number between 0.0 and 1.0
        srgb_blue = blue / 255
        linear_blue = self.convert_srgb_to_linear_rgb(srgb_blue)

        alpha = 1.0
        return tuple([linear_red, linear_green, linear_blue, alpha])

    def convert_srgb_to_linear_rgb(self, srgb_color_component):
        """
        Converting from sRGB to Linear RGB
        based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ

        Args:
        - srgb_color_component (float): The sRGB color component value

        Return:
        - linear_color_coponent (float): The linear RGB color component value
        """

        if srgb_color_component <= 0.04045:
            linear_color_component = srgb_color_component / 12.92
        else:
            linear_color_component = math.pow(
                (srgb_color_component + 0.055) / 1.055, 2.4
            )

        return linear_color_component

    def get_random_rgba(
        self,
    ):
        random_rgba = (
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
            1,
        )
        return random_rgba

    def get_random_rotation(
        self,
    ):
        return random.uniform(0, 2 * np.pi)

    def get_json_color_palette(self, colorpalette_file_name):
        return f"{self.material_folder_url}{colorpalette_file_name}.json"

    def get_dining_room_object(self, obj_name, path_to_material_list):

        with open(path_to_material_list, "r") as object:
            objects = json.loads(object.read())

        for object in objects:
            if object["name"] == obj_name:
                return object

        return None

    def pick_random_material_and_color_palette(
        self, object, attribute_name, path_to_material_color_palettes_folder
    ):

        material = random.choice(object[attribute_name])
        if material["color_palette"] == "rgb":
            return (material, "rgb")
        else:
            path_to_material_color_palettes_folder = pathlib.Path(
                f"{path_to_material_color_palettes_folder}/{material['color_palette']}.json"
            )
            with open(path_to_material_color_palettes_folder, "r") as color_palette:
                color_palettes = json.loads(color_palette.read())

            color_palette = random.choice(color_palettes)
            return (material, color_palette)


class LightingRandomizer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LightingRandomizer, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.lamp_temperature = 0
        self.light_bulb_watt_strength = 2.1

        self.sun_size = 0
        self.sun_intensity = 0
        self.sun_elevation = 0
        self.sun_rotation = 0
        self.air_density = 0
        self.dust_density = 0
        self.ozone_density = 0

    def randomize_indoor_lighting(self, context):

        self.lamp_temperature = np.random.choice(np.arange(2700, 5300, 50))

        light_obj = bpy.data.objects["room_light"].data
        light_obj.energy = self.light_bulb_watt_strength
        light_obj.shadow_soft_size = 0
        light_obj.color = [1.0, 1.0, 1.0]
        light_obj.node_tree.nodes["Group"].inputs[
            "Temperature"
        ].default_value = self.lamp_temperature

    def randomize_environment_lighting(self, context):

        self.sun_intensity = np.random.choice(np.arange(0, 1000, 10))
        self.sun_elevation = np.random.choice(np.arange(0, np.pi / 2, 0.001))
        self.sun_rotation = np.random.choice(np.arange(0, np.pi, 0.001))
        self.air_density = np.random.choice(np.arange(1, 2, 0.001))
        self.dust_density = np.random.choice(np.arange(0, 10, 0.001))
        self.ozone_density = np.random.choice(np.arange(1, 2, 0.001))

        environment_nodes = bpy.data.worlds["World"].node_tree.nodes
        sky_texture_node = environment_nodes["Sky Texture"]

        sky_texture_node.sun_disc = True
        sky_texture_node.sun_size = math.radians(2)
        sky_texture_node.sun_intensity = self.sun_intensity
        sky_texture_node.sun_elevation = self.sun_elevation
        sky_texture_node.sun_rotation = self.sun_rotation
        sky_texture_node.altitude = 0
        sky_texture_node.air_density = self.air_density
        sky_texture_node.dust_density = self.dust_density
        sky_texture_node.ozone_density = self.ozone_density


class CameraRandomizer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CameraRandomizer, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.camera_rotation = 0
        self.focus_point_pos = 0
        self.camera_height = 0
        self.camera_position_random_seed = 0
        self.focal_length = 0
        self.exposure = 0

    def randomize_camera_position(self, context):
        image_camera_obj = bpy.data.objects["camera_image"]
        segmentation_camera_obj = bpy.data.objects["camera_segmentation"]
        focus_point_obj = bpy.data.objects["camera_focus_point"]

        if "Room Generator" in context.object.modifiers:
            rg_mod = context.object.modifiers["Room Generator"]
            rg_node_group = rg_mod.node_group

            self.camera_height = np.random.choice(np.arange(1.3, 1.6, 0.01))
            self.camera_position_random_seed = np.random.choice(np.arange(0, 5000, 1))
            self.focal_length = np.random.choice(np.arange(35, 85, 1))
            self.exposure = bpy.data.scenes[
                SceneRenderer().main_scene_name
            ].view_settings.exposure

            camera_height_id = rg_node_group.interface.items_tree[
                "Camera Height"
            ].identifier
            camera_position_random_seed_id = rg_node_group.interface.items_tree[
                "Camera Position Random Seed"
            ].identifier

            rg_mod[camera_height_id] = self.camera_height
            rg_mod[camera_position_random_seed_id] = int(
                self.camera_position_random_seed
            )

            rg_node_group.interface_update(context)

            camera_position = [
                v.vector
                for v in context.object.evaluated_get(context.evaluated_depsgraph_get())
                .data.attributes["camera_position"]
                .data
            ][0]

            focus_point_position = [
                v.vector
                for v in context.object.evaluated_get(context.evaluated_depsgraph_get())
                .data.attributes["focus_point_position"]
                .data
            ][0]

            image_camera_obj.location = (
                camera_position[0],
                camera_position[1],
                self.camera_height,
            )
            segmentation_camera_obj.location = (
                camera_position[0],
                camera_position[1],
                self.camera_height,
            )
            focus_point_obj.location = focus_point_position

            image_camera_obj.data.lens = self.focal_length
            segmentation_camera_obj.data.lens = self.focal_length


class ProceduralPlate(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralPlate, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.plate_diameter = 0
        self.plate_height = 0
        self.plate_thickness = 0
        self.well_x = 0
        self.well_coor = (self.well_x, 0)
        self.lip_x = 0
        self.lip_y = 0
        self.lip_coor = (self.lip_x, self.lip_y)
        self.rim_coor = (self.plate_diameter, 0)
        self.base = False
        self.base_radius = 0
        self.base_height = 0
        self.base_width = 0

        self.dirt_pattern_seed = 0
        self.crumb_geometry_seed = 0
        self.crumb_distribution_seed = 0
        self.crumb_scale_seed = 0

        self.tableware_spawn_point_seed = 0
        self.tableware_rotation_seed = 0
        self.tableware_object_seed = 0

    def create_plate(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.object.name = "plate"

        pcg_mod = bpy.context.object.modifiers.new("Plate Curve Generator", "NODES")
        if "plate_curve_generator" in bpy.data.node_groups.keys():
            pcg_node_tree = bpy.data.node_groups["plate_curve_generator"].copy()
        else:
            self.report({"ERROR"}, "WIP: Plate Curve Generator Node Tree not found.")
        pcg_mod.node_group = pcg_node_tree

        screw_mod = bpy.context.object.modifiers.new("Screw", "SCREW")
        screw_mod.use_merge_vertices = True

        subdiv_mod = bpy.context.object.modifiers.new("Subdivision", "SUBSURF")
        subdiv_mod.levels = 2

    def reset_curvemapping(self, context, geo_group=None):

        points = geo_group.nodes["Float Curve"].mapping.curves[0].points

        # Required to keep at least two points
        while len(points) > 2:
            points.remove(points[1])

        # Reset curve location
        points[0].location = (0, 0)
        points[1].location = (1, 1)

        geo_group.nodes["Float Curve"].mapping.update()
        geo_group.interface_update(context)

    def randomize_plate(self, context):
        if "Plate Curve Generator" in context.object.modifiers:
            pcg_mod = context.object.modifiers["Plate Curve Generator"]
            pcg_node_group = pcg_mod.node_group

            self.reset_curvemapping(context, pcg_node_group)
            points = pcg_node_group.nodes["Float Curve"].mapping.curves[0].points

            # Used Online DB with Ikea Tableware Measurements
            self.plate_diameter = np.random.choice(np.arange(0.11, 0.36, 0.001))
            self.plate_height = np.random.choice(np.arange(0.015, 0.12, 0.001))
            self.plate_thickness = np.random.choice(np.arange(0.002, 0.01, 0.001))

            plate_radius = self.plate_diameter / 2

            self.well_x = np.random.choice(np.arange(0, plate_radius, 0.001))
            self.well_coor = (self.well_x, 0)

            self.lip_x = np.random.choice(np.arange(self.well_x, plate_radius, 0.001))
            self.lip_y = np.random.choice(np.arange(0, self.plate_height, 0.001))

            self.lip_coor = (self.lip_x, self.lip_y)

            self.rim_coor = (
                plate_radius,
                np.random.choice(np.arange(self.lip_y, self.plate_height, 0.001)),
            )

            well_point = points.new(self.well_coor[0], self.well_coor[1])
            well_point.handle_type = "AUTO" if random.random() < 0.5 else "VECTOR"

            lip_point = points.new(self.lip_coor[0], self.lip_coor[1])
            lip_point.handle_type = "AUTO" if random.random() < 0.5 else "VECTOR"

            points[3].location = (self.rim_coor[0], self.rim_coor[1])

            # To avoid curves with a too high gradient
            points.new(self.rim_coor[0] + 0.0101, self.rim_coor[1])

            base_id = pcg_node_group.interface.items_tree["Base"].identifier
            diameter_id = pcg_node_group.interface.items_tree["Diameter"].identifier
            thickness_id = pcg_node_group.interface.items_tree["Thickness"].identifier
            base_radius_id = pcg_node_group.interface.items_tree[
                "Base Radius"
            ].identifier
            base_height_id = pcg_node_group.interface.items_tree[
                "Base Height"
            ].identifier
            base_width_id = pcg_node_group.interface.items_tree["Base Width"].identifier

            # arbitrarily choosen (measure on own tableware)
            if self.well_x >= 0.02:
                self.base = random.random() < 0.5
                pcg_mod[base_id] = self.base
                # Used Online DB with Ikea Tableware Measurements
                self.base_radius = self.well_x
                pcg_mod[base_radius_id] = self.base_radius
            else:
                self.base = True
                pcg_mod[base_id] = self.base

                # arbitrarily choosen (measure on own tableware)
                self.base_radius = plate_radius / 3
                pcg_mod[base_radius_id] = self.base_radius

            pcg_mod[diameter_id] = self.plate_diameter

            # arbitrarily choosen (measure on own tableware)
            pcg_mod[thickness_id] = self.plate_thickness

            # arbitrarily choosen (measure on own tableware)
            self.base_height = np.random.choice(np.arange(0.002, 0.01, 0.001))
            pcg_mod[base_height_id] = self.base_height

            self.base_width = np.random.choice(np.arange(0.002, 0.01, 0.001))
            pcg_mod[base_width_id] = self.base_width

            pcg_node_group.nodes["Float Curve"].mapping.update()
            pcg_node_group.interface_update(context)

            # print()
            # print(
            #     f"Plate Radius: {self.plate_diameter}\nPlate Height: {self.plate_height}\nWell Radius: {self.well_radius}\nLip Coor: {self.lip_coor}\nRim Height: {self.rim_coor}"
            # )
            # print()
        else:
            print("Object does not have the 'Plate Curve Generator' Modifier")
            self.report(
                {"ERROR"}, "Object does not have the 'Plate Curve Generator' Modifier"
            )

    def randomize_soil_material(self, context):
        ceramic_dirt_mat = bpy.data.materials["Procedural Ceramic Plate Dirt"]
        ceramic_crumble_mat = bpy.data.materials["Procedural Crumb Pastries"]

        random_num = np.random.choice(np.arange(-10000, 10000, 1))
        random_smear_col = ColorPaletteRandomizer().get_random_rgba()
        random_spot_col = ColorPaletteRandomizer().get_random_rgba()
        random_crumble_col = ColorPaletteRandomizer().get_random_rgba()

        ceramic_dirt_mat.node_tree.nodes["Group"].inputs[
            "Random"
        ].default_value = random_num
        ceramic_dirt_mat.node_tree.nodes["Group"].inputs[
            "Color 1"
        ].default_value = random_smear_col
        ceramic_dirt_mat.node_tree.nodes["Group"].inputs[
            "Color 2"
        ].default_value = random_spot_col

        ceramic_crumble_mat.node_tree.nodes["Group"].inputs[
            "Color 1"
        ].default_value = random_crumble_col

        ceramic_dirt_mat.node_tree.interface_update(context)
        ceramic_crumble_mat.node_tree.interface_update(context)

    def randomize_crumbs(self, context):
        if "Plate Crumbs" in context.object.modifiers:
            pc_mod = context.object.modifiers["Plate Crumbs"]
            pc_node_group = pc_mod.node_group

            self.dirt_pattern_seed = np.random.choice(np.arange(-10000, 10000, 1))
            self.crumb_geometry_seed = np.random.choice(np.arange(-10000, 10000, 1))
            self.crumb_distribution_seed = np.random.choice(np.arange(-10000, 10000, 1))
            self.crumb_scale_seed = np.random.choice(np.arange(-10000, 10000, 1))

            dirt_pattern_seed_id = pc_node_group.interface.items_tree[
                "Dirt Pattern Random Seed"
            ].identifier
            crumb_geometry_seed_id = pc_node_group.interface.items_tree[
                "Crumb Geometry Random Seed"
            ].identifier
            crumb_distribution_seed_id = pc_node_group.interface.items_tree[
                "Crumb Distribution Random Seed"
            ].identifier
            crumb_scale_seed_id = pc_node_group.interface.items_tree[
                "Crumb Scale Random Seed"
            ].identifier

            pc_mod[dirt_pattern_seed_id] = int(self.dirt_pattern_seed)
            pc_mod[crumb_geometry_seed_id] = int(self.crumb_geometry_seed)
            pc_mod[crumb_distribution_seed_id] = int(self.crumb_distribution_seed)
            pc_mod[crumb_scale_seed_id] = int(self.crumb_scale_seed)

            pc_node_group.interface_update(context)

    def randomize_tableware_on_plate(self, context):
        if "Tableware on Plate" in context.object.modifiers:
            top_mod = context.object.modifiers["Tableware on Plate"]
            top_node_group = top_mod.node_group

            self.tableware_spawn_point_seed = np.random.choice(
                np.arange(-10000, 10000, 1)
            )
            self.tableware_rotation_seed = np.random.choice(np.arange(-10000, 10000, 1))
            self.tableware_object_seed = np.random.choice(np.arange(-10000, 10000, 1))

            tableware_spawn_point_seed_id = top_node_group.interface.items_tree[
                "Spawn Point Seed"
            ].identifier
            tableware_rotation_seed_id = top_node_group.interface.items_tree[
                "Tableware Rotation Seed"
            ].identifier
            tableware_object_seed_id = top_node_group.interface.items_tree[
                "Object Seed"
            ].identifier

            top_mod[tableware_spawn_point_seed_id] = int(
                self.tableware_spawn_point_seed
            )
            top_mod[tableware_rotation_seed_id] = int(self.tableware_rotation_seed)
            top_mod[tableware_object_seed_id] = int(self.tableware_object_seed)

            top_node_group.interface_update(context)


class ProceduralSpoon(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralSpoon, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.length = 0
        self.thickness = 0

        self.lod = 3

        self.bowl_length = 0
        self.bowl_width = 0
        self.bowl_depth = 0

        self.neck_length = 0
        self.neck_height = 0

        self.handle_width = 0
        self.handle_end_height = 0
        self.handle_end_width = 0
        self.handle_end_curvature = 0

    def create_spoon(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.object.name = "spoon"

        sg_mod = bpy.context.object.modifiers.new("Spoon Generator", "NODES")
        if "spoon_generator" in bpy.data.node_groups.keys():
            sg_node_tree = bpy.data.node_groups["spoon_generator"]
        else:
            self.report({"ERROR"}, "WIP: Spoon Generator Node Tree not found.")
        sg_mod.node_group = sg_node_tree

        solidify_mod = bpy.context.object.modifiers.new("Solidify", "SOLIDIFY")
        solidify_mod.thickness = 0.002
        solidify_mod.offset = 1
        solidify_mod.use_even_offset = True
        solidify_mod.use_rim = True

        bevel_mod = bpy.context.object.modifiers.new("Bevel", "BEVEL")
        bevel_mod.width = 0.001
        bevel_mod.segments = 2

    def randomize_spoon(self, context):
        if "Spoon Generator" in context.object.modifiers:
            sg_mod = context.object.modifiers["Spoon Generator"]
            sg_node_group = sg_mod.node_group

            self.length = np.random.choice(np.arange(0.187, 0.218, 0.001))
            self.thickness = np.random.choice(np.arange(0.001, 0.002, 0.0001))

            self.lod = 3

            self.bowl_length = np.random.choice(np.arange(0.05, 0.064, 0.001))
            self.bowl_width = np.random.choice(np.arange(0.038, 0.044, 0.001))
            self.bowl_depth = np.random.choice(np.arange(0.005, 0.0125, 0.001))

            self.neck_length = np.random.choice(np.arange(0.005, 0.03, 0.001))
            self.neck_height = np.random.choice(np.arange(0.01, 0.025, 0.001))

            self.handle_width = np.random.choice(
                np.arange(0.005, self.bowl_width / 3, 0.001)
            )
            self.handle_end_height = np.random.choice(np.arange(0.01, 0.05, 0.001))
            self.handle_end_width = np.random.choice(
                np.arange(0.005, self.handle_width + 0.01, 0.001)
            )
            self.handle_end_curvature = np.random.choice(
                np.arange(0, self.length - self.bowl_length - self.neck_length, 0.001)
            )

            ##################################################################################

            length_id = sg_node_group.interface.items_tree["Length"].identifier

            lod_id = sg_node_group.interface.items_tree["Level of Detail"].identifier

            bowl_length_id = sg_node_group.interface.items_tree[
                "Bowl Length"
            ].identifier
            bowl_width_id = sg_node_group.interface.items_tree["Bowl Width"].identifier
            bowl_depth_id = sg_node_group.interface.items_tree["Bowl Depth"].identifier

            neck_length_id = sg_node_group.interface.items_tree[
                "Neck Length"
            ].identifier
            neck_height_id = sg_node_group.interface.items_tree[
                "Neck Height"
            ].identifier

            handle_width_id = sg_node_group.interface.items_tree[
                "Handle Width"
            ].identifier
            handle_end_height_id = sg_node_group.interface.items_tree[
                "Handle End Height"
            ].identifier
            handle_end_width_id = sg_node_group.interface.items_tree[
                "Handle End Width"
            ].identifier
            handle_end_curvature_id = sg_node_group.interface.items_tree[
                "Handle End Curvature"
            ].identifier

            ##################################################################################

            sg_mod[length_id] = self.length

            sg_mod[lod_id] = self.lod

            sg_mod[bowl_length_id] = self.bowl_length
            sg_mod[bowl_width_id] = self.bowl_width
            sg_mod[bowl_depth_id] = self.bowl_depth

            sg_mod[neck_length_id] = self.neck_length
            sg_mod[neck_height_id] = self.neck_height

            sg_mod[handle_width_id] = self.handle_width
            sg_mod[handle_end_height_id] = self.handle_end_height
            sg_mod[handle_end_width_id] = self.handle_end_width
            sg_mod[handle_end_curvature_id] = self.handle_end_curvature

            if "Solidify" in context.object.modifiers:
                solidify_mod = context.object.modifiers["Solidify"]
                rounded_thickness = float(np.around(self.thickness, decimals=5))
                solidify_mod.thickness = rounded_thickness
            else:
                print("Object does not have the 'Solidify' Modifier")
                self.report({"ERROR"}, "Object does not have the 'Solidify' Modifier")

            sg_node_group.interface_update(context)
        else:
            print("Object does not have the 'Spoon Generator' Modifier")
            self.report(
                {"ERROR"}, "Object does not have the 'Spoon Generator' Modifier"
            )


class ProceduralFork(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralFork, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.length = 0
        self.thickness = 0

        self.amount_of_prongs = 4
        self.prong_length = 0
        self.prong_tip_curvature = 0

        self.eyes_curvature = 0

        self.bowl_length = 0
        self.bowl_width = 0
        self.bowl_curvature = 0

        self.neck_length = 0
        self.neck_height = 0

        self.handle_width = 0
        self.handle_end_height = 0
        self.handle_end_width = 0
        self.handle_end_curvature = 0

    def create_fork(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.object.name = "fork"

        fg_mod = bpy.context.object.modifiers.new("Fork Generator", "NODES")
        if "fork_generator" in bpy.data.node_groups.keys():
            fg_node_tree = bpy.data.node_groups["fork_generator"]
        else:
            self.report({"ERROR"}, "WIP: Fork Generator Node Tree not found.")
        fg_mod.node_group = fg_node_tree

        solidify_mod = bpy.context.object.modifiers.new("Solidify", "SOLIDIFY")
        solidify_mod.thickness = 0.002
        solidify_mod.offset = 1
        solidify_mod.use_even_offset = True
        solidify_mod.use_rim = True

        bevel_mod = bpy.context.object.modifiers.new("Bevel", "BEVEL")
        bevel_mod.width = 0.001
        bevel_mod.segments = 2

    def randomize_fork(self, context):
        if "Fork Generator" in context.object.modifiers:
            fg_mod = context.object.modifiers["Fork Generator"]
            fg_node_group = fg_mod.node_group

            self.length = np.random.choice(np.arange(0.183, 0.217, 0.001))
            self.thickness = np.random.choice(np.arange(0.001, 0.002, 0.0001))

            self.amount_of_prongs = 4
            self.prong_length = np.random.choice(np.arange(0.032, 0.051, 0.001))
            self.prong_tip_curvature = np.random.choice(
                np.arange(0, self.prong_length, 0.001)
            )

            if self.prong_tip_curvature <= 0:
                self.eyes_curvature = 0.0
            else:
                self.eyes_curvature = np.random.choice(
                    np.arange(0, self.prong_tip_curvature, 0.001)
                )

            self.bowl_length = np.random.choice(np.arange(0.008, 0.02, 0.001))
            self.bowl_width = np.random.choice(np.arange(0.02, 0.031, 0.001))
            self.bowl_curvature = np.random.choice(np.arange(2, 5, 1))

            self.neck_length = np.random.choice(np.arange(0.005, 0.03, 0.001))
            self.neck_height = np.random.choice(np.arange(0.01, 0.025, 0.001))

            self.handle_width = np.random.choice(
                np.arange(0.005, self.bowl_width / 2, 0.001)
            )

            self.handle_end_height = np.random.choice(np.arange(0.01, 0.05, 0.001))
            self.handle_end_width = np.random.choice(
                np.arange(0.005, self.handle_width + 0.01, 0.001)
            )
            self.handle_end_curvature = np.random.choice(
                np.arange(
                    0,
                    self.length
                    - self.prong_length
                    - self.bowl_length
                    - self.neck_length,
                    0.001,
                )
            )

            ##################################################################################

            length_id = fg_node_group.interface.items_tree["Length"].identifier

            amount_of_prongs_id = fg_node_group.interface.items_tree[
                "Amount of Prongs"
            ].identifier

            prong_length_id = fg_node_group.interface.items_tree[
                "Prong Length"
            ].identifier
            prong_tip_curvature_id = fg_node_group.interface.items_tree[
                "Prong Tip Curvature"
            ].identifier

            eyes_curvature_id = fg_node_group.interface.items_tree[
                "Eyes Curvature"
            ].identifier

            bowl_length_id = fg_node_group.interface.items_tree[
                "Bowl Length"
            ].identifier
            bowl_width_id = fg_node_group.interface.items_tree["Bowl Width"].identifier
            bowl_curvature_id = fg_node_group.interface.items_tree[
                "Bowl Curvature"
            ].identifier

            neck_length_id = fg_node_group.interface.items_tree[
                "Neck Length"
            ].identifier
            neck_height_id = fg_node_group.interface.items_tree[
                "Neck Height"
            ].identifier

            handle_width_id = fg_node_group.interface.items_tree[
                "Handle Width"
            ].identifier
            handle_end_height_id = fg_node_group.interface.items_tree[
                "Handle End Height"
            ].identifier
            handle_end_width_id = fg_node_group.interface.items_tree[
                "Handle End Width"
            ].identifier
            handle_end_curvature_id = fg_node_group.interface.items_tree[
                "Handle End Curvature"
            ].identifier

            ##################################################################################

            fg_mod[length_id] = self.length

            fg_mod[amount_of_prongs_id] = self.amount_of_prongs
            fg_mod[prong_length_id] = self.prong_length
            fg_mod[prong_tip_curvature_id] = self.prong_tip_curvature

            fg_mod[eyes_curvature_id] = self.eyes_curvature

            fg_mod[bowl_length_id] = self.bowl_length
            fg_mod[bowl_width_id] = self.bowl_width
            fg_mod[bowl_curvature_id] = int(self.bowl_curvature)

            fg_mod[neck_length_id] = self.neck_length
            fg_mod[neck_height_id] = self.neck_height

            fg_mod[handle_width_id] = self.handle_width
            fg_mod[handle_end_height_id] = self.handle_end_height
            fg_mod[handle_end_width_id] = self.handle_end_width
            fg_mod[handle_end_curvature_id] = self.handle_end_curvature

            if "Solidify" in context.object.modifiers:
                solidify_mod = context.object.modifiers["Solidify"]
                rounded_thickness = float(np.around(self.thickness, decimals=5))
                solidify_mod.thickness = rounded_thickness
            else:
                print("Object does not have the 'Solidify' Modifier")
                self.report({"ERROR"}, "Object does not have the 'Solidify' Modifier")

            fg_node_group.interface_update(context)

        else:
            self.report({"ERROR"}, "Object does not have the 'Fork Generator' Modifier")
            print("Object does not have the 'Fork Generator' Modifier")


class ProceduralKnife(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralKnife, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.length = 0
        self.width = 0
        self.thickness = 0

        self.blade_length = 0
        self.blade_thickness = 0

        self.blade_tip_curvature = 0
        self.blade_tip_intensity = 0

        self.blade_base_curvature = 0
        self.blade_base_intensity = 0

        self.handle_width = 0
        self.handle_end_width = 0
        self.handle_end_curvature = 0

    def create_knife(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.object.name = "knife"

        kg_mod = bpy.context.object.modifiers.new("Knife Generator", "NODES")
        if "knife_generator" in bpy.data.node_groups.keys():
            kg_node_tree = bpy.data.node_groups["knife_generator"]
        else:
            self.report({"ERROR"}, "WIP: Knife Generator Node Tree not found.")
        kg_mod.node_group = kg_node_tree

    def randomize_knife(self, context):
        if "Knife Generator" in context.object.modifiers:
            kg_mod = context.object.modifiers["Knife Generator"]
            kg_node_group = kg_mod.node_group

            self.length = np.random.choice(np.arange(0.203, 0.23, 0.001))
            self.width = np.random.choice(np.arange(0.02, 0.03, 0.001))
            self.thickness = np.random.choice(np.arange(0.005, 0.012, 0.001))

            self.blade_length = np.random.choice(np.arange(0.08, 0.12, 0.001))
            self.blade_thickness = np.random.choice(
                np.arange(0.001, self.thickness, 0.001)
            )

            self.blade_tip_curvature = np.random.choice(
                np.arange(0.01, self.blade_length - 0.01, 0.001)
            )
            self.blade_tip_intensity = np.random.choice(
                np.arange(0.002, self.length - self.blade_length - 0.005, 0.001)
            )

            self.blade_base_curvature = np.random.choice(
                np.arange(
                    0.001, self.blade_length - self.blade_tip_curvature - 0.005, 0.001
                )
            )
            self.blade_base_intensity = np.random.choice(
                np.arange(0, self.width - self.handle_width, 0.001)
            )

            self.handle_width = np.random.choice(np.arange(0.008, 0.015, 0.001))
            self.handle_end_width = np.random.choice(
                np.arange(0.005, self.handle_width + 0.01, 0.001)
            )
            self.handle_end_curvature = np.random.choice(
                np.arange(0, self.length - self.blade_length, 0.001)
            )

            ##################################################################################

            length_id = kg_node_group.interface.items_tree["Length"].identifier
            width_id = kg_node_group.interface.items_tree["Width"].identifier
            thickness_id = kg_node_group.interface.items_tree["Thickness"].identifier

            blade_length_id = kg_node_group.interface.items_tree[
                "Blade Length"
            ].identifier
            blade_thickness_id = kg_node_group.interface.items_tree[
                "Blade Thickness"
            ].identifier

            blade_tip_curvature_id = kg_node_group.interface.items_tree[
                "Blade Tip Curvature"
            ].identifier
            blade_tip_intensity_id = kg_node_group.interface.items_tree[
                "Blade Tip Intensity"
            ].identifier

            blade_base_curvature_id = kg_node_group.interface.items_tree[
                "Blade Base Curvature"
            ].identifier
            blade_base_intensity_id = kg_node_group.interface.items_tree[
                "Blade Base Intensity"
            ].identifier

            handle_width_id = kg_node_group.interface.items_tree[
                "Handle Width"
            ].identifier
            handle_end_width_id = kg_node_group.interface.items_tree[
                "Handle End Width"
            ].identifier
            handle_end_curvature_id = kg_node_group.interface.items_tree[
                "Handle End Curvature"
            ].identifier

            ##################################################################################

            kg_mod[length_id] = self.length
            kg_mod[width_id] = self.width
            kg_mod[thickness_id] = self.thickness

            kg_mod[blade_length_id] = self.blade_length
            kg_mod[blade_thickness_id] = self.blade_thickness

            kg_mod[blade_tip_curvature_id] = self.blade_tip_curvature
            kg_mod[blade_tip_intensity_id] = self.blade_tip_intensity

            kg_mod[blade_base_curvature_id] = self.blade_base_curvature
            kg_mod[blade_base_intensity_id] = self.blade_base_intensity

            kg_mod[handle_width_id] = self.handle_width
            kg_mod[handle_end_width_id] = self.handle_end_width
            kg_mod[handle_end_curvature_id] = self.handle_end_curvature

            kg_node_group.interface_update(context)
        else:
            print("Object does not have the 'Knife Generator' Modifier")
            self.report(
                {"ERROR"}, "Object does not have the 'Knife Generator' Modifier"
            )


class ProceduralGlass(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralGlass, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.lod = 3

        self.height = 0
        self.thickness = 0

        self.base_diameter = 0
        self.base_curvature = 0
        self.base_thickness = 0

        self.mid_curvature_height = 0
        self.mid_curvature_diameter = 0

        self.rim_diameter = 0
        self.rim_curvature = 0

        self.bowl_curvature = 0

    def create_glass(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.object.name = "glass"

        gg_mod = bpy.context.object.modifiers.new("Glass Generator", "NODES")
        if "glass_generator" in bpy.data.node_groups.keys():
            gg_node_tree = bpy.data.node_groups["glass_generator"]
        else:
            print("WIP: Glass Generator Node Tree not found.")
            self.report({"ERROR"}, "WIP: Glass Generator Node Tree not found.")
        gg_mod.node_group = gg_node_tree

    def randomize_glass(self, context):
        if "Glass Generator" in context.object.modifiers:
            gg_mod = context.object.modifiers["Glass Generator"]
            gg_node_group = gg_mod.node_group

            self.lod = 3

            self.height = np.random.choice(np.arange(0.06, 0.1775, 0.001))
            self.thickness = np.random.choice(np.arange(0.002, 0.01, 0.001))

            self.mid_curvature_height = np.random.choice(
                np.arange(0.001, self.height, 0.001)
            )

            self.base_diameter = np.random.choice(np.arange(0.0725, 0.1, 0.001))

            if self.mid_curvature_height == 0.001:
                self.base_curvature = 0.001
            else:
                self.base_curvature = np.random.choice(
                    np.arange(0.001, self.mid_curvature_height, 0.001)
                )
            self.base_thickness = np.random.choice(
                np.arange(0.001, self.height / 5, 0.001)
            )

            self.mid_curvature_diameter = np.random.choice(
                np.arange(0.0725, 0.1, 0.001)
            )

            self.rim_diameter = np.random.choice(np.arange(0.0725, 0.1, 0.001))
            self.rim_curvature = np.random.choice(np.arange(0, self.thickness, 0.001))

            self.bowl_curvature = self.base_curvature

            ##################################################################################

            lod_id = gg_node_group.interface.items_tree["Level of Detail"].identifier

            height_id = gg_node_group.interface.items_tree["Height"].identifier
            thickness_id = gg_node_group.interface.items_tree["Thickness"].identifier

            base_diameter_id = gg_node_group.interface.items_tree[
                "Base Diameter"
            ].identifier
            base_curvature_id = gg_node_group.interface.items_tree[
                "Base Curvature"
            ].identifier
            base_thickness_id = gg_node_group.interface.items_tree[
                "Base Thickness"
            ].identifier

            mid_curvature_height_id = gg_node_group.interface.items_tree[
                "Mid Curvature Height"
            ].identifier
            mid_curvature_diameter_id = gg_node_group.interface.items_tree[
                "Mid Curvature Diameter"
            ].identifier

            rim_diameter_id = gg_node_group.interface.items_tree[
                "Rim Diameter"
            ].identifier
            rim_curvature_id = gg_node_group.interface.items_tree[
                "Rim Curvature"
            ].identifier

            bowl_curvature_id = gg_node_group.interface.items_tree[
                "Bowl Curvature"
            ].identifier

            ##################################################################################

            gg_mod[lod_id] = self.lod

            gg_mod[height_id] = self.height
            gg_mod[thickness_id] = self.thickness

            gg_mod[base_diameter_id] = self.base_diameter
            gg_mod[base_curvature_id] = self.base_curvature
            gg_mod[base_thickness_id] = self.base_thickness

            gg_mod[mid_curvature_height_id] = self.mid_curvature_height
            gg_mod[mid_curvature_diameter_id] = self.mid_curvature_diameter

            gg_mod[rim_diameter_id] = self.rim_diameter
            gg_mod[rim_curvature_id] = self.rim_curvature

            gg_mod[bowl_curvature_id] = self.bowl_curvature

            gg_node_group.interface_update(context)

        else:
            print("Object does not have the 'Glass Generator' Modifier")
            self.report(
                {"ERROR"}, "Object does not have the 'Glass Generator' Modifier"
            )


class ProceduralPlacemat(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralPlacemat, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.round_tablecloth = False
        self.symmetry = False

        self.height = 0
        self.width = 0
        self.depth = 0

        self.square_placemat_curvature = 0

    def create_placemat(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.object.name = "placemat"

        pmg_mod = bpy.context.object.modifiers.new("Placemat Generator", "NODES")
        if "placemat_generator" in bpy.data.node_groups.keys():
            pmg_node_tree = bpy.data.node_groups["placemat_generator"]
        else:
            self.report({"ERROR"}, "WIP: Placemat Generator Node Tree not found.")
        pmg_mod.node_group = pmg_node_tree

    def randomize_placemat(self, context):
        if "Placemat Generator" in context.object.modifiers:
            pmg_mod = context.object.modifiers["Placemat Generator"]
            pmg_node_group = pmg_mod.node_group

            self.round_tablecloth = random.random() < 0.5
            self.symmetry = random.random() < 0.5
            self.height = np.random.choice(np.arange(0.0015, 0.004, 0.0001))

            if self.symmetry:
                self.width = np.random.choice(np.arange(0.292, 0.457, 0.001))
                self.depth = self.width
            else:
                self.width = np.random.choice(np.arange(0.362, 0.457, 0.001))
                self.depth = np.random.choice(np.arange(0.292, 0.368, 0.001))

            self.square_placemat_curvature = np.random.choice(
                np.arange(0.001, np.minimum(self.width / 2, self.depth / 2), 0.001)
            )

            ##################################################################################

            round_tablecloth_id = pmg_node_group.interface.items_tree[
                "Round Tablecloth"
            ].identifier

            height_id = pmg_node_group.interface.items_tree["Height"].identifier
            width_id = pmg_node_group.interface.items_tree["Width"].identifier
            depth_id = pmg_node_group.interface.items_tree["Depth"].identifier

            square_placemat_curvature = pmg_node_group.interface.items_tree[
                "Square Placemat Curvature"
            ].identifier

            ##################################################################################

            pmg_mod[round_tablecloth_id] = self.round_tablecloth

            pmg_mod[height_id] = self.height
            pmg_mod[width_id] = self.width
            pmg_mod[depth_id] = self.depth

            pmg_mod[square_placemat_curvature] = self.depth

            pmg_node_group.interface_update(context)

        else:
            print("Object does not have the 'Placemat Generator' Modifier")
            self.report(
                {"ERROR"}, "Object does not have the 'Placemat Generator' Modifier"
            )


class ProceduralChair(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralChair, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.curved_backrest = False
        self.round_seat = False
        self.round_rail = False

        self.height = 0
        self.width = 0
        self.depth = 0

        self.backrest_angle = 0

        self.top_rail_height = 0
        self.top_rail_thickness = 0

        self.backpost_width = 0
        self.backpost_thickness = 0

        self.amount_of_crossrails = 0
        self.crossrail_height = 0
        self.crossrail_thickness = 0

        self.amount_of_slats = 0
        self.slat_width = 0
        self.slat_thickness = 0

        self.seat_height = 0
        self.seat_thickness = 0
        self.seat_curvature = 0

        self.seat_rail_reduction = 0
        self.seat_rail_thickness = 0

        self.leg_width = 0
        self.leg_thickness = 0
        self.leg_angle = 0

        self.chair_seat_mat = ""
        self.chair_seat_col_palette = ""
        self.chair_seat_mat_rot = 0
        self.chair_rail_mat = ""
        self.chair_rail_col_palette = ""
        self.chair_rail_mat_rot = 0

    def create_chair(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.object.name = "chair"

        cg_mod = bpy.context.object.modifiers.new("Chair Generator", "NODES")
        if "chair_generator" in bpy.data.node_groups.keys():
            cg_node_tree = bpy.data.node_groups["chair_generator"]
        else:
            self.report({"ERROR"}, "WIP: Chair Generator Node Tree not found.")
        cg_mod.node_group = cg_node_tree

        bevel_mod = bpy.context.object.modifiers.new("Bevel", "BEVEL")
        bevel_mod.width = 0.002
        bevel_mod.segments = 4

    def randomize_chair(self, context):
        if "Chair Generator" in context.object.modifiers:
            cg_mod = context.object.modifiers["Chair Generator"]
            cg_node_group = cg_mod.node_group

            self.curved_backrest = random.random() < 0.5
            self.round_seat = random.random() < 0.5
            self.round_rail = random.random() < 0.5

            self.height = np.random.choice(np.arange(0.73, 0.949, 0.001))
            self.width = np.random.choice(np.arange(0.42, 0.559, 0.001))
            self.depth = np.random.choice(np.arange(0.46, 0.69, 0.001))

            self.backpost_width = np.random.choice(np.arange(0.03, 0.15, 0.001))
            self.backpost_thickness = np.random.choice(np.arange(0.03, 0.1, 0.001))

            self.backrest_angle = np.random.choice(np.arange(0, 0.1, 0.001))
            self.top_rail_height = np.random.choice(np.arange(0, 0.1, 0.01))

            self.seat_height = np.random.choice(np.arange(0.419, 0.483, 0.001))
            self.seat_thickness = np.random.choice(np.arange(0.01, 0.05, 0.001))
            self.seat_curvature = np.random.choice(
                np.arange(0.001, np.minimum(self.width / 2, self.depth / 2), 0.001)
            )

            if self.top_rail_height <= 0:

                self.top_rail_thickness = 0.0

                self.amount_of_crossrails = np.random.choice(np.arange(2, 5, 1))

                self.crossrail_height = np.random.choice(
                    np.arange(
                        0.005,
                        (
                            (self.height - self.seat_height - self.top_rail_height)
                            / self.amount_of_crossrails
                        )
                        - 0.01,
                        0.001,
                    )
                )
                self.crossrail_thickness = self.backpost_thickness

                self.amount_of_slats = 0.0
                self.slat_width = 0.0
                self.slat_thickness = 0.0

            else:
                self.top_rail_thickness = np.random.choice(
                    np.arange(0.01, self.backpost_thickness, 0.01)
                )

                self.amount_of_crossrails = np.random.choice(np.arange(0, 5, 1))
                if self.amount_of_crossrails == 0:
                    self.crossrail_height = 0
                    self.crossrail_thickness = 0
                else:
                    self.crossrail_height = np.random.choice(
                        np.arange(
                            0.005,
                            (
                                (self.height - self.seat_height - self.top_rail_height)
                                / self.amount_of_crossrails
                            )
                            - 0.01,
                            0.001,
                        )
                    )
                    self.crossrail_thickness = np.random.choice(
                        np.arange(0.005, self.top_rail_thickness, 0.001)
                    )

            self.seat_rail_thickness = np.random.choice(np.arange(0, 0.1, 0.01))

            ##################################################################################

            curved_backrest_id = cg_node_group.interface.items_tree[
                "Curved Backrest"
            ].identifier
            round_seat_id = cg_node_group.interface.items_tree["Round Seat"].identifier
            round_rail_id = cg_node_group.interface.items_tree["Round Rail"].identifier

            height_id = cg_node_group.interface.items_tree["Height"].identifier
            width_id = cg_node_group.interface.items_tree["Width"].identifier
            depth_id = cg_node_group.interface.items_tree["Depth"].identifier

            backrest_angle_id = cg_node_group.interface.items_tree[
                "Backrest Angle"
            ].identifier

            top_rail_height_id = cg_node_group.interface.items_tree[
                "Top Rail Height"
            ].identifier
            top_rail_thickness_id = cg_node_group.interface.items_tree[
                "Top Rail Thickness"
            ].identifier

            backpost_width_id = cg_node_group.interface.items_tree[
                "Backpost Width"
            ].identifier
            backpost_thickness_id = cg_node_group.interface.items_tree[
                "Backpost Thickness"
            ].identifier

            amount_of_crossrails_id = cg_node_group.interface.items_tree[
                "Amount of Crossrails"
            ].identifier
            crossrail_height_id = cg_node_group.interface.items_tree[
                "Crossrail Height"
            ].identifier
            crossrail_thickness_id = cg_node_group.interface.items_tree[
                "Crossrail Thickness"
            ].identifier

            amount_of_slats_id = cg_node_group.interface.items_tree[
                "Amount of Slats"
            ].identifier
            slat_width_id = cg_node_group.interface.items_tree["Slat Width"].identifier
            slat_thickness_id = cg_node_group.interface.items_tree[
                "Slat Thickness"
            ].identifier

            seat_height_id = cg_node_group.interface.items_tree[
                "Seat Height"
            ].identifier
            seat_thickness_id = cg_node_group.interface.items_tree[
                "Seat Thickness"
            ].identifier
            seat_curvature_id = cg_node_group.interface.items_tree[
                "Seat Curvature"
            ].identifier

            seat_rail_reduction_id = cg_node_group.interface.items_tree[
                "Seat Rail Reduction"
            ].identifier
            seat_rail_thickness_id = cg_node_group.interface.items_tree[
                "Seat Rail Thickness"
            ].identifier

            leg_width_id = cg_node_group.interface.items_tree["Leg Width"].identifier
            leg_thickness_id = cg_node_group.interface.items_tree[
                "Leg Thickness"
            ].identifier
            leg_angle_id = cg_node_group.interface.items_tree["Leg Angle"].identifier

            ##################################################################################

            cg_mod[curved_backrest_id] = self.curved_backrest
            cg_mod[round_seat_id] = self.round_seat
            cg_mod[round_rail_id] = self.round_rail

            cg_mod[height_id] = self.height
            cg_mod[width_id] = self.width
            cg_mod[depth_id] = self.depth

            cg_mod[backrest_angle_id] = self.backrest_angle

            cg_mod[top_rail_height_id] = self.top_rail_height
            cg_mod[top_rail_thickness_id] = self.top_rail_thickness

            cg_mod[backpost_width_id] = self.backpost_width
            cg_mod[backpost_thickness_id] = self.backpost_thickness

            cg_mod[amount_of_crossrails_id] = int(self.amount_of_crossrails)
            cg_mod[crossrail_height_id] = float(self.crossrail_height)
            cg_mod[crossrail_thickness_id] = float(self.crossrail_thickness)

            cg_mod[seat_height_id] = self.seat_height
            cg_mod[seat_thickness_id] = self.seat_thickness
            cg_mod[seat_curvature_id] = self.seat_curvature

            cg_mod[seat_rail_thickness_id] = self.seat_rail_thickness

            cg_node_group.interface_update(context)

            ## Must be at the end, can only be calculated after every other attribute is registered
            ## ORDER IS VERY IMPORTANT HERE

            seat_area_max_width = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["seat_area_max_width"]
                    .data
                ]
            )

            seat_area_max_depth = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["seat_area_max_depth"]
                    .data
                ]
            )

            self.leg_width = np.random.choice(
                np.arange(0.03, seat_area_max_width / 2, 0.001)
            )
            self.leg_thickness = np.random.choice(
                np.arange(0.03, seat_area_max_depth / 2, 0.001)
            )

            self.seat_rail_reduction = np.random.choice(
                np.arange(
                    0,
                    np.minimum(
                        seat_area_max_width - (2 * self.leg_width),
                        seat_area_max_depth - (2 * self.leg_thickness),
                    ),
                    0.001,
                )
            )

            if self.seat_rail_reduction <= 0:
                self.leg_angle = 0
            else:
                self.leg_angle = np.random.choice(
                    np.arange(0, self.seat_rail_reduction / 2, 0.001)
                )

            if self.top_rail_height > 0:
                self.amount_of_slats = np.random.choice(np.arange(0, 5, 1))
                cg_mod[amount_of_slats_id] = int(self.amount_of_slats)
                cg_node_group.interface_update(context)
                if self.amount_of_slats == 0:
                    self.slat_thickness = 0
                    self.slat_width = 0
                else:

                    max_slat_width = (
                        context.object.evaluated_get(context.evaluated_depsgraph_get())
                        .data.attributes["max_slat_width"]
                        .data[0]
                        .value
                    )

                    if max_slat_width <= 0:
                        self.slat_width = 0
                        self.slat_thickness = 0
                    else:
                        self.slat_width = np.random.choice(
                            np.arange(
                                0 if max_slat_width < 0.0005 else 0.0005,
                                max_slat_width,
                                0.0001,
                            )
                        )

                        self.slat_thickness = np.random.choice(
                            np.arange(0.005, self.top_rail_thickness, 0.001)
                        )

                        while self.crossrail_thickness == self.slat_thickness:
                            self.slat_thickness = np.random.choice(
                                np.arange(0.005, self.top_rail_thickness, 0.001)
                            )

            cg_mod[seat_rail_reduction_id] = self.seat_rail_reduction

            cg_mod[leg_thickness_id] = self.leg_thickness
            cg_mod[leg_width_id] = self.leg_width
            cg_mod[leg_angle_id] = float(self.leg_angle)

            cg_mod[slat_width_id] = float(self.slat_width)
            cg_mod[slat_thickness_id] = float(self.slat_thickness)

            cg_node_group.interface_update(context)

    def randomize_material(self, context):

        chair_obj = ColorPaletteRandomizer().get_dining_room_object(
            obj_name="chair",
            path_to_material_list=ColorPaletteRandomizer().material_list_url,
        )
        chair_seat_color_palette = (
            ColorPaletteRandomizer().pick_random_material_and_color_palette(
                chair_obj, "materials_top", ColorPaletteRandomizer().material_folder_url
            )
        )
        self.chair_seat_mat = (
            f"Procedural {chair_seat_color_palette[0]['material']} Chair Seat"
        )
        self.chair_seat_col_palette = chair_seat_color_palette[1]

        chair_rail_color_palette = (
            ColorPaletteRandomizer().pick_random_material_and_color_palette(
                chair_obj,
                "materials_bottom",
                ColorPaletteRandomizer().material_folder_url,
            )
        )
        self.chair_rail_mat = (
            f"Procedural {chair_rail_color_palette[0]['material']} Chair Rail"
        )
        self.chair_rail_col_palette = chair_rail_color_palette[1]

        if "Chair Generator" in context.object.modifiers:
            cg_mod = context.object.modifiers["Chair Generator"]
            cg_node_group = cg_mod.node_group

            seat_mat = bpy.data.materials[self.chair_seat_mat]

            if "rgb" in self.chair_seat_col_palette:
                self.chair_seat_col_palette = ColorPaletteRandomizer().get_random_rgba()
                seat_mat.node_tree.nodes["Group"].inputs[
                    f"Color {1}"
                ].default_value = self.chair_seat_col_palette
            else:
                for i, hex_color in enumerate(self.chair_seat_col_palette, 1):
                    seat_mat.node_tree.nodes["Group"].inputs[
                        f"Color {i}"
                    ].default_value = ColorPaletteRandomizer().hex_color_str_to_rgba(
                        hex_color
                    )

            if "Rotation" in seat_mat.node_tree.nodes["Group"].inputs.keys():
                # Rotate on Z-Axis
                self.chair_seat_mat_rot = ColorPaletteRandomizer().get_random_rotation()
                seat_mat.node_tree.nodes["Group"].inputs["Rotation"].default_value[
                    2
                ] = self.chair_seat_mat_rot
            else:
                self.chair_seat_mat_rot = 0

            seat_mat_id = cg_node_group.interface.items_tree["Seat Material"].identifier
            cg_mod[seat_mat_id] = bpy.data.materials[self.chair_seat_mat]

            seat_mat.node_tree.interface_update(context)

            rail_mat = bpy.data.materials[self.chair_rail_mat]

            if "rgb" in self.chair_rail_col_palette:
                self.chair_rail_col_palette = ColorPaletteRandomizer().get_random_rgba()
                rail_mat.node_tree.nodes["Group"].inputs[
                    f"Color {1}"
                ].default_value = self.chair_rail_col_palette
            else:
                for i, hex_color in enumerate(self.chair_rail_col_palette, 1):
                    rail_mat.node_tree.nodes["Group"].inputs[
                        f"Color {i}"
                    ].default_value = ColorPaletteRandomizer().hex_color_str_to_rgba(
                        hex_color
                    )

            if "Rotation" in rail_mat.node_tree.nodes["Group"].inputs.keys():
                # Rotate on Z-Axis
                self.chair_rail_mat_rot = ColorPaletteRandomizer().get_random_rotation()
                rail_mat.node_tree.nodes["Group"].inputs["Rotation"].default_value[
                    2
                ] = self.chair_rail_mat_rot
            else:
                self.chair_rail_mat_rot = 0

            rail_mat_id = cg_node_group.interface.items_tree["Rail Material"].identifier
            cg_mod[rail_mat_id] = bpy.data.materials[self.chair_rail_mat]

            rail_mat.node_tree.interface_update(context)

            cg_node_group.interface_update(context)


class ProceduralTable(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralTable, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.round_table = False
        self.round_apron = False

        self.height = 0
        self.width = 0
        self.depth = 0

        self.top_thickness = 0
        self.top_curvature = 0

        self.apron_size_reduction = 0
        self.apron_thickness = 0

        self.leg_width = 0
        self.leg_thickness = 0
        self.leg_angle = 0

        self.table_top_mat = ""
        self.table_top_col_palette = ""
        self.table_top_mat_rot = 0
        self.table_bot_mat = ""
        self.table_bot_col_palette = ""
        self.table_bot_mat_rot = 0

    def create_table(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.object.name = "table"

        tg_mod = bpy.context.object.modifiers.new("Table Generator", "NODES")
        if "table_generator" in bpy.data.node_groups.keys():
            tg_node_tree = bpy.data.node_groups["table_generator"]
        else:
            self.report({"ERROR"}, "WIP: Table Generator Node Tree not found.")
        tg_mod.node_group = tg_node_tree

        bevel_mod = bpy.context.object.modifiers.new("Bevel", "BEVEL")
        bevel_mod.width = 0.002
        bevel_mod.segments = 4

    def randomize_table(self, context):
        if "Table Generator" in context.object.modifiers:
            tg_mod = context.object.modifiers["Table Generator"]
            tg_node_group = tg_mod.node_group

            self.round_table = random.random() < 0.5
            self.round_apron = random.random() < 0.5

            self.height = np.random.choice(np.arange(0.71, 0.76, 0.001))
            self.width = np.random.choice(np.arange(1.12, 1.524, 0.001))
            self.depth = self.width

            self.top_thickness = np.random.choice(np.arange(0.01905, 0.0508, 0.001))
            self.top_curvature = np.random.choice(
                np.arange(0.001, np.minimum(self.width / 2, self.depth / 2), 0.001)
            )

            self.apron_thickness = np.random.choice(np.arange(0, 0.1, 0.01))

            ##################################################################################

            round_table_id = tg_node_group.interface.items_tree[
                "Round Table"
            ].identifier
            round_apron_id = tg_node_group.interface.items_tree[
                "Round Apron"
            ].identifier

            height_id = tg_node_group.interface.items_tree["Height"].identifier
            width_id = tg_node_group.interface.items_tree["Width"].identifier
            depth_id = tg_node_group.interface.items_tree["Depth"].identifier

            top_thickness_id = tg_node_group.interface.items_tree[
                "Top Thickness"
            ].identifier
            top_curvature_id = tg_node_group.interface.items_tree[
                "Top Curvature"
            ].identifier

            apron_size_reduction_id = tg_node_group.interface.items_tree[
                "Apron Size Reduction"
            ].identifier
            apron_thickness_id = tg_node_group.interface.items_tree[
                "Apron Thickness"
            ].identifier

            leg_width_id = tg_node_group.interface.items_tree["Leg Width"].identifier
            leg_thickness_id = tg_node_group.interface.items_tree[
                "Leg Thickness"
            ].identifier
            leg_angle_id = tg_node_group.interface.items_tree["Leg Angle"].identifier

            ##################################################################################

            tg_mod[round_table_id] = self.round_table
            tg_mod[round_apron_id] = self.round_apron

            tg_mod[height_id] = self.height
            tg_mod[width_id] = self.width
            tg_mod[depth_id] = self.depth

            tg_mod[top_thickness_id] = self.top_thickness
            tg_mod[top_curvature_id] = self.top_curvature

            tg_mod[apron_thickness_id] = self.apron_thickness

            tg_node_group.interface_update(context)

            ## Must be at the end, can only be calculated after every other attribute is registered
            ## ORDER IS VERY IMPORTANT HERE

            table_area_max_width = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["table_area_max_width"]
                    .data
                ]
            )

            table_area_max_depth = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["table_area_max_depth"]
                    .data
                ]
            )

            self.leg_width = np.random.choice(
                np.arange(0.03, table_area_max_width / 2, 0.001)
            )
            self.leg_thickness = np.random.choice(
                np.arange(0.03, table_area_max_depth / 2, 0.001)
            )

            self.apron_size_reduction = np.random.choice(
                np.arange(
                    0,
                    np.minimum(
                        table_area_max_width - (2 * self.leg_width),
                        table_area_max_depth - (2 * self.leg_thickness),
                    ),
                    0.001,
                )
            )

            if self.apron_size_reduction <= 0:
                self.leg_angle = 0
            else:
                self.leg_angle = np.random.choice(
                    np.arange(0, self.apron_size_reduction / 2, 0.01)
                )

            tg_mod[apron_size_reduction_id] = self.apron_size_reduction

            tg_mod[leg_width_id] = self.leg_width
            tg_mod[leg_thickness_id] = self.leg_thickness
            tg_mod[leg_angle_id] = float(self.leg_angle)

            tg_node_group.interface_update(context)

    def randomize_material(self, context):

        table_obj = ColorPaletteRandomizer().get_dining_room_object(
            obj_name="table",
            path_to_material_list=ColorPaletteRandomizer().material_list_url,
        )
        table_top_color_palette = (
            ColorPaletteRandomizer().pick_random_material_and_color_palette(
                table_obj, "materials_top", ColorPaletteRandomizer().material_folder_url
            )
        )
        self.table_top_mat = (
            f"Procedural {table_top_color_palette[0]['material']} Table Top"
        )
        self.table_top_col_palette = table_top_color_palette[1]

        table_bottom_color_palette = (
            ColorPaletteRandomizer().pick_random_material_and_color_palette(
                table_obj,
                "materials_bottom",
                ColorPaletteRandomizer().material_folder_url,
            )
        )

        self.table_bot_mat = (
            f"Procedural {table_bottom_color_palette[0]['material']} Table Bottom"
        )
        self.table_bot_col_palette = table_bottom_color_palette[1]

        if "Table Generator" in context.object.modifiers:
            tg_mod = context.object.modifiers["Table Generator"]
            tg_node_group = tg_mod.node_group

            top_mat = bpy.data.materials[self.table_top_mat]

            if "rgb" in self.table_top_col_palette:
                self.table_top_col_palette = ColorPaletteRandomizer().get_random_rgba()
                top_mat.node_tree.nodes["Group"].inputs[
                    f"Color {1}"
                ].default_value = self.table_top_col_palette

            else:
                for i, hex_color in enumerate(self.table_top_col_palette, 1):
                    top_mat.node_tree.nodes["Group"].inputs[
                        f"Color {i}"
                    ].default_value = ColorPaletteRandomizer().hex_color_str_to_rgba(
                        hex_color
                    )

            if "Rotation" in top_mat.node_tree.nodes["Group"].inputs.keys():
                # Rotate on Z-Axis
                self.table_top_mat_rot = ColorPaletteRandomizer().get_random_rotation()
                top_mat.node_tree.nodes["Group"].inputs["Rotation"].default_value[
                    2
                ] = self.table_top_mat_rot
            else:
                self.table_top_mat_rot = 0

            top_mat_id = tg_node_group.interface.items_tree[
                "Table Top Material"
            ].identifier
            tg_mod[top_mat_id] = bpy.data.materials[self.table_top_mat]

            top_mat.node_tree.interface_update(context)

            bottom_mat = bpy.data.materials[self.table_bot_mat]

            if "rgb" in self.table_bot_col_palette:
                self.table_bot_col_palette = ColorPaletteRandomizer().get_random_rgba()
                bottom_mat.node_tree.nodes["Group"].inputs[
                    f"Color {1}"
                ].default_value = self.table_bot_col_palette

            else:
                for i, hex_color in enumerate(self.table_bot_col_palette, 1):
                    bottom_mat.node_tree.nodes["Group"].inputs[
                        f"Color {i}"
                    ].default_value = ColorPaletteRandomizer().hex_color_str_to_rgba(
                        hex_color
                    )

            if "Rotation" in bottom_mat.node_tree.nodes["Group"].inputs.keys():
                # Rotate on Z-Axis
                self.table_bot_mat_rot = ColorPaletteRandomizer().get_random_rotation()
                bottom_mat.node_tree.nodes["Group"].inputs["Rotation"].default_value[
                    2
                ] = self.table_bot_mat_rot
            else:
                self.table_bot_mat_rot = 0

            bottom_mat_id = tg_node_group.interface.items_tree[
                "Table Bottom Material"
            ].identifier
            tg_mod[bottom_mat_id] = bpy.data.materials[self.table_bot_mat]

            bottom_mat.node_tree.interface_update(context)

            tg_node_group.interface_update(context)


class ProceduralDistractor(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralDistractor, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.max_length = 0
        self.max_height = 0
        self.max_segments = 0
        self.random_seed = 0
        self.distractor_mat_random_seed = 0
        self.distractor_mat_rotation = (0, 0, 0)
        self.distractor_mat_color1 = (0, 0, 0)
        self.distractor_mat_color2 = (0, 0, 0)
        self.distractor_mat_color3 = (0, 0, 0)

    def create_distractor(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.object.name = "distractor"

        dg_mod = bpy.context.object.modifiers.new("Distractor Generator", "NODES")
        if "distractor_generator" in bpy.data.node_groups.keys():
            dg_node_tree = bpy.data.node_groups["distractor_generator"]
        else:
            self.report({"ERROR"}, "WIP: Distractor Generator Node Tree not found.")
        dg_mod.node_group = dg_node_tree

    def randomize_distractor(self, context):
        if "Distractor Generator" in context.object.modifiers:
            dg_mod = context.object.modifiers["Distractor Generator"]
            dg_node_group = dg_mod.node_group

            self.max_length = np.random.choice(np.arange(0.05, 0.2, 0.01))
            self.max_height = np.random.choice(np.arange(0.05, 0.3, 0.01))
            self.max_segments = 64
            self.random_seed = np.random.choice(np.arange(-10000, 10000, 1))

            ##################################################################################

            max_length_id = dg_node_group.interface.items_tree["Max Length"].identifier
            max_height_id = dg_node_group.interface.items_tree["Max Height"].identifier
            max_segments_id = dg_node_group.interface.items_tree[
                "Max Segments"
            ].identifier
            random_seed_id = dg_node_group.interface.items_tree[
                "Random Seed"
            ].identifier

            ##################################################################################

            dg_mod[max_length_id] = self.max_length
            dg_mod[max_height_id] = self.max_height
            dg_mod[max_segments_id] = self.max_segments
            dg_mod[random_seed_id] = int(self.random_seed)

            dg_node_group.interface_update(context)

        else:
            print("Object does not have the 'Distractor Generator' Modifier")
            self.report(
                {"ERROR"}, "Object does not have the 'Distractor Generator' Modifier"
            )

    def randomize_material(self, context):

        if "Distractor Generator" in context.object.modifiers:
            dg_mod = context.object.modifiers["Distractor Generator"]
            dg_node_group = dg_mod.node_group

            distractor_mat_id = dg_node_group.interface.items_tree[
                "Material"
            ].identifier

            distractor_mat = dg_mod[distractor_mat_id]

            self.distractor_mat_random_seed = np.random.choice(
                np.arange(-10000, 10000, 1)
            )
            self.distractor_mat_color1 = ColorPaletteRandomizer().get_random_rgba()
            self.distractor_mat_color2 = ColorPaletteRandomizer().get_random_rgba()
            self.distractor_mat_color3 = ColorPaletteRandomizer().get_random_rgba()
            self.distractor_mat_rotation = [
                ColorPaletteRandomizer().get_random_rotation(),
                ColorPaletteRandomizer().get_random_rotation(),
                ColorPaletteRandomizer().get_random_rotation(),
            ]

            distractor_mat.node_tree.nodes["Group"].inputs[
                "Random"
            ].default_value = self.distractor_mat_random_seed
            distractor_mat.node_tree.nodes["Group"].inputs[
                "Rotation"
            ].default_value = self.distractor_mat_rotation
            distractor_mat.node_tree.nodes["Group"].inputs[
                "Color 1"
            ].default_value = self.distractor_mat_color1
            distractor_mat.node_tree.nodes["Group"].inputs[
                "Color 2"
            ].default_value = self.distractor_mat_color2
            distractor_mat.node_tree.nodes["Group"].inputs[
                "Color 3"
            ].default_value = self.distractor_mat_color3

            distractor_mat.node_tree.interface_update(context)


class ProceduralRoom:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProceduralRoom, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.room_area = 40
        self.construct_floor_random_seed = 0

        self.wall_height = 0
        self.wall_thickness = 0
        self.baseboard_height = 0
        self.baseboard_width = 0
        self.table_location_random_seed = 0

        self.amount_of_windows = 0
        self.window_height = 0
        self.window_width = 0
        self.window_frame_thickness = 0
        self.window_frame_depth = 0
        self.window_depth = 0
        self.window_thickness = 0
        self.glass_thickness = 0
        self.min_glass_height = 1.30
        self.distance_to_ceiling = 0
        self.distance_to_ground = 0
        self.distance_to_corner = 0
        self.window_height_pos = 0
        self.window_distribution_random_seed = 0

        self.indoor_lighting = False
        self.room_lumen_per_sqm = 0
        self.lumen_per_light_bulb = 800
        self.amount_of_lights = 0
        self.light_distribution_random_seed = 0

        self.room_wall_mat = ""
        self.room_wall_col_palette = ""
        self.room_wall_mat_rot = 0
        self.room_floor_mat = ""
        self.room_floor_col_palette = ""
        self.room_floor_mat_rot = 0

    def create_room(self, context):

        self.construct_floor_random_seed = np.random.choice(np.arange(-5000, 5000, 1))
        floor_obj = self.construct_random_floor(
            used_floor_area=self.room_area,
            random_seed=int(self.construct_floor_random_seed),
        )

        bpy.ops.object.select_all(action="DESELECT")
        floor_obj.select_set(True)
        bpy.context.view_layer.objects.active = floor_obj

        rg_mod = bpy.context.object.modifiers.new("Room Generator", "NODES")
        if "room_generator" in bpy.data.node_groups.keys():
            rg_node_tree = bpy.data.node_groups["room_generator"]
        else:
            self.report({"ERROR"}, "WIP: Room Generator Node Tree not found.")

        rg_mod.node_group = rg_node_tree
        self.randomize_room(context)

        solidify_mod = bpy.context.object.modifiers.new("Solidify", "SOLIDIFY")
        solidify_mod.thickness = 0.0001
        solidify_mod.use_even_offset = True
        solidify_mod.use_rim = True

    def randomize_room(self, context):
        if "Room Generator" in context.object.modifiers:
            rg_mod = context.object.modifiers["Room Generator"]
            rg_node_group = rg_mod.node_group

            self.amount_of_windows = np.random.choice(np.arange(1, 6, 1))
            self.wall_height = np.random.choice(np.arange(2.3, 2.5, 0.01))

            max_room_width = np.max(context.object.dimensions[:2])

            self.window_width = (max_room_width * 0.55) / self.amount_of_windows

            self.wall_thickness = np.random.choice(np.arange(0.365, 0.49, 0.001))
            self.baseboard_height = np.random.choice(np.arange(0.079, 0.14, 0.001))
            self.baseboard_width = np.random.choice(np.arange(0.011, 0.016, 0.001))
            self.table_location_random_seed = np.random.choice(np.arange(0, 5000, 1))

            self.distance_to_ceiling = np.random.choice(np.arange(0.01, 0.3, 0.01))
            self.distance_to_ground = np.random.choice(np.arange(0.8, 0.95, 0.01))
            self.window_frame_thickness = np.random.choice(
                np.arange(0.015, 0.03, 0.001)
            )
            self.window_frame_depth = np.random.choice(np.arange(0.07, 0.095, 0.001))
            self.window_depth = np.random.choice(np.arange(0.015, 0.025, 0.001))
            self.window_thickness = np.random.choice(np.arange(0.05, 0.1, 0.001))
            self.glass_thickness = np.random.choice(np.arange(0.006, 0.01, 0.001))
            self.window_distribution_random_seed = np.random.choice(
                np.arange(0, 5000, 1)
            )

            min_window_height = (
                self.min_glass_height
                + self.window_frame_thickness
                + self.window_thickness
            )
            max_window_height = (
                self.wall_height - self.distance_to_ceiling - self.distance_to_ground
            )

            if min_window_height < max_window_height:
                self.window_height = np.random.choice(
                    np.arange(
                        self.min_glass_height
                        + self.window_frame_thickness
                        + self.window_thickness,
                        self.wall_height
                        - self.distance_to_ceiling
                        - self.distance_to_ground,
                        0.001,
                    )
                )
            else:
                self.window_height = max_window_height

            self.window_height_pos = self.distance_to_ground + (self.window_height / 2)

            self.indoor_lighting = random.choice([True, False])
            self.room_lumen_per_sqm = np.random.choice(np.arange(600, 800, 1))
            self.amount_of_lights = np.floor(
                (self.room_lumen_per_sqm * self.room_area) / self.lumen_per_light_bulb
            )
            self.light_distribution_random_seed = np.random.choice(
                np.arange(0, 5000, 1)
            )

            wall_height_id = rg_node_group.interface.items_tree[
                "Wall Height"
            ].identifier
            wall_thickness_id = rg_node_group.interface.items_tree[
                "Wall Thickness"
            ].identifier
            baseboard_height_id = rg_node_group.interface.items_tree[
                "Baseboard Height"
            ].identifier
            baseboard_width_id = rg_node_group.interface.items_tree[
                "Baseboard Width"
            ].identifier
            table_location_random_seed_id = rg_node_group.interface.items_tree[
                "Table Location Random Seed"
            ].identifier

            amount_of_windows_id = rg_node_group.interface.items_tree[
                "Amount of Windows"
            ].identifier
            window_height_id = rg_node_group.interface.items_tree[
                "Window Height"
            ].identifier
            window_width_id = rg_node_group.interface.items_tree[
                "Window Width"
            ].identifier
            window_frame_thickness_id = rg_node_group.interface.items_tree[
                "Window Frame Thickness"
            ].identifier
            window_frame_depth_id = rg_node_group.interface.items_tree[
                "Window Frame Depth"
            ].identifier
            window_thickness_id = rg_node_group.interface.items_tree[
                "Window Thickness"
            ].identifier
            window_depth_id = rg_node_group.interface.items_tree[
                "Window Depth"
            ].identifier
            glass_thickness_id = rg_node_group.interface.items_tree[
                "Glass Thickness"
            ].identifier
            window_height_pos_id = rg_node_group.interface.items_tree[
                "Window Height Position"
            ].identifier
            window_distribution_random_seed = rg_node_group.interface.items_tree[
                "Window Distribution Random Seed"
            ].identifier

            indoor_lighting_id = rg_node_group.interface.items_tree[
                "Indoor Lighting"
            ].identifier
            amount_of_lights_id = rg_node_group.interface.items_tree[
                "Amount of Lights"
            ].identifier
            light_distribution_random_seed_id = rg_node_group.interface.items_tree[
                "Light Distribution Random Seed"
            ].identifier

            rg_mod[wall_height_id] = self.wall_height
            rg_mod[wall_thickness_id] = self.wall_thickness
            rg_mod[baseboard_height_id] = self.baseboard_height
            rg_mod[baseboard_width_id] = self.baseboard_width
            rg_mod[table_location_random_seed_id] = int(self.table_location_random_seed)

            rg_mod[amount_of_windows_id] = int(self.amount_of_windows)
            rg_mod[window_height_id] = self.window_height
            rg_mod[window_width_id] = self.window_width
            rg_mod[window_frame_thickness_id] = self.window_frame_thickness
            rg_mod[window_frame_depth_id] = self.window_frame_depth
            rg_mod[window_thickness_id] = self.window_thickness
            rg_mod[window_depth_id] = self.window_depth
            rg_mod[glass_thickness_id] = self.glass_thickness
            rg_mod[window_height_pos_id] = self.window_height_pos
            rg_mod[window_distribution_random_seed] = int(
                self.window_distribution_random_seed
            )

            rg_mod[indoor_lighting_id] = self.indoor_lighting
            rg_mod[amount_of_lights_id] = int(self.amount_of_lights)
            rg_mod[light_distribution_random_seed_id] = int(
                self.light_distribution_random_seed
            )

            rg_node_group.interface_update(context)

        else:
            print("Object does not have 'Room Generator' Modifier")
            self.report({"ERROR"}, "Object does not have 'Room Generator' Modifier")

    def randomize_material(self, context):

        room_obj = ColorPaletteRandomizer().get_dining_room_object(
            obj_name="room",
            path_to_material_list=ColorPaletteRandomizer().material_list_url,
        )
        room_floor_color_palette = (
            ColorPaletteRandomizer().pick_random_material_and_color_palette(
                room_obj,
                "floor_materials",
                ColorPaletteRandomizer().material_folder_url,
            )
        )
        self.room_floor_mat = (
            f"Procedural {room_floor_color_palette[0]['material']} Floor"
        )
        self.room_floor_col_palette = room_floor_color_palette[1]

        room_wall_color_palette = (
            ColorPaletteRandomizer().pick_random_material_and_color_palette(
                room_obj, "wall_materials", ColorPaletteRandomizer().material_folder_url
            )
        )
        self.room_wall_mat = f"Procedural {room_wall_color_palette[0]['material']} Wall"
        self.room_wall_col_palette = room_wall_color_palette[1]

        if "Room Generator" in context.object.modifiers:
            rg_mod = context.object.modifiers["Room Generator"]
            rg_node_group = rg_mod.node_group

            floor_mat = bpy.data.materials[self.room_floor_mat]

            if "rgb" in self.room_floor_col_palette:
                self.room_floor_col_palette = ColorPaletteRandomizer().get_random_rgba()
                floor_mat.node_tree.nodes["Group"].inputs[
                    f"Color {1}"
                ].default.value = self.room_floor_col_palette
            else:
                for i, hex_color in enumerate(self.room_floor_col_palette, 1):

                    floor_mat.node_tree.nodes["Group"].inputs[
                        f"Color {i}"
                    ].default_value = ColorPaletteRandomizer().hex_color_str_to_rgba(
                        hex_color
                    )

            if "Rotation" in floor_mat.node_tree.nodes["Group"].inputs.keys():
                # Rotate on Z-Axis
                self.room_floor_mat_rot = ColorPaletteRandomizer().get_random_rotation()
                floor_mat.node_tree.nodes["Group"].inputs["Rotation"].default_value[
                    2
                ] = self.room_floor_mat_rot
            else:
                self.room_floor_mat_rot = 0

            floor_mat_id = rg_node_group.interface.items_tree[
                "Floor Material"
            ].identifier
            rg_mod[floor_mat_id] = bpy.data.materials[self.room_floor_mat]

            floor_mat.node_tree.interface_update(context)

            wall_mat = bpy.data.materials[self.room_wall_mat]

            if "rgb" in self.room_wall_col_palette:
                self.room_wall_col_palette = ColorPaletteRandomizer().get_random_rgba()
                wall_mat.node_tree.nodes["Group"].inputs[
                    f"Color {1}"
                ].default_value = self.room_wall_col_palette
            else:
                for i, hex_color in enumerate(self.room_wall_col_palette, 1):
                    wall_mat.node_tree.nodes["Group"].inputs[
                        f"Color {i}"
                    ].default_value = ColorPaletteRandomizer().hex_color_str_to_rgba(
                        hex_color
                    )

            if "Rotation" in wall_mat.node_tree.nodes["Group"].inputs.keys():
                # Rotate on Z-Axis
                self.room_wall_mat_rot = ColorPaletteRandomizer().get_random_rotation()
                wall_mat.node_tree.nodes["Group"].inputs["Rotation"].default_value[
                    2
                ] = self.room_wall_mat_rot
            else:
                self.room_wall_mat_rot = 0

            wall_mat_id = rg_node_group.interface.items_tree["Wall Material"].identifier
            rg_mod[wall_mat_id] = bpy.data.materials[self.room_wall_mat]

            wall_mat.node_tree.interface_update(context)

            rg_node_group.interface_update(context)

    def construct_random_floor(
        self,
        random_seed,
        used_floor_area: float = 40,
        amount_of_extrusions: int = 3,
        fac_from_square_room: float = 0.0,
        corridor_width: float = 1.5,
        amount_of_floor_cuts: int = 2,
        only_use_big_edges: bool = True,
    ):

        if not bpy.context.object or bpy.context.object.mode == "OBJECT":

            random.seed(random_seed)

            # if there is more than one extrusions, the used floor area must be split over all sections
            # the first section should be at least 60% - 80% big, after that the size depends on the amount of left
            # floor values
            if amount_of_extrusions > 1:
                size_sequence = []
                running_sum = 0.0
                start_minimum = 0.0
                for i in range(amount_of_extrusions - 1):
                    if i == 0:
                        size_sequence.append(random.uniform(0.6, 0.8))
                        start_minimum = (1.0 - size_sequence[-1]) / amount_of_extrusions
                    else:
                        if start_minimum < 1.0 - running_sum:
                            size_sequence.append(
                                random.uniform(start_minimum, 1.0 - running_sum)
                            )
                        else:
                            break
                    running_sum += size_sequence[-1]
                if 1.0 - running_sum > 1e-7:
                    size_sequence.append(1.0 - running_sum)
                if amount_of_extrusions != len(size_sequence):
                    print(
                        f"Amount of extrusions was reduced to: {len(size_sequence)}. To avoid rooms, "
                        f"which are smaller than 1e-7"
                    )
                    self.report(
                        {"WARNING"},
                        f"Amount of extrusions was reduced to: {len(size_sequence)}. To avoid rooms, "
                        f"which are smaller than 1e-7",
                    )
                    amount_of_extrusions = len(size_sequence)
            else:
                size_sequence = [1.0]

            # this list of areas is then used to calculate the extrusions
            # if there is only one element in there, it will create a rectangle
            used_floor_areas = [size * used_floor_area for size in size_sequence]

            # calculate the squared room length for the base room
            squared_room_length = np.sqrt(used_floor_areas[0])

            # create a new plane and rename it to Wall
            bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
            room_obj = bpy.context.object
            room_obj.name = "room"

            # calculate the side length of the base room, for that the `fac_from_square_room` is used
            room_length_x = (
                fac_from_square_room * random.uniform(-1, 1) * squared_room_length
                + squared_room_length
            )
            # make sure that the floor area is still used
            room_length_y = used_floor_areas[0] / room_length_x

            # change the plane to this size
            bpy.ops.object.select_all(action="DESELECT")
            room_obj.select_set(True)
            bpy.context.view_layer.objects.active = room_obj
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.transform.resize(
                value=(room_length_x * 0.5, room_length_y * 0.5, 1)
            )
            bpy.ops.object.mode_set(mode="OBJECT")

            def cut_plane(plane: bpy.types.Object):

                # save the size of the plane to determine a best split value
                x_size = np.array(plane.scale)[0]
                y_size = np.array(plane.scale)[1]

                # switch to edit mode and select all faces
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action="SELECT")
                bpy.ops.object.mode_set(mode="OBJECT")

                # convert plane to BMesh object
                bm = bmesh.new()
                bm.from_mesh(plane.data)
                bm.faces.ensure_lookup_table()

                # find all selected edges
                edges = [edge for edge in bm.edges if edge.select]

                biggest_face_id = np.argmax([f.calc_area() for f in bm.faces])
                biggest_face = bm.faces[biggest_face_id]

                # find the biggest face
                faces = [face for face in bm.faces if face == biggest_face]
                geom = []
                geom.extend(edges)
                geom.extend(faces)

                # calculate cutting point
                cutting_point = [
                    x_size * random.uniform(-1, 1),
                    y_size * random.uniform(-1, 1),
                    0,
                ]
                # select a random axis to specify in which direction to cut
                direction_axis = [1, 0, 0] if random.uniform(0, 1) < 0.5 else [0, 1, 0]

                # cut the plane and update the final mesh
                bmesh.ops.bisect_plane(
                    bm,
                    dist=0.01,
                    geom=geom,
                    plane_co=cutting_point,
                    plane_no=direction_axis,
                )

                if bm.is_wrapped:
                    bmesh.update_edit_mesh(plane.data)
                else:
                    bm.to_mesh(plane.data)
                    bm.free()

                plane.data.update()

            # for each floor cut perform one cut_plane
            for i in range(amount_of_floor_cuts):
                cut_plane(room_obj)

            # do several extrusions of the basic floor plan, the first one is always the basic one
            for i in range(1, amount_of_extrusions):
                # Change to edit mode of the selected floor
                bpy.ops.object.select_all(action="DESELECT")
                room_obj.select_set(True)
                bpy.context.view_layer.objects.active = room_obj
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action="DESELECT")
                bm = bmesh.from_edit_mesh(room_obj.data)
                bm.faces.ensure_lookup_table()
                bm.edges.ensure_lookup_table()

                # calculate the size of all edges and find all edges, which are wider than the minimum corridor_width
                # to avoid that super small, super long pieces are created
                boundary_edges = [edge for edge in bm.edges if edge.is_boundary]
                boundary_sizes = [(edge, edge.calc_length()) for edge in boundary_edges]
                boundary_sizes = [
                    (edge, size)
                    for edge, size in boundary_sizes
                    if size > corridor_width
                ]

                if len(boundary_sizes) > 0:
                    # sort the boundaries to focus oonly on the big ones
                    boundary_sizes.sort(key=lambda edge: edge[1])
                    if only_use_big_edges:
                        # only select the bigger half of the selected boundaries
                        half_size = len(boundary_sizes) // 2
                    else:
                        # use any of the selected boundaries
                        half_size = 0
                    used_edges = [edge for edge, s in boundary_sizes[half_size:]]

                    random_edge = None
                    shift_vec = None
                    edge_counter = 0
                    random_index = random.randrange(len(used_edges))

                    while edge_counter < len(used_edges):
                        # select a random edge from the choose edges
                        random_edge = used_edges[random_index]

                        # get the direction of the current edge
                        direction = np.abs(
                            random_edge.verts[0].co - random_edge.verts[1].co
                        )
                        # the shift value depends on the used_floor_area size
                        shift_value = used_floor_areas[i] / random_edge.calc_length()

                        # depending if the random edge is aligned with the x-axis or the y-axis,
                        # the shift is the opposite direction
                        if direction[0] == 0:
                            x_shift, y_shift = shift_value, 0
                        else:
                            x_shift, y_shift = 0, shift_value

                        # calculate the vertices for the new face
                        shift_vec = mathutils.Vector([x_shift, y_shift, 0])
                        dir_found = False
                        for tested_dir in [1, -1]:
                            shift_vec *= tested_dir
                            new_verts = [edge.co for edge in random_edge.verts]
                            new_verts.extend([edge + shift_vec for edge in new_verts])
                            new_verts = np.array(new_verts)

                            # check if the newly constructed face is colliding with one of the others
                            # if so generate a new face
                            collision_face_found = False

                            for existing_face in bm.faces:
                                existing_verts = np.array(
                                    [vert.co for vert in existing_face.verts]
                                )

                                @staticmethod
                                def check_bb_intersection_on_values(
                                    min_b1: List[float],
                                    max_b1: List[float],
                                    min_b2: List[float],
                                    max_b2: List[float],
                                    used_check: Callable[
                                        [float, float], bool
                                    ] = lambda a, b: a
                                    >= b,
                                ):
                                    """
                                    Checks if there is an intersection of the given bounding box values. Here we use two different bounding boxes,
                                    namely b1 and b2. Each of them has a corresponding set of min and max values, this works for 2 and 3 dimensional
                                    problems.

                                    :param min_b1: List of minimum bounding box points for b1.
                                    :param max_b1: List of maximum bounding box points for b1.
                                    :param min_b2: List of minimum bounding box points for b2.
                                    :param max_b2: List of maximum bounding box points for b2.
                                    :param used_check: The operation used inside the is_overlapping1D. With that it possible to change the \
                                                    collision check from volume and surface check to pure surface or volume checks.
                                    :return: True if the two bounding boxes intersect with each other
                                    """
                                    collide = True
                                    for (
                                        min_b1_val,
                                        max_b1_val,
                                        min_b2_val,
                                        max_b2_val,
                                    ) in zip(min_b1, max_b1, min_b2, max_b2):
                                        # inspired by this:
                                        # https://stackoverflow.com/questions/20925818/algorithm-to-check-if-two-boxes-overlap
                                        # Checks in each dimension, if there is an overlap if this happens it must be an overlap in 3D, too.
                                        def is_overlapping_1D(
                                            x_min_1, x_max_1, x_min_2, x_max_2
                                        ):
                                            # returns true if the min and max values are overlapping
                                            return used_check(
                                                x_max_1, x_min_2
                                            ) and used_check(x_max_2, x_min_1)

                                        collide = collide and is_overlapping_1D(
                                            min_b1_val,
                                            max_b1_val,
                                            min_b2_val,
                                            max_b2_val,
                                        )
                                    return collide

                                if check_bb_intersection_on_values(
                                    np.min(existing_verts, axis=0)[:2],
                                    np.max(existing_verts, axis=0)[:2],
                                    np.min(new_verts, axis=0)[:2],
                                    np.max(new_verts, axis=0)[:2],
                                    # by using this check an edge collision is ignored
                                    used_check=lambda a, b: a > b,
                                ):
                                    collision_face_found = True
                                    break
                            if not collision_face_found:
                                dir_found = True
                                break
                        if dir_found:
                            break

                        random_index = (random_index + 1) % len(used_edges)
                        edge_counter += 1
                        random_edge = None

                    if random_edge is None:
                        for edge in used_edges:
                            edge.select = True
                        raise Exception(
                            "No edge found to extrude up on! The reason might be that there are to many cuts"
                            "in the basic room or that the corridor width is too high."
                        )

                    # extrude this edge with the calculated shift
                    random_edge.select = True
                    bpy.ops.mesh.extrude_region_move(
                        MESH_OT_extrude_region={
                            "use_normal_flip": False,
                            "use_dissolve_ortho_edges": False,
                            "mirror": False,
                        },
                        TRANSFORM_OT_translate={
                            "value": shift_vec,
                            "orient_type": "GLOBAL",
                        },
                    )

                else:
                    raise Exception(
                        "The corridor width is so big that no edge could be selected, "
                        "reduce the corridor width or reduce the amount of floor cuts."
                    )

                # remove all double vertices, which might occur
                bpy.ops.mesh.select_all(action="SELECT")
                bpy.ops.mesh.remove_doubles()
                bpy.ops.mesh.select_all(action="DESELECT")
                if bm.is_wrapped:
                    bmesh.update_edit_mesh(room_obj.data)
                else:
                    bm.to_mesh(room_obj.data)
                    bm.free()

                bpy.ops.object.mode_set(mode="OBJECT")

        return room_obj

    def randomize_lighting(self, context):
        if "Room Generator" in context.object.modifiers:
            rg_mod = context.object.modifiers["Room Generator"]
            rg_node_group = rg_mod.node_group

            self.indoor_lighting = random.choice([True, False])
            self.room_lumen_per_sqm = np.random.choice(np.arange(600, 800, 1))
            self.amount_of_lights = np.floor(
                (self.room_lumen_per_sqm * self.room_area) / self.lumen_per_light_bulb
            )
            self.light_distribution_random_seed = np.random.choice(
                np.arange(0, 5000, 1)
            )

            indoor_lighting_id = rg_node_group.interface.items_tree[
                "Indoor Lighting"
            ].identifier
            amount_of_lights_id = rg_node_group.interface.items_tree[
                "Amount of Lights"
            ].identifier
            light_distribution_random_seed_id = rg_node_group.interface.items_tree[
                "Light Distribution Random Seed"
            ].identifier

            rg_mod[indoor_lighting_id] = self.indoor_lighting
            rg_mod[amount_of_lights_id] = int(self.amount_of_lights)
            rg_mod[light_distribution_random_seed_id] = int(
                self.light_distribution_random_seed
            )

            rg_node_group.interface_update(context)

        else:
            print("Object does not have 'Room Generator' Modifier")
            self.report({"ERROR"}, "Object does not have 'Room Generator' Modifier")


class DiningRoomDistributor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DiningRoomDistributor, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.distribution_random_seed = 0
        self.tableware_rotation_random_seed = 0
        self.chair_location_random_seed = 0
        self.chair_rotation_random_seed = 0
        self.amount_of_forks = 0
        self.amount_of_glasses = 0
        self.amount_of_knives = 0
        self.amount_of_plates = 0
        self.amount_of_spoons = 0
        self.amount_of_distractors = 0
        self.amount_of_napkins = 0

    def create_distribution(self, context):
        if (
            "Table Generator" in context.object.modifiers
            and "Dining Room Distributor" not in context.object.modifiers
        ):
            drd_mod = bpy.context.object.modifiers.new(
                "Dining Room Distributor", "NODES"
            )
            if "dining_room_distributor" in bpy.data.node_groups.keys():
                drd_node_tree = bpy.data.node_groups["dining_room_distributor"]
            else:
                self.report({"ERROR"}, "WIP: Dining Room Distributor Tree not found.")

            drd_mod.node_group = drd_node_tree
            self.randomize_distribution(context)
        else:
            print(
                "Object does not have 'Table Generator' or does have 'Dining Room Distributor' Modifier already"
            )
            self.report(
                {"ERROR"},
                "Object does not have 'Table Generator' or does have 'Dining Room Distributor' Modifier already",
            )

    def randomize_distribution(self, context):
        if "Dining Room Distributor" in context.object.modifiers:
            drd_mod = context.object.modifiers["Dining Room Distributor"]
            drd_node_group = drd_mod.node_group

            self.distribution_random_seed = np.random.choice(np.arange(0, 5000, 1))
            self.tableware_rotation_random_seed = np.random.choice(
                np.arange(0, 5000, 1)
            )
            self.chair_location_random_seed = np.random.choice(np.arange(0, 5000, 1))
            self.chair_rotation_random_seed = np.random.choice(np.arange(0, 5000, 1))

            distribution_random_seed_id = drd_node_group.interface.items_tree[
                "Distribution Random Seed"
            ].identifier
            tableware_rotation_random_seed_id = drd_node_group.interface.items_tree[
                "Tableware Rotation Random Seed"
            ].identifier
            chair_location_random_seed_id = drd_node_group.interface.items_tree[
                "Chair Location Random Seed"
            ].identifier
            chair_rotation_random_seed_id = drd_node_group.interface.items_tree[
                "Chair Rotation Random Seed"
            ].identifier

            drd_mod[distribution_random_seed_id] = int(self.distribution_random_seed)
            drd_mod[tableware_rotation_random_seed_id] = int(
                self.tableware_rotation_random_seed
            )
            drd_mod[chair_location_random_seed_id] = int(
                self.chair_location_random_seed
            )
            drd_mod[chair_rotation_random_seed_id] = int(
                self.chair_rotation_random_seed
            )

            drd_node_group.interface_update(context)

            self.amount_of_forks = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["amount_of_forks"]
                    .data
                ]
            )

            self.amount_of_glasses = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["amount_of_glasses"]
                    .data
                ]
            )

            self.amount_of_knives = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["amount_of_knives"]
                    .data
                ]
            )

            self.amount_of_plates = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["amount_of_plates"]
                    .data
                ]
            )

            self.amount_of_spoons = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["amount_of_spoons"]
                    .data
                ]
            )

            self.amount_of_distractors = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["amount_of_distractors"]
                    .data
                ]
            )

            self.amount_of_napkins = np.max(
                [
                    v.value
                    for v in context.object.evaluated_get(
                        context.evaluated_depsgraph_get()
                    )
                    .data.attributes["amount_of_napkins"]
                    .data
                ]
            )

        else:
            print("Object does not have 'Dining Room Distributor' Modifier")
            self.report(
                {"ERROR"}, "Object does not have 'Dining Room Distributor' Modifier"
            )


class SceneRenderer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SceneRenderer, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.main_scene_name = "image_scene"
        self.exec_start_time = 0
        self.curr_start_time = 0
        self.render_time = 0
        self.exec_time = 0

    def select_scene_object(self, select_object):
        bpy.ops.object.select_all(action="DESELECT")
        select_object.select_set(True)
        bpy.context.view_layer.objects.active = select_object

    def randomize_scene(self, context, data_logger):

        ### Generate Room

        # Delete Old Room
        render_collection = bpy.data.collections["Render Collection"]

        while render_collection.objects:
            curr_ob = render_collection.objects[0]
            render_collection.objects.unlink(curr_ob)
            bpy.data.objects.remove(curr_ob, do_unlink=True)

        # Create new Room
        context.view_layer.active_layer_collection = (
            bpy.data.scenes[self.main_scene_name]
            .view_layers["ViewLayer"]
            .layer_collection.children[render_collection.name]
        )

        ### Randomize Room
        procedural_room = ProceduralRoom()
        procedural_room.create_room(context)
        room_obj = bpy.data.objects["room"]
        self.select_scene_object(room_obj)
        procedural_room.randomize_room(context)
        procedural_room.randomize_material(context)
        data_logger.datalog_room(procedural_room)

        ### Randomize Lighting
        room_obj = bpy.data.objects["room"]
        self.select_scene_object(room_obj)
        lighting_randomizer = LightingRandomizer()
        lighting_randomizer.randomize_environment_lighting(context)
        lighting_randomizer.randomize_indoor_lighting(context)
        data_logger.datalog_lighting(procedural_room, lighting_randomizer)

        ### Randomize Tableware Attributes

        # Fork
        fork_obj = bpy.data.objects["fork"]
        self.select_scene_object(fork_obj)
        procedural_fork = ProceduralFork()
        procedural_fork.randomize_fork(context)
        data_logger.datalog_fork(procedural_fork)

        # Glass
        glass_obj = bpy.data.objects["glass"]
        self.select_scene_object(glass_obj)
        procedural_glass = ProceduralGlass()
        procedural_glass.randomize_glass(context)
        data_logger.datalog_glass(procedural_glass)

        # Knife
        knife_obj = bpy.data.objects["knife"]
        self.select_scene_object(knife_obj)
        procedural_knife = ProceduralKnife()
        procedural_knife.randomize_knife(context)
        data_logger.datalog_knife(procedural_knife)

        # Plate
        plate_obj = bpy.data.objects["plate"]
        self.select_scene_object(plate_obj)
        procedural_plate = ProceduralPlate()
        procedural_plate.randomize_plate(context)
        procedural_plate.randomize_crumbs(context)
        procedural_plate.randomize_tableware_on_plate(context)
        procedural_plate.randomize_soil_material(context)
        data_logger.datalog_plate(procedural_plate)

        # Randomize Objects on Plates
        plate_alts_list = [
            plate_alt
            for plate_alt in bpy.data.objects
            if plate_alt.name.startswith("plate_alt")
        ]
        procedural_plat_alt = ProceduralPlate()
        for i, plate_alt in enumerate(plate_alts_list):
            self.select_scene_object(plate_alt)
            procedural_plat_alt.randomize_plate(context)
            procedural_plat_alt.randomize_crumbs(context)
            procedural_plat_alt.randomize_tableware_on_plate(context)
            procedural_plat_alt.randomize_soil_material(context)

        # Spoon
        spoon_obj = bpy.data.objects["spoon"]
        self.select_scene_object(spoon_obj)
        procedural_spoon = ProceduralSpoon()
        procedural_spoon.randomize_spoon(context)
        data_logger.datalog_spoon(procedural_spoon)

        # Distractor
        distractor_list = [
            distractor
            for distractor in bpy.data.objects
            if distractor.name.startswith("distractor")
        ]
        procedural_distractor = ProceduralDistractor()
        for i, distractor in enumerate(distractor_list):
            self.select_scene_object(distractor)
            procedural_distractor.randomize_distractor(context)
            procedural_distractor.randomize_material(context)
            data_logger.datalog_distractor(procedural_distractor, i)

        # Randomize Napkin Materials
        napkin_mat_key_list = [
            mat_key
            for mat_key in bpy.data.materials.keys()
            if mat_key.startswith("Napkin")
        ]

        for i, mat_key in enumerate(napkin_mat_key_list):
            napkin_mat = bpy.data.materials[mat_key]

            random_col = ColorPaletteRandomizer().get_random_rgba()
            napkin_mat.node_tree.nodes["Group"].inputs[
                "Color"
            ].default_value = random_col

            data_logger.datalog_napkin_mat(random_col, i)

        ### Randomize Furniture Attributes + Material

        # Chair
        chair_obj = bpy.data.objects["chair"]
        self.select_scene_object(chair_obj)
        procedural_chair = ProceduralChair()
        procedural_chair.randomize_chair(context)
        procedural_chair.randomize_material(context)
        data_logger.datalog_chair(procedural_chair)

        # Table
        table_obj = bpy.data.objects["table"]
        self.select_scene_object(table_obj)
        procedural_table = ProceduralTable()
        procedural_table.randomize_table(context)
        procedural_table.randomize_material(context)
        data_logger.datalog_table(procedural_table)

        # Randomize Dining Room Distribution
        table_obj = bpy.data.objects["table"]
        self.select_scene_object(table_obj)
        dining_room_distributor = DiningRoomDistributor()
        dining_room_distributor.randomize_distribution(context)
        data_logger.datalog_table_distribution(dining_room_distributor)

        ### Randomize Camera
        # Set Table Top Material for Selection in Room to randomize Camera
        rg_mod = room_obj.modifiers["Room Generator"]
        rg_node_group = rg_mod.node_group
        tg_mod = table_obj.modifiers["Table Generator"]
        tg_node_group = tg_mod.node_group

        rg_mod[rg_node_group.interface.items_tree["Table Top Material"].identifier] = (
            tg_mod[tg_node_group.interface.items_tree["Table Top Material"].identifier]
        )

        # Set Camera
        room_obj = bpy.data.objects["room"]
        self.select_scene_object(room_obj)
        camera_randomizer = CameraRandomizer()
        camera_randomizer.randomize_camera_position(context)
        data_logger.datalog_camera(camera_randomizer)

    def time_seed(self, operator):
        """
        Sets random seed based on the time and copies the seed into the clipboard.

        Returns:
        - seed (int): The random seed based on the current time.
        """

        seed = int(time.time())
        print(f"Seed: {seed}")
        operator.report({"INFO"}, f"Seed: {seed}")
        random.seed(seed)

        bpy.context.window_manager.clipboard = str(seed)

        return seed

    def setup_scene(self, operator, index, data_logger, random_seed=0):
        """
        Sets up the scene for rendering with specified index and seed

        Args:
        - index (int): index of the image
        - seed (float, optional): The random seed to use.
            If not provided a new seed will be generated based on the current time.

        """

        if random_seed:
            random.seed(random_seed)
        else:
            random_seed = self.time_seed(operator)

        # project_name = "dirty_dining_room_dataset"
        # render_dir_path = pathlib.Path.cwd() / project_name
        # render_dir_path.parent.mkdir(parents=True, exist_ok=True)

        render_dir_path = pathlib.Path(
            f"{bpy.context.scene.render_filepath}"
        )  # / project_name"
        # render_dir_path.parent.mkdir(parents=True, exist_ok=True)

        img_name = f"img_{index}_{random_seed}"
        gt_name = f"gt_{index}_{random_seed}"

        bpy.context.scene.render.image_settings.file_format = "JPEG"
        bpy.context.scene.render.filepath = str(render_dir_path)

        bpy.data.scenes[self.main_scene_name].node_tree.nodes[
            "File Output"
        ].base_path = str(render_dir_path)
        bpy.data.scenes[self.main_scene_name].node_tree.nodes["File Output"].file_slots[
            0
        ].path = img_name
        bpy.data.scenes[self.main_scene_name].node_tree.nodes["File Output"].file_slots[
            1
        ].path = gt_name

        data_logger.scene_index = index
        data_logger.scene_datetime = datetime.datetime.now()
        data_logger.scene_seed = random_seed

    def prepare_and_render_scene(
        self,
        operator,
        index,
        start_idx,
        amount_of_imgs,
        context,
        data_logger,
        seed=None,
    ):
        """
        Prepares and renders the scene with the specified index and seed

        Args:
        - index (int): index of the image
        - seed(float, optional): The random seed to use.
            If not provided, a new seed will be generated based on the current time

        """
        print("Setting up and randomize the scene.")
        operator.report({"INFO"}, "Setting up and randomize the scene.")

        self.setup_scene(
            operator=operator, index=index, data_logger=data_logger, random_seed=seed
        )
        self.randomize_scene(context=context, data_logger=data_logger)

        bpy.app.timers.register(
            lambda: self.render_scene(
                operator=operator,
                context=context,
                data_logger=data_logger,
                curr_index=index,
                start_idx=start_idx,
                amount_of_imgs=amount_of_imgs,
            ),
            first_interval=20,
        )

    def render_start(self, operator, context, start_idx, amount_of_imgs):

        bpy.context.scene.render.engine = "CYCLES"
        data_logger = DataLogger()

        self.exec_start_time = time.time()
        print("##########################################")
        print("Start Rendering")
        operator.report({"INFO"}, "Start Rendering")
        print("##########################################")
        print(f"Start Time: {time.asctime(time.gmtime(self.exec_start_time))}")
        operator.report(
            {"INFO"}, f"Start Time: {time.asctime(time.gmtime(self.exec_start_time))}"
        )
        data_logger.start_exec_render_time = self.exec_start_time

        curr_index = start_idx

        for window in context.window_manager.windows:
            for area in window.screen.areas:  # iterate through areas in current screen
                if area.type == "VIEW_3D":
                    for (
                        space
                    ) in area.spaces:  # iterate through spaces in current VIEW_3D area
                        if space.type == "VIEW_3D":  # check if space is a 3D view
                            space.shading.type = "RENDERED"
                            bpy.ops.object.select_camera()
                            bpy.ops.view3d.object_as_camera()

        # Render Image and Ground Truth
        self.prepare_and_render_scene(
            operator=operator,
            index=curr_index,
            start_idx=start_idx,
            amount_of_imgs=amount_of_imgs,
            context=context,
            data_logger=data_logger,
        )

    def render_scene(
        self,
        operator,
        context,
        data_logger,
        curr_index,
        start_idx,
        amount_of_imgs,
    ):
        self.curr_start_time = time.time()

        print(f"Rendering Scene: {time.asctime(time.gmtime(time.time()))}")
        operator.report(
            {"INFO"},
            f"Rendering Scene {curr_index + 1}: {time.asctime(time.gmtime(time.time()))}",
        )

        curr_index = curr_index + 1
        bpy.app.handlers.render_post.append(
            lambda *args, **kwargs: self.render_repeat(
                operator=operator,
                data_logger=data_logger,
                context=context,
                curr_index=curr_index,
                start_idx=start_idx,
                amount_of_imgs=amount_of_imgs,
            )
        )

        bpy.ops.render.render()

    def render_repeat(
        self,
        operator,
        data_logger,
        context,
        curr_index,
        start_idx,
        amount_of_imgs,
    ):
        self.render_time = time.time() - self.curr_start_time
        data_logger.scene_render_time = self.render_time
        data_logger.camera_exposure = bpy.data.scenes[
            self.main_scene_name
        ].view_settings.exposure
        data_logger.create_or_append_csv()
        bpy.app.handlers.render_post.clear()
        print(f"Saving Scene: {time.asctime(time.gmtime(time.time()))}")
        operator.report(
            {"INFO"}, f"Saving Scene: {time.asctime(time.gmtime(time.time()))}"
        )

        if curr_index < (start_idx + amount_of_imgs):
            # Render Image and Ground Truth
            self.prepare_and_render_scene(
                operator=operator,
                index=curr_index,
                context=context,
                data_logger=data_logger,
                start_idx=start_idx,
                amount_of_imgs=amount_of_imgs,
            )
        else:
            exec_time = time.time() - data_logger.start_exec_render_time
            print(f"Execution Time: {time.asctime(time.gmtime(exec_time))}")
            operator.report(
                {"INFO"}, f"Execution Time: {time.asctime(time.gmtime(exec_time))}"
            )


############################ PROPERTIES #############n###############


############################ OPERATORS #############n###############


class DRG_OT_create_plate(bpy.types.Operator):
    """Create a plate object"""

    bl_idname = "drg.create_plate"
    bl_label = "Create Plate"

    def execute(self, context):

        ProceduralPlate().create_plate(context)

        return {"FINISHED"}


class DRG_OT_randomize_plate(bpy.types.Operator):
    """Randomize a plate object"""

    bl_idname = "drg.randomize_plate"
    bl_label = "Randomize Plate"

    def execute(self, context):
        if "Plate Curve Generator" in context.object.modifiers:
            ProceduralPlate().randomize_plate(context)
            bpy.ops.ed.undo_push()
        else:
            self.report(
                {"ERROR"}, "Object does not contain Plate Curve Generator Modifier."
            )

        return {"FINISHED"}


class DRG_OT_randomize_plate_soil(bpy.types.Operator):
    """Randomize plate soil"""

    bl_idname = "drg.randomize_plate_soil"
    bl_label = "Randomize Plate Soil"

    def execute(self, context):
        if "Plate Crumbs" in context.object.modifiers:
            ProceduralPlate().randomize_crumbs(context)
            ProceduralPlate().randomize_soil_material(context)

            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Plate Crumbs Modifier.")

        return {"FINISHED"}


class DRG_OT_create_spoon(bpy.types.Operator):
    """Create a spoon object"""

    bl_idname = "drg.create_spoon"
    bl_label = "Create Spoon"

    def execute(self, context):

        ProceduralSpoon().create_spoon(context)

        return {"FINISHED"}


class DRG_OT_randomize_spoon(bpy.types.Operator):
    """Randomize a spoon object"""

    bl_idname = "drg.randomize_spoon"
    bl_label = "Randomize Spoon"

    def execute(self, context):
        if "Spoon Generator" in context.object.modifiers:
            ProceduralSpoon().randomize_spoon(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Spoon Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_create_fork(bpy.types.Operator):
    """Create a fork object"""

    bl_idname = "drg.create_fork"
    bl_label = "Create Fork"

    def execute(self, context):

        ProceduralFork().create_fork(context)

        return {"FINISHED"}


class DRG_OT_randomize_fork(bpy.types.Operator):
    """Randomize a fork object"""

    bl_idname = "drg.randomize_fork"
    bl_label = "Randomize Fork"

    def execute(self, context):
        if "Fork Generator" in context.object.modifiers:
            ProceduralFork().randomize_fork(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Fork Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_create_knife(bpy.types.Operator):
    """Create a knife object"""

    bl_idname = "drg.create_knife"
    bl_label = "Create Knife"

    def execute(self, context):

        ProceduralKnife().create_knife(context)

        return {"FINISHED"}


class DRG_OT_randomize_knife(bpy.types.Operator):
    """Randomize a knife object"""

    bl_idname = "drg.randomize_knife"
    bl_label = "Randomize Knife"

    def execute(self, context):
        if "Knife Generator" in context.object.modifiers:
            ProceduralKnife().randomize_knife(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Knife Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_create_glass(bpy.types.Operator):
    """Create a glass object"""

    bl_idname = "drg.create_glass"
    bl_label = "Create Glass"

    def execute(self, context):

        ProceduralGlass().create_glass(context)

        return {"FINISHED"}


class DRG_OT_randomize_glass(bpy.types.Operator):
    """Randomize a glass object"""

    bl_idname = "drg.randomize_glass"
    bl_label = "Randomize Glass"

    def execute(self, context):
        if "Glass Generator" in context.object.modifiers:
            ProceduralGlass().randomize_glass(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Glass Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_create_placemat(bpy.types.Operator):
    """Create a placemat object"""

    bl_idname = "drg.create_placemat"
    bl_label = "Create Placemat"

    def execute(self, context):

        ProceduralPlacemat().create_placemat(context)

        return {"FINISHED"}


class DRG_OT_randomize_placemat(bpy.types.Operator):
    """Randomize a placemat object"""

    bl_idname = "drg.randomize_placemat"
    bl_label = "Randomize Placemat"

    def execute(self, context):
        if "Placemat Generator" in context.object.modifiers:
            ProceduralPlacemat().randomize_placemat(context)
            bpy.ops.ed.undo_push()
        else:
            self.report(
                {"ERROR"}, "Object does not contain Placemat Generator Modifier."
            )

        return {"FINISHED"}


class DRG_OT_create_chair(bpy.types.Operator):
    """Create a chair object"""

    bl_idname = "drg.create_chair"
    bl_label = "Create Chair"

    def execute(self, context):

        ProceduralChair().create_chair(context)

        return {"FINISHED"}


class DRG_OT_randomize_chair(bpy.types.Operator):
    """Randomize a chair object"""

    bl_idname = "drg.randomize_chair"
    bl_label = "Randomize Chair"

    def execute(self, context):
        if "Chair Generator" in context.object.modifiers:
            ProceduralChair().randomize_chair(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Chair Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_randomize_chair_material(bpy.types.Operator):
    """Randomize chair material"""

    bl_idname = "drg.randomize_chair_material"
    bl_label = "Randomize Chair Material"

    def execute(self, context):
        if "Chair Generator" in context.object.modifiers:
            ProceduralChair().randomize_material(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Chair Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_create_table(bpy.types.Operator):
    """Create a table object"""

    bl_idname = "drg.create_table"
    bl_label = "Create Table"

    def execute(self, context):

        ProceduralTable().create_table(context)

        return {"FINISHED"}


class DRG_OT_randomize_table(bpy.types.Operator):
    """Randomize a table object"""

    bl_idname = "drg.randomize_table"
    bl_label = "Randomize Table"

    def execute(self, context):
        if "Table Generator" in context.object.modifiers:
            ProceduralTable().randomize_table(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Table Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_randomize_table_material(bpy.types.Operator):
    """Randomize table material"""

    bl_idname = "drg.randomize_table_material"
    bl_label = "Randomize Table Material"

    def execute(self, context):
        if "Table Generator" in context.object.modifiers:
            ProceduralTable().randomize_material(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Table Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_create_dining_room_distribution(bpy.types.Operator):
    """Create dining room distribution"""

    bl_idname = "drg.create_dining_room_distribution"
    bl_label = "Create Dining Room Distribution"

    def execute(self, context):
        if "Table Generator" in context.object.modifiers:
            DiningRoomDistributor().create_distribution(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Table Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_randomize_dining_room_distribution(bpy.types.Operator):
    """Randomize a dining room distribution"""

    bl_idname = "drg.randomize_dining_room_distribution"
    bl_label = "Randomize Dining Room Distribution"

    def execute(self, context):
        if "Dining Room Distributor" in context.object.modifiers:
            DiningRoomDistributor().randomize_distribution(context)
            bpy.ops.ed.undo_push()
        else:
            self.report(
                {"ERROR"}, "Object does not contain Dining Room Distribution Modifier."
            )

        return {"FINISHED"}


class DRG_OT_create_room(bpy.types.Operator):
    """Create a room object"""

    bl_idname = "drg.create_room"
    bl_label = "Create Room"

    def execute(self, context):
        ProceduralRoom().create_room(
            context,
        )
        return {"FINISHED"}


class DRG_OT_randomize_room(bpy.types.Operator):
    """Randomize a room object"""

    bl_idname = "drg.randomize_room"
    bl_label = "Randomize Room"

    def execute(self, context):
        ProceduralRoom().randomize_room(context)
        bpy.ops.ed.undo_push()
        return {"FINISHED"}


class DRG_OT_randomize_room_material(bpy.types.Operator):
    """Randomize room material"""

    bl_idname = "drg.randomize_room_material"
    bl_label = "Randomize Room Material"

    def execute(self, context):
        if "Room Generator" in context.object.modifiers:
            ProceduralRoom().randomize_material(context)
            bpy.ops.ed.undo_push()
        else:
            self.report({"ERROR"}, "Object does not contain Room Generator Modifier.")

        return {"FINISHED"}


class DRG_OT_randomize_indoor_lighting(bpy.types.Operator):
    """Randomize spotlight for indoor lighting"""

    bl_idname = "drg.randomize_indoor_lighting"
    bl_label = "Randomize Indoor Lighting"

    def execute(self, context):
        LightingRandomizer().randomize_indoor_lighting(context)

        if "Room Generator" in context.object.modifiers:
            ProceduralRoom().randomize_lighting(context)
        bpy.ops.ed.undo_push()

        return {"FINISHED"}


class DRG_OT_randomize_environment_lighting(bpy.types.Operator):
    """Randomize environment lighting"""

    bl_idname = "drg.randomize_environment_lighting"
    bl_label = "Randomize Environment Lighting"

    def execute(self, context):
        LightingRandomizer().randomize_environment_lighting(context)
        bpy.ops.ed.undo_push()

        return {"FINISHED"}


class DRG_OT_randomize_all_lighting(bpy.types.Operator):
    """Randomize all scene ligthing"""

    bl_idname = "drg.randomize_all_lighting"
    bl_label = "Randomize All Lighting"

    def execute(self, context):
        LightingRandomizer().randomize_environment_lighting(context)
        LightingRandomizer().randomize_indoor_lighting(context)

        if "Room Generator" in context.object.modifiers:
            ProceduralRoom().randomize_lighting(context)
        bpy.ops.ed.undo_push()

        return {"FINISHED"}


class DRG_OT_randomize_camera_position(bpy.types.Operator):
    """Ranomize camera position"""

    bl_idname = "drg.randomize_camera_postion"
    bl_label = "Randomize Camera Position"

    def execute(self, context):
        if "Room Generator" in context.object.modifiers:
            CameraRandomizer().randomize_camera_position(context)
        bpy.ops.ed.undo_push()

        return {"FINISHED"}


class DRG_OT_randomize_scene(bpy.types.Operator):
    """Randomize scene"""

    bl_idname = "drg.randomize_scene"
    bl_label = "Randomize Scene"

    def execute(self, context):
        data_logger = DataLogger()
        SceneRenderer().randomize_scene(context, data_logger)
        SceneRenderer().setup_scene(operator=self, index=0, data_logger=data_logger)
        bpy.ops.ed.undo_push()

        return {"FINISHED"}


class DRG_OT_render_scene(bpy.types.Operator):
    """Render randomized scene"""

    bl_idname = "drg.render_randomize_scene"
    bl_label = "Render Randomized Scene"

    def execute(self, context):
        SceneRenderer().render_start(
            self, context, context.scene.render_index, context.scene.amount_of_imgs
        )
        bpy.ops.ed.undo_push()
        return {"FINISHED"}


class DRG_OT_confirm_rendering(bpy.types.Operator):
    """Confirm rendering images"""

    bl_idname = "drg.confirm_rendering"
    bl_label = "Render all images?"
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        DRG_OT_render_scene.execute(self, context)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class DRG_OT_path_filebrowser(bpy.types.Operator, ImportHelper):
    """Open FileBrowser and set Rendering Path"""

    bl_idname = "drg.path_filebrowser"
    bl_label = "Set Export Path"

    directory: bpy.props.StringProperty()  # type: ignore

    filter_glob: bpy.props.StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer lenght, longer would be clamped
    )  # type: ignore

    def execute(self, context):
        context.scene.render_filepath = self.directory
        return {"FINISHED"}


class DRG_OT_test(bpy.types.Operator):
    bl_idname = "drg.test"
    bl_label = "Test"

    def execute(self, context):
        # DataLogger().create_or_append_csv()
        # test_obj = DiningRoomDistributor()
        # test_obj.randomize_distribution(context)
        # print(test_obj.amount_of_forks)
        # print(test_obj.amount_of_glasses)
        # print(test_obj.amount_of_knives)
        # print(test_obj.amount_of_plates)
        # print(test_obj.amount_of_spoons)
        self.report(
            {"WARNING"},
            f"{os.getcwd()}, {os.path.abspath}, {os.path.relpath}, {__file__}",
        )

        # area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        # space = next(space for space in area.spaces if space.type == 'VIEW_3D')
        # space.viewport_shade = 'RENDERED'

        # context.space_data.shading.type = "RENDERED"

        return {"FINISHED"}


############################ UI ############################


class DRG_PT_tableware_creator_sub_panel(bpy.types.Panel):
    """Dining Room Creator Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        self.layout.operator(DRG_OT_create_plate.bl_idname)
        self.layout.operator(DRG_OT_create_spoon.bl_idname)
        self.layout.operator(DRG_OT_create_fork.bl_idname)
        self.layout.operator(DRG_OT_create_knife.bl_idname)
        self.layout.operator(DRG_OT_create_glass.bl_idname)
        self.layout.operator(DRG_OT_create_placemat.bl_idname)
        self.layout.operator(DRG_OT_create_chair.bl_idname)
        self.layout.operator(DRG_OT_create_table.bl_idname)
        self.layout.operator(DRG_OT_create_room.bl_idname)


class DRG_PT_plate_characteristics_sub_panel(bpy.types.Panel):
    """Generating Plate Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):

        return (
            "Plate Curve Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        self.layout.separator()
        self.layout.operator(DRG_OT_randomize_plate.bl_idname)
        self.layout.operator(DRG_OT_randomize_plate_soil.bl_idname)
        self.layout.separator()

        pcg_modifier = context.object.modifiers["Plate Curve Generator"]
        pcg_node_group = pcg_modifier.node_group

        base_id = pcg_node_group.interface.items_tree["Base"].identifier
        diameter_id = pcg_node_group.interface.items_tree["Diameter"].identifier
        thickness_id = pcg_node_group.interface.items_tree["Thickness"].identifier
        base_radius_id = pcg_node_group.interface.items_tree["Base Radius"].identifier
        base_height_id = pcg_node_group.interface.items_tree["Base Height"].identifier
        base_width_id = pcg_node_group.interface.items_tree["Base Width"].identifier

        self.layout.label(text="Plate Characteristics")
        self.layout.prop(pcg_modifier, f'["{diameter_id}"]', text="Diameter")
        self.layout.prop(pcg_modifier, f'["{thickness_id}"]', text="Thickness")
        self.layout.prop(pcg_modifier, f'["{base_id}"]', text="Base")
        self.layout.prop(pcg_modifier, f'["{base_radius_id}"]', text="Base Radius")
        self.layout.prop(pcg_modifier, f'["{base_height_id}"]', text="Base Height")
        self.layout.prop(pcg_modifier, f'["{base_width_id}"]', text="Base Width")


class DRG_PT_plate_curvature_sub_panel(bpy.types.Panel):
    """Plate Curvature Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return (
            "Plate Curve Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        pcg_modifier = context.object.modifiers["Plate Curve Generator"]
        pcg_node_group = pcg_modifier.node_group

        self.layout.template_curve_mapping(
            pcg_node_group.nodes["Float Curve"],
            "mapping",
        )


class DRG_PT_spoon_characteristics_sub_panel(bpy.types.Panel):
    """Generating Spoon Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):

        return (
            "Spoon Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        self.layout.separator()
        self.layout.operator(DRG_OT_randomize_spoon.bl_idname)
        self.layout.separator()

        sg_modifier = context.object.modifiers["Spoon Generator"]
        sg_node_group = sg_modifier.node_group

        length_id = sg_node_group.interface.items_tree["Length"].identifier

        lod_id = sg_node_group.interface.items_tree["Level of Detail"].identifier

        bowl_length_id = sg_node_group.interface.items_tree["Bowl Length"].identifier
        bowl_width_id = sg_node_group.interface.items_tree["Bowl Width"].identifier
        bowl_depth_id = sg_node_group.interface.items_tree["Bowl Depth"].identifier

        neck_length_id = sg_node_group.interface.items_tree["Neck Length"].identifier
        neck_height_id = sg_node_group.interface.items_tree["Neck Height"].identifier

        handle_width_id = sg_node_group.interface.items_tree["Handle Width"].identifier
        handle_end_height_id = sg_node_group.interface.items_tree[
            "Handle End Height"
        ].identifier
        handle_end_width_id = sg_node_group.interface.items_tree[
            "Handle End Width"
        ].identifier
        handle_end_curvature_id = sg_node_group.interface.items_tree[
            "Handle End Curvature"
        ].identifier

        self.layout.label(text="Spoon Characteristics")
        self.layout.prop(sg_modifier, f'["{lod_id}"]', text="Level of Detail")
        self.layout.prop(sg_modifier, f'["{length_id}"]', text="Length")
        self.layout.prop(sg_modifier, f'["{bowl_length_id}"]', text="Bowl Length")
        self.layout.prop(sg_modifier, f'["{bowl_width_id}"]', text="Bowl Width")
        self.layout.prop(sg_modifier, f'["{bowl_depth_id}"]', text="Bowl Depth")
        self.layout.prop(sg_modifier, f'["{neck_length_id}"]', text="Neck Length")
        self.layout.prop(sg_modifier, f'["{neck_height_id}"]', text="Neck Height")
        self.layout.prop(sg_modifier, f'["{handle_width_id}"]', text="Handle Width")
        self.layout.prop(
            sg_modifier, f'["{handle_end_height_id}"]', text="Handle End Height"
        )
        self.layout.prop(
            sg_modifier, f'["{handle_end_width_id}"]', text="Handle End Width"
        )
        self.layout.prop(
            sg_modifier, f'["{handle_end_curvature_id}"]', text="Handle End Curvature"
        )


class DRG_PT_fork_characteristics_sub_panel(bpy.types.Panel):
    """Generating Fork Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):

        return (
            "Fork Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        self.layout.separator()
        self.layout.operator(DRG_OT_randomize_fork.bl_idname)
        self.layout.separator()

        fg_modifier = context.object.modifiers["Fork Generator"]
        fg_node_group = fg_modifier.node_group

        length_id = fg_node_group.interface.items_tree["Length"].identifier

        amount_of_prongs_id = fg_node_group.interface.items_tree[
            "Amount of Prongs"
        ].identifier

        prong_length_id = fg_node_group.interface.items_tree["Prong Length"].identifier
        prong_tip_curvature_id = fg_node_group.interface.items_tree[
            "Prong Tip Curvature"
        ].identifier

        eyes_curvature_id = fg_node_group.interface.items_tree[
            "Eyes Curvature"
        ].identifier

        bowl_length_id = fg_node_group.interface.items_tree["Bowl Length"].identifier
        bowl_width_id = fg_node_group.interface.items_tree["Bowl Width"].identifier
        bowl_curvature_id = fg_node_group.interface.items_tree[
            "Bowl Curvature"
        ].identifier

        neck_length_id = fg_node_group.interface.items_tree["Neck Length"].identifier
        neck_height_id = fg_node_group.interface.items_tree["Neck Height"].identifier

        handle_width_id = fg_node_group.interface.items_tree["Handle Width"].identifier
        handle_end_height_id = fg_node_group.interface.items_tree[
            "Handle End Height"
        ].identifier
        handle_end_width_id = fg_node_group.interface.items_tree[
            "Handle End Width"
        ].identifier
        handle_end_curvature_id = fg_node_group.interface.items_tree[
            "Handle End Curvature"
        ].identifier

        self.layout.label(text="Fork Characteristics")
        self.layout.prop(fg_modifier, f'["{length_id}"]', text="Length")
        self.layout.prop(
            fg_modifier, f'["{amount_of_prongs_id}"]', text="Amount of Prongs"
        )
        self.layout.prop(fg_modifier, f'["{prong_length_id}"]', text="Prong Length")
        self.layout.prop(
            fg_modifier, f'["{prong_tip_curvature_id}"]', text="Prong Tip Curvature"
        )
        self.layout.prop(fg_modifier, f'["{eyes_curvature_id}"]', text="Eyes Curvature")
        self.layout.prop(fg_modifier, f'["{bowl_length_id}"]', text="Bowl Length")
        self.layout.prop(fg_modifier, f'["{bowl_width_id}"]', text="Bowl Width")
        self.layout.prop(fg_modifier, f'["{bowl_curvature_id}"]', text="Bowl Curvature")
        self.layout.prop(fg_modifier, f'["{neck_length_id}"]', text="Neck Length")
        self.layout.prop(fg_modifier, f'["{neck_height_id}"]', text="Neck Height")
        self.layout.prop(fg_modifier, f'["{handle_width_id}"]', text="Handle Width")
        self.layout.prop(
            fg_modifier, f'["{handle_end_height_id}"]', text="Handle End Height"
        )
        self.layout.prop(
            fg_modifier, f'["{handle_end_width_id}"]', text="Handle End Width"
        )
        self.layout.prop(
            fg_modifier, f'["{handle_end_curvature_id}"]', text="Handle End Curvature"
        )


class DRG_PT_knife_characteristics_sub_panel(bpy.types.Panel):
    """Generating Knife Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):

        return (
            "Knife Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        self.layout.separator()
        self.layout.operator(DRG_OT_randomize_knife.bl_idname)
        self.layout.separator()

        kg_modifier = context.object.modifiers["Knife Generator"]
        kg_node_group = kg_modifier.node_group

        length_id = kg_node_group.interface.items_tree["Length"].identifier
        width_id = kg_node_group.interface.items_tree["Width"].identifier
        thickness_id = kg_node_group.interface.items_tree["Thickness"].identifier

        blade_length_id = kg_node_group.interface.items_tree["Blade Length"].identifier
        blade_thickness_id = kg_node_group.interface.items_tree[
            "Blade Thickness"
        ].identifier

        blade_tip_curvature_id = kg_node_group.interface.items_tree[
            "Blade Tip Curvature"
        ].identifier
        blade_tip_intensity_id = kg_node_group.interface.items_tree[
            "Blade Tip Intensity"
        ].identifier

        blade_base_curvature_id = kg_node_group.interface.items_tree[
            "Blade Base Curvature"
        ].identifier
        blade_base_intensity_id = kg_node_group.interface.items_tree[
            "Blade Base Intensity"
        ].identifier

        handle_width_id = kg_node_group.interface.items_tree["Handle Width"].identifier
        handle_end_width_id = kg_node_group.interface.items_tree[
            "Handle End Width"
        ].identifier
        handle_end_curvature_id = kg_node_group.interface.items_tree[
            "Handle End Curvature"
        ].identifier

        self.layout.label(text="Knife Characteristics")
        self.layout.prop(kg_modifier, f'["{length_id}"]', text="Length")
        self.layout.prop(kg_modifier, f'["{width_id}"]', text="Width")
        self.layout.prop(kg_modifier, f'["{thickness_id}"]', text="Thickness")
        self.layout.prop(kg_modifier, f'["{blade_length_id}"]', text="Blade Length")
        self.layout.prop(
            kg_modifier, f'["{blade_thickness_id}"]', text="Blade Thickness"
        )
        self.layout.prop(
            kg_modifier, f'["{blade_tip_curvature_id}"]', text="Blade Tip Curvature"
        )
        self.layout.prop(
            kg_modifier, f'["{blade_tip_intensity_id}"]', text="Blade Tip Intensity"
        )
        self.layout.prop(
            kg_modifier, f'["{blade_base_curvature_id}"]', text="Blade Base Curvature"
        )
        self.layout.prop(
            kg_modifier, f'["{blade_base_intensity_id}"]', text="Blade Base Intensity"
        )
        self.layout.prop(kg_modifier, f'["{handle_width_id}"]', text="Handle Width")
        self.layout.prop(
            kg_modifier, f'["{handle_end_width_id}"]', text="Handle End Width"
        )
        self.layout.prop(
            kg_modifier, f'["{handle_end_curvature_id}"]', text="Handle End Curvature"
        )


class DRG_PT_glass_characteristics_sub_panel(bpy.types.Panel):
    """Generating Glass Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return (
            "Glass Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        self.layout.separator()
        self.layout.operator(DRG_OT_randomize_glass.bl_idname)
        self.layout.separator()

        gg_modifier = context.object.modifiers["Glass Generator"]
        gg_node_group = gg_modifier.node_group

        lod_id = gg_node_group.interface.items_tree["Level of Detail"].identifier

        height_id = gg_node_group.interface.items_tree["Height"].identifier
        thickness_id = gg_node_group.interface.items_tree["Thickness"].identifier

        base_diameter_id = gg_node_group.interface.items_tree[
            "Base Diameter"
        ].identifier
        base_curvature_id = gg_node_group.interface.items_tree[
            "Base Curvature"
        ].identifier
        base_thickness_id = gg_node_group.interface.items_tree[
            "Base Thickness"
        ].identifier

        mid_curvature_height_id = gg_node_group.interface.items_tree[
            "Mid Curvature Height"
        ].identifier
        mid_curvature_diameter_id = gg_node_group.interface.items_tree[
            "Mid Curvature Diameter"
        ].identifier

        rim_diameter_id = gg_node_group.interface.items_tree["Rim Diameter"].identifier
        rim_curvature_id = gg_node_group.interface.items_tree[
            "Rim Curvature"
        ].identifier

        bowl_curvature_id = gg_node_group.interface.items_tree[
            "Bowl Curvature"
        ].identifier

        self.layout.label(text="Glass Characteristics")
        self.layout.prop(gg_modifier, f'["{lod_id}"]', text="Level of Detail")
        self.layout.prop(gg_modifier, f'["{height_id}"]', text="Height")
        self.layout.prop(gg_modifier, f'["{thickness_id}"]', text="Thickness")
        self.layout.prop(gg_modifier, f'["{base_diameter_id}"]', text="Base Diameter")
        self.layout.prop(gg_modifier, f'["{base_curvature_id}"]', text="Base Curvature")
        self.layout.prop(gg_modifier, f'["{base_thickness_id}"]', text="Base Thickness")
        self.layout.prop(
            gg_modifier, f'["{mid_curvature_height_id}"]', text="Mid Curvature Height"
        )
        self.layout.prop(
            gg_modifier,
            f'["{mid_curvature_diameter_id}"]',
            text="Mid Curvature Diameter",
        )
        self.layout.prop(gg_modifier, f'["{rim_diameter_id}"]', text="Rim Diameter")
        self.layout.prop(gg_modifier, f'["{rim_curvature_id}"]', text="Rim Curvature")
        self.layout.prop(gg_modifier, f'["{bowl_curvature_id}"]', text="Bowl Curvature")


class DRG_PT_placemat_characteristics_sub_panel(bpy.types.Panel):
    """Generating Placemat Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return (
            "Placemat Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        self.layout.separator()
        self.layout.operator(DRG_OT_randomize_placemat.bl_idname)
        self.layout.separator()

        pmg_modifier = context.object.modifiers["Placemat Generator"]
        pmg_node_group = pmg_modifier.node_group

        round_tablecloth_id = pmg_node_group.interface.items_tree[
            "Round Tablecloth"
        ].identifier

        height_id = pmg_node_group.interface.items_tree["Height"].identifier
        width_id = pmg_node_group.interface.items_tree["Width"].identifier
        depth_id = pmg_node_group.interface.items_tree["Depth"].identifier

        square_placemat_curvature = pmg_node_group.interface.items_tree[
            "Square Placemat Curvature"
        ].identifier

        self.layout.label(text="Placemat Characteristics")
        self.layout.prop(
            pmg_modifier, f'["{round_tablecloth_id}"]', text="Round Tablecloth"
        )
        self.layout.prop(pmg_modifier, f'["{height_id}"]', text="Height")
        self.layout.prop(pmg_modifier, f'["{width_id}"]', text="Width")
        self.layout.prop(pmg_modifier, f'["{depth_id}"]', text="Depth")
        self.layout.prop(
            pmg_modifier,
            f'["{square_placemat_curvature}"]',
            text="Square Placemat Curvature",
        )


class DRG_PT_chair_characteristics_sub_panel(bpy.types.Panel):
    """Generating Chair Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return (
            "Chair Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        self.layout.separator()
        self.layout.operator(DRG_OT_randomize_chair.bl_idname)
        self.layout.operator(DRG_OT_randomize_chair_material.bl_idname)
        self.layout.separator()

        cg_modifier = context.object.modifiers["Chair Generator"]
        cg_node_group = cg_modifier.node_group

        curved_backrest_id = cg_node_group.interface.items_tree[
            "Curved Backrest"
        ].identifier
        round_seat_id = cg_node_group.interface.items_tree["Round Seat"].identifier
        round_rail_id = cg_node_group.interface.items_tree["Round Rail"].identifier

        height_id = cg_node_group.interface.items_tree["Height"].identifier
        width_id = cg_node_group.interface.items_tree["Width"].identifier
        depth_id = cg_node_group.interface.items_tree["Depth"].identifier

        backrest_angle_id = cg_node_group.interface.items_tree[
            "Backrest Angle"
        ].identifier

        top_rail_height_id = cg_node_group.interface.items_tree[
            "Top Rail Height"
        ].identifier
        top_rail_thickness_id = cg_node_group.interface.items_tree[
            "Top Rail Thickness"
        ].identifier

        backpost_width_id = cg_node_group.interface.items_tree[
            "Backpost Width"
        ].identifier
        backpost_thickness_id = cg_node_group.interface.items_tree[
            "Backpost Thickness"
        ].identifier

        amount_of_crossrails_id = cg_node_group.interface.items_tree[
            "Amount of Crossrails"
        ].identifier
        crossrail_height_id = cg_node_group.interface.items_tree[
            "Crossrail Height"
        ].identifier
        crossrail_thickness_id = cg_node_group.interface.items_tree[
            "Crossrail Thickness"
        ].identifier

        amount_of_slats_id = cg_node_group.interface.items_tree[
            "Amount of Slats"
        ].identifier
        slat_width_id = cg_node_group.interface.items_tree["Slat Width"].identifier
        slat_thickness_id = cg_node_group.interface.items_tree[
            "Slat Thickness"
        ].identifier

        seat_height_id = cg_node_group.interface.items_tree["Seat Height"].identifier
        seat_thickness_id = cg_node_group.interface.items_tree[
            "Seat Thickness"
        ].identifier
        seat_curvature_id = cg_node_group.interface.items_tree[
            "Seat Curvature"
        ].identifier

        seat_rail_reduction_id = cg_node_group.interface.items_tree[
            "Seat Rail Reduction"
        ].identifier
        seat_rail_thickness_id = cg_node_group.interface.items_tree[
            "Seat Rail Thickness"
        ].identifier

        leg_width_id = cg_node_group.interface.items_tree["Leg Width"].identifier
        leg_thickness_id = cg_node_group.interface.items_tree[
            "Leg Thickness"
        ].identifier
        leg_angle_id = cg_node_group.interface.items_tree["Leg Angle"].identifier

        self.layout.label(text="Chair Characteristics")
        self.layout.prop(
            cg_modifier, f'["{curved_backrest_id}"]', text="Curved Backrest"
        )
        self.layout.prop(cg_modifier, f'["{round_seat_id}"]', text="Round Seat")
        self.layout.prop(cg_modifier, f'["{round_rail_id}"]', text="Round Rail")
        self.layout.prop(cg_modifier, f'["{height_id}"]', text="Height")
        self.layout.prop(cg_modifier, f'["{width_id}"]', text="Width")
        self.layout.prop(cg_modifier, f'["{depth_id}"]', text="Depth")
        self.layout.prop(cg_modifier, f'["{backrest_angle_id}"]', text="Backrest Angle")
        self.layout.prop(
            cg_modifier, f'["{top_rail_height_id}"]', text="Top Rail Height"
        )
        self.layout.prop(
            cg_modifier, f'["{top_rail_thickness_id}"]', text="Top Rail Thickness"
        )
        self.layout.prop(cg_modifier, f'["{backpost_width_id}"]', text="Backpost Width")
        self.layout.prop(
            cg_modifier, f'["{backpost_thickness_id}"]', text="Backpost Thickness"
        )
        self.layout.prop(
            cg_modifier, f'["{amount_of_crossrails_id}"]', text="Amount of Crossrails"
        )
        self.layout.prop(
            cg_modifier, f'["{crossrail_height_id}"]', text="Crossrail Height"
        )
        self.layout.prop(
            cg_modifier, f'["{crossrail_thickness_id}"]', text="Crossrail Thickness"
        )
        self.layout.prop(
            cg_modifier, f'["{amount_of_slats_id}"]', text="Amount of Slats"
        )
        self.layout.prop(cg_modifier, f'["{slat_width_id}"]', text="Slat Width")
        self.layout.prop(cg_modifier, f'["{slat_thickness_id}"]', text="Slat Thickness")
        self.layout.prop(cg_modifier, f'["{seat_height_id}"]', text="Seat Height")
        self.layout.prop(cg_modifier, f'["{seat_thickness_id}"]', text="Seat Thickness")
        self.layout.prop(cg_modifier, f'["{seat_curvature_id}"]', text="Seat Curvature")
        self.layout.prop(
            cg_modifier, f'["{seat_rail_reduction_id}"]', text="Seat Rail Reduction"
        )
        self.layout.prop(
            cg_modifier, f'["{seat_rail_thickness_id}"]', text="Seat Rail Thickness"
        )
        self.layout.prop(cg_modifier, f'["{leg_width_id}"]', text="Leg Width")
        self.layout.prop(cg_modifier, f'["{leg_thickness_id}"]', text="Leg Thickness")
        self.layout.prop(cg_modifier, f'["{leg_angle_id}"]', text="Leg Angle")


class DRG_PT_table_characteristics_sub_panel(bpy.types.Panel):
    """Generating Table Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return (
            "Table Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        self.layout.separator()
        self.layout.operator(DRG_OT_randomize_table.bl_idname)
        self.layout.operator(DRG_OT_randomize_table_material.bl_idname)
        self.layout.separator()

        tg_modifier = context.object.modifiers["Table Generator"]
        tg_node_group = tg_modifier.node_group

        round_table_id = tg_node_group.interface.items_tree["Round Table"].identifier
        round_apron_id = tg_node_group.interface.items_tree["Round Apron"].identifier

        height_id = tg_node_group.interface.items_tree["Height"].identifier
        width_id = tg_node_group.interface.items_tree["Width"].identifier
        depth_id = tg_node_group.interface.items_tree["Depth"].identifier

        top_thickness_id = tg_node_group.interface.items_tree[
            "Top Thickness"
        ].identifier
        top_curvature_id = tg_node_group.interface.items_tree[
            "Top Curvature"
        ].identifier

        apron_size_reduction_id = tg_node_group.interface.items_tree[
            "Apron Size Reduction"
        ].identifier
        apron_thickness_id = tg_node_group.interface.items_tree[
            "Apron Thickness"
        ].identifier

        leg_width_id = tg_node_group.interface.items_tree["Leg Width"].identifier
        leg_thickness_id = tg_node_group.interface.items_tree[
            "Leg Thickness"
        ].identifier
        leg_angle_id = tg_node_group.interface.items_tree["Leg Angle"].identifier

        self.layout.label(text="Table Characteristics")
        self.layout.prop(tg_modifier, f'["{round_table_id}"]', text="Round Table")
        self.layout.prop(tg_modifier, f'["{round_apron_id}"]', text="Round Apron")
        self.layout.prop(tg_modifier, f'["{height_id}"]', text="Height")
        self.layout.prop(tg_modifier, f'["{width_id}"]', text="Width")
        self.layout.prop(tg_modifier, f'["{depth_id}"]', text="Depth")
        self.layout.prop(tg_modifier, f'["{top_thickness_id}"]', text="Top Thickness")
        self.layout.prop(tg_modifier, f'["{top_curvature_id}"]', text="Top Curvature")
        self.layout.prop(
            tg_modifier, f'["{apron_size_reduction_id}"]', text="Apron Size Reduction"
        )
        self.layout.prop(
            tg_modifier, f'["{apron_thickness_id}"]', text="Apron Thickness"
        )
        self.layout.prop(tg_modifier, f'["{leg_width_id}"]', text="Leg Width")
        self.layout.prop(tg_modifier, f'["{leg_thickness_id}"]', text="Leg Thickness")
        self.layout.prop(tg_modifier, f'["{leg_angle_id}"]', text="Leg Angle")


class DRG_PT_room_characteristics_sub_panel(bpy.types.Panel):
    """Generating Room Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return (
            "Room Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        self.layout.separator()
        self.layout.operator(DRG_OT_randomize_room.bl_idname)
        self.layout.operator(DRG_OT_randomize_room_material.bl_idname)
        self.layout.separator()

        rg_modifier = context.object.modifiers["Room Generator"]
        rg_node_group = rg_modifier.node_group

        wall_height_id = rg_node_group.interface.items_tree["Wall Height"].identifier
        wall_thickness_id = rg_node_group.interface.items_tree[
            "Wall Thickness"
        ].identifier

        baseboard_height_id = rg_node_group.interface.items_tree[
            "Baseboard Height"
        ].identifier
        baseboard_width_id = rg_node_group.interface.items_tree[
            "Baseboard Width"
        ].identifier
        table_location_random_seed_id = rg_node_group.interface.items_tree[
            "Table Location Random Seed"
        ].identifier

        amount_of_windows_id = rg_node_group.interface.items_tree[
            "Amount of Windows"
        ].identifier
        window_height_id = rg_node_group.interface.items_tree[
            "Window Height"
        ].identifier
        window_width_id = rg_node_group.interface.items_tree["Window Width"].identifier
        window_frame_thickness_id = rg_node_group.interface.items_tree[
            "Window Frame Thickness"
        ].identifier
        window_frame_depth_id = rg_node_group.interface.items_tree[
            "Window Frame Depth"
        ].identifier
        window_thickness_id = rg_node_group.interface.items_tree[
            "Window Thickness"
        ].identifier
        window_depth_id = rg_node_group.interface.items_tree["Window Depth"].identifier
        glass_thickness_id = rg_node_group.interface.items_tree[
            "Glass Thickness"
        ].identifier
        window_height_pos_id = rg_node_group.interface.items_tree[
            "Window Height Position"
        ].identifier
        window_distribution_random_seed = rg_node_group.interface.items_tree[
            "Window Distribution Random Seed"
        ].identifier

        indoor_lighting_id = rg_node_group.interface.items_tree[
            "Indoor Lighting"
        ].identifier
        amount_of_lights_id = rg_node_group.interface.items_tree[
            "Amount of Lights"
        ].identifier
        light_distribution_random_seed_id = rg_node_group.interface.items_tree[
            "Window Height Position"
        ].identifier

        table_distributor_object_id = rg_node_group.interface.items_tree[
            "Table Distributor Object"
        ].identifier

        camera_object_id = rg_node_group.interface.items_tree[
            "Camera Object"
        ].identifier

        self.layout.label(text="Room Characteristics")
        self.layout.prop(rg_modifier, f'["{wall_height_id}"]', text="Wall Height")
        self.layout.prop(rg_modifier, f'["{wall_thickness_id}"]', text="Wall Thickness")
        self.layout.prop(
            rg_modifier, f'["{baseboard_height_id}"]', text="Baseboard Height"
        )
        self.layout.prop(
            rg_modifier, f'["{baseboard_width_id}"]', text="Baseboard Width"
        )
        self.layout.prop(
            rg_modifier,
            f'["{table_location_random_seed_id}"]',
            text="Table Location Random Seed",
        )
        self.layout.separator()

        self.layout.prop(
            rg_modifier, f'["{amount_of_windows_id}"]', text="Amount of Windows"
        )
        self.layout.prop(rg_modifier, f'["{window_height_id}"]', text="Window Height")
        self.layout.prop(rg_modifier, f'["{window_width_id}"]', text="Window Width")
        self.layout.prop(
            rg_modifier,
            f'["{window_frame_thickness_id}"]',
            text="Window Frame Thickness",
        )
        self.layout.prop(
            rg_modifier, f'["{window_frame_depth_id}"]', text="Window Frame Depth"
        )
        self.layout.prop(
            rg_modifier, f'["{window_thickness_id}"]', text="Window Thickness"
        )
        self.layout.prop(rg_modifier, f'["{window_depth_id}"]', text="Window Depth")
        self.layout.prop(
            rg_modifier, f'["{glass_thickness_id}"]', text="Glass Thickness"
        )
        self.layout.prop(
            rg_modifier, f'["{window_height_pos_id}"]', text="Window Height Position"
        )
        self.layout.prop(
            rg_modifier,
            f'["{window_distribution_random_seed}"]',
            text="Window Distribution Random Seed",
        )

        self.layout.separator()

        self.layout.prop(
            rg_modifier, f'["{indoor_lighting_id}"]', text="Indoor Lighting"
        )
        self.layout.prop(
            rg_modifier, f'["{amount_of_lights_id}"]', text="Amount of Lights"
        )
        self.layout.prop(
            rg_modifier,
            f'["{light_distribution_random_seed_id}"]',
            text="Light Distribution Random Seed",
        )

        self.layout.separator()
        self.layout.prop(
            rg_modifier,
            f'["{table_distributor_object_id}"]',
            text="Table Distributor Object",
        )
        self.layout.prop(rg_modifier, f'["{camera_object_id}"]', text="Camera Object")


class DRG_PT_dining_room_distribution_sub_panel(bpy.types.Panel):
    """Dining Room Distribution Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return (
            "Table Generator" in context.object.modifiers
            if context.object is not None
            else False
        )

    def draw(self, context):
        if (
            "Table Generator" in context.object.modifiers
            and "Dining Room Distributor" not in context.object.modifiers
        ):
            self.layout.separator()
            self.layout.operator(DRG_OT_create_dining_room_distribution.bl_idname)
            self.layout.separator()
        elif (
            "Table Generator" in context.object.modifiers
            and "Dining Room Distributor" in context.object.modifiers
        ):
            self.layout.separator()
            self.layout.operator(DRG_OT_randomize_dining_room_distribution.bl_idname)
            self.layout.separator()

            drd_modifier = context.object.modifiers["Dining Room Distributor"]
            drd_node_group = drd_modifier.node_group

            distribution_random_seed_id = drd_node_group.interface.items_tree[
                "Distribution Random Seed"
            ].identifier
            tableware_rotation_random_seed_id = drd_node_group.interface.items_tree[
                "Tableware Rotation Random Seed"
            ].identifier
            chair_location_random_seed_id = drd_node_group.interface.items_tree[
                "Chair Location Random Seed"
            ].identifier
            chair_rotation_random_seed_id = drd_node_group.interface.items_tree[
                "Chair Rotation Random Seed"
            ].identifier

            self.layout.label(text="Dining Room Distribution")
            self.layout.prop(
                drd_modifier,
                f'["{distribution_random_seed_id}"]',
                text="Distribution Random Seed",
            )
            self.layout.prop(
                drd_modifier,
                f'["{tableware_rotation_random_seed_id}"]',
                text="Tableware Rotation Random Seed",
            )
            self.layout.prop(
                drd_modifier,
                f'["{chair_location_random_seed_id}"]',
                text="Chair Location Random Seed",
            )
            self.layout.prop(
                drd_modifier,
                f'["{chair_rotation_random_seed_id}"]',
                text="Chair Rotation Random Seed",
            )


class DRG_PT_lighting_randomizer_sub_panel(bpy.types.Panel):
    """Lighting Randomizer Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        self.layout.operator(DRG_OT_randomize_indoor_lighting.bl_idname)
        self.layout.operator(DRG_OT_randomize_environment_lighting.bl_idname)
        self.layout.operator(DRG_OT_randomize_all_lighting.bl_idname)


class DRG_PT_camera_randomizer_sub_panel(bpy.types.Panel):
    """Camera Randomizer Sub Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):

        if context.object and "Room Generator" in context.object.modifiers:
            self.layout.operator(DRG_OT_randomize_camera_position.bl_idname)
        else:
            self.layout.label(text="Select Room Object for randomize Camera Position")


class DRG_PT_dirt_generator_sub_panel(bpy.types.Panel):
    """Dirt Generator Panel for the dining room generator addon"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        self.layout.label(text="Dirt Generator", icon="CURRENT_FILE")
        self.layout.label(text="Dirt Generator2", icon="CURRENT_FILE")


class DRG_viewport_panel:
    """Abstract class for the main panel in the View3D UI, displays the tab in the viewport"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Dining Room Generator"


class DRG_PT_viewport_panel(DRG_viewport_panel, bpy.types.Panel):
    """Main Panel for the dining room generator addon in the VIEW3D UI"""

    bl_idname = "DRG_PT_viewport_panel"
    bl_label = "Dining Room Generator"

    def draw(self, context):
        self.layout.operator(DRG_OT_randomize_scene.bl_idname)
        self.layout.operator(DRG_OT_path_filebrowser.bl_idname)
        self.layout.separator()
        self.layout.label(
            text=f"Export Folder: {context.scene.render_filepath}", icon="FILE_FOLDER"
        )
        self.layout.prop(context.scene, "render_index", text="Start Image Index")
        self.layout.prop(context.scene, "amount_of_imgs", text="Amount of Images")
        self.layout.prop(context.scene, "datalogger_name", text="Datalogger File Name")
        self.layout.separator()
        # self.layout.operator(DRG_OT_render_scene.bl_idname, text="Render")
        self.layout.operator(DRG_OT_confirm_rendering.bl_idname, text="Render Images")
        # self.layout.operator(DRG_OT_test.bl_idname)


class DRG_PT_viewport_tableware_creator_sub_panel(DRG_PT_tableware_creator_sub_panel):
    """Dining Room Creator Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_tableware_creator_sub_panel"
    bl_label = "Dining Room Creator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_plate_characteristics_sub_panel(
    DRG_PT_plate_characteristics_sub_panel
):
    """Plate Characteristics Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_plate_characteristics_sub_panel"
    bl_label = "Plate Characteristics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_plate_curvature_sub_panel(DRG_PT_plate_curvature_sub_panel):
    """Plate Curvature Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_plate_curvature_sub_panel"
    bl_label = "Plate Curvature"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_spoon_characteristics_sub_panel(
    DRG_PT_spoon_characteristics_sub_panel
):
    """Spoon Characteristics Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_spoon_characteristics_sub_panel"
    bl_label = "Spoon Characteristics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_fork_characteristics_sub_panel(
    DRG_PT_fork_characteristics_sub_panel
):
    """Fork Characteristics Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_fork_characteristics_sub_panel"
    bl_label = "Fork Characteristics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_knife_characteristics_sub_panel(
    DRG_PT_knife_characteristics_sub_panel
):
    """Knife Characteristics Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_knife_characteristics_sub_panel"
    bl_label = "Knife Characteristics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_glass_characteristics_sub_panel(
    DRG_PT_glass_characteristics_sub_panel
):
    """Glass Characteristics Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_glass_characteristics_sub_panel"
    bl_label = "Glass Characteristics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_placemat_characteristics_sub_panel(
    DRG_PT_placemat_characteristics_sub_panel
):
    """Placemat Characteristics Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_placemat_characteristics_sub_panel"
    bl_label = "Placemat Characteristics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_chair_characteristics_sub_panel(
    DRG_PT_chair_characteristics_sub_panel
):
    """Chair Characteristics Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_chair_characteristics_sub_panel"
    bl_label = "Chair Characteristics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_room_characteristics_sub_panel(
    DRG_PT_room_characteristics_sub_panel
):
    """Room Characteristics Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_room_characteristics_sub_panel"
    bl_label = "Room Characteristics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_table_characteristics_sub_panel(
    DRG_PT_table_characteristics_sub_panel
):
    """Table Characteristics Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_table_characteristics_sub_panel"
    bl_label = "Table Characteristics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_dining_room_distribution_sub_panel(
    DRG_PT_dining_room_distribution_sub_panel
):
    """Dining Room Distribution Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_dining_room_distribution_sub_panel"
    bl_label = "Dining Room Distribution"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_lighting_randomizer_sub_panel(
    DRG_PT_lighting_randomizer_sub_panel
):
    """Lighting Randomizer Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_lighting_randomizer_sub_panel"
    bl_label = "Lighting Randomizer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_camera_randomizer_sub_panel(DRG_PT_camera_randomizer_sub_panel):
    """Camera Randomizer Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_camera_randomizer_sub_panel"
    bl_label = "Camera Randomizer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class DRG_PT_viewport_dirt_generator_sub_panel(DRG_PT_dirt_generator_sub_panel):
    """Dirt Generator Sub Panel for the dining room generator addon in the View3D UI"""

    bl_parent_id = DRG_PT_viewport_panel.bl_idname
    bl_idname = "DRG_PT_viewport_dirt_generator_sub_panel"
    bl_label = "Dirt Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


##### OBJECT PROPERTIES PANEL ############################################################


class DRG_object_properties_panel:
    """Abstract class for the main panel in the object properties UI"""

    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "Dining Room Generator"
    bl_context = "object"


class DRG_PT_object_panel(DRG_object_properties_panel, bpy.types.Panel):
    """Main Panel for the dining room generator addon in the object properties"""

    bl_idname = "DRG_PT_object_panel"
    bl_label = "Dining Room Generator"

    def draw(self, context):
        self.layout.operator(DRG_OT_randomize_scene.bl_idname)
        self.layout.operator(DRG_OT_render_scene.bl_idname)


class DRG_PT_object_tableware_creator_sub_panel(DRG_PT_tableware_creator_sub_panel):
    """Tableware Creator Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_tableware_creator_sub_panel"
    bl_label = "Dining Room Creator"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_plate_characteristics_sub_panel(
    DRG_PT_plate_characteristics_sub_panel
):
    """Plate Characteristics Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_plate_characteristics_sub_panel"
    bl_label = "Plate Characteristics"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_plate_curvature_sub_panel(DRG_PT_plate_curvature_sub_panel):
    """Plate Curvature Sub Panel for the dining room generator addon in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_plate_curvature_sub_panel"
    bl_label = "Plate Curvature"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_spoon_characteristics_sub_panel(
    DRG_PT_spoon_characteristics_sub_panel
):
    """Spoon Characteristics Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_spoon_characteristics_sub_panel"
    bl_label = "Spoon Characteristics"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_fork_characteristics_sub_panel(
    DRG_PT_fork_characteristics_sub_panel
):
    """Fork Characteristics Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_fork_characteristics_sub_panel"
    bl_label = "Fork Characteristics"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_knife_characteristics_sub_panel(
    DRG_PT_knife_characteristics_sub_panel
):
    """Knife Characteristics Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_knife_characteristics_sub_panel"
    bl_label = "Knife Characteristics"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_glass_characteristics_sub_panel(
    DRG_PT_glass_characteristics_sub_panel
):
    """Glass Characteristics Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_glass_characteristics_sub_panel"
    bl_label = "Glass Characteristics"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_placemat_characteristics_sub_panel(
    DRG_PT_placemat_characteristics_sub_panel
):
    """Placemat Characteristics Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_placemat_characteristics_sub_panel"
    bl_label = "Placemat Characteristics"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_chair_characteristics_sub_panel(
    DRG_PT_chair_characteristics_sub_panel
):
    """Chair Characteristics Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_chair_characteristics_sub_panel"
    bl_label = "Chair Characteristics"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_room_characteristics_sub_panel(
    DRG_PT_room_characteristics_sub_panel
):
    """Room Characteristics Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_room_characteristics_sub_panel"
    bl_label = "Room Characteristics"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_table_characteristics_sub_panel(
    DRG_PT_table_characteristics_sub_panel
):
    """Table Characteristics Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_table_characteristics_sub_panel"
    bl_label = "Table Characteristics"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_dining_room_distribution_sub_panel(
    DRG_PT_dining_room_distribution_sub_panel
):
    """Dining Room Distribution Sub Panel for the dining room generator in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_dining_room_distribution_sub_panel"
    bl_label = "Dining Room Distribution"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_lighting_randomizer_sub_panel(DRG_PT_lighting_randomizer_sub_panel):
    """Lighting Randomizer Sub Panel for the dining room generator addon in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_lighting_randomizer_sub_panel"
    bl_label = "Lighting Randomizer"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_camera_randomizer_sub_panel(DRG_PT_camera_randomizer_sub_panel):
    """Camera Randomizer Sub Panel for the dining room generator addon in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_camera_randomizer_sub_panel"
    bl_label = "Camera Randomizer"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"


class DRG_PT_object_dirt_generator_sub_panel(DRG_PT_dirt_generator_sub_panel):
    """Dirt Generator Sub Panel for the dining room generator addon in the object properties"""

    bl_parent_id = DRG_PT_object_panel.bl_idname
    bl_idname = "DRG_PT_object_dirt_generator_sub_panel"
    bl_label = "Dirt Generator"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
