from .drg_addon import *
import bpy

bl_info = {
    "name": "Dining Room Generator",
    "author": "Philipp Mach",
    "version": (0, 0, 1),
    "blender": (4, 2, 1),
    # "location": "Properties > Object Properties > Dining Room Generator",
    "description": "Dining Room Generator Plugin",
    "category": "Mesh",
    "wiki_url": "tbd",
}


##### REGISTERING CLASSES ############################################################

classes = [
    # PROPERTIES
    # OPERATORS
    DRG_OT_create_plate,
    DRG_OT_randomize_plate,
    DRG_OT_randomize_plate_soil,
    DRG_OT_create_spoon,
    DRG_OT_randomize_spoon,
    DRG_OT_create_fork,
    DRG_OT_randomize_fork,
    DRG_OT_create_knife,
    DRG_OT_randomize_knife,
    DRG_OT_create_glass,
    DRG_OT_randomize_glass,
    DRG_OT_create_placemat,
    DRG_OT_randomize_placemat,
    DRG_OT_create_chair,
    DRG_OT_randomize_chair,
    DRG_OT_randomize_chair_material,
    DRG_OT_create_table,
    DRG_OT_randomize_table,
    DRG_OT_randomize_table_material,
    DRG_OT_create_dining_room_distribution,
    DRG_OT_randomize_dining_room_distribution,
    DRG_OT_create_room,
    DRG_OT_randomize_room,
    DRG_OT_randomize_room_material,
    DRG_OT_randomize_indoor_lighting,
    DRG_OT_randomize_environment_lighting,
    DRG_OT_randomize_all_lighting,
    DRG_OT_randomize_camera_position,
    DRG_OT_randomize_scene,
    # DRG_OT_render_scene,
    DRG_OT_confirm_rendering,
    DRG_OT_path_filebrowser,
    # DRG_OT_test,
    # UI
    DRG_PT_viewport_panel,
    DRG_PT_viewport_tableware_creator_sub_panel,
    DRG_PT_viewport_plate_characteristics_sub_panel,
    DRG_PT_viewport_plate_curvature_sub_panel,
    DRG_PT_viewport_spoon_characteristics_sub_panel,
    DRG_PT_viewport_fork_characteristics_sub_panel,
    DRG_PT_viewport_knife_characteristics_sub_panel,
    DRG_PT_viewport_glass_characteristics_sub_panel,
    DRG_PT_viewport_placemat_characteristics_sub_panel,
    DRG_PT_viewport_chair_characteristics_sub_panel,
    DRG_PT_viewport_room_characteristics_sub_panel,
    DRG_PT_viewport_table_characteristics_sub_panel,
    DRG_PT_viewport_dining_room_distribution_sub_panel,
    DRG_PT_viewport_lighting_randomizer_sub_panel,
    DRG_PT_viewport_camera_randomizer_sub_panel,
    # DRG_PT_viewport_dirt_generator_sub_panel,
    # DRG_PT_object_panel,
    # DRG_PT_object_tableware_creator_sub_panel,
    # DRG_PT_object_plate_characteristics_sub_panel,
    # DRG_PT_object_plate_curvature_sub_panel,
    # DRG_PT_object_spoon_characteristics_sub_panel,
    # DRG_PT_object_fork_characteristics_sub_panel,
    # DRG_PT_object_knife_characteristics_sub_panel,
    # DRG_PT_object_glass_characteristics_sub_panel,
    # DRG_PT_object_placemat_characteristics_sub_panel,
    # DRG_PT_object_chair_characteristics_sub_panel,
    # DRG_PT_object_room_characteristics_sub_panel,
    # DRG_PT_object_table_characteristics_sub_panel,
    # DRG_PT_object_dining_room_distribution_sub_panel,
    # DRG_PT_object_lighting_randomizer_sub_panel,
    # DRG_PT_object_camera_randomizer_sub_panel,
    # DRG_PT_object_dirt_generator_sub_panel,
]

class_register, class_unregister = bpy.utils.register_classes_factory(classes)


def register():
    class_register()
    # PROPERTIES
    bpy.types.Scene.render_index = bpy.props.IntProperty(
        name="render_index", default=0, min=0
    )
    bpy.types.Scene.amount_of_imgs = bpy.props.IntProperty(
        name="amount_of_imgs", default=1, min=1
    )
    bpy.types.Scene.render_filepath = bpy.props.StringProperty(
        name="render_filepath", default="<Please select export path.>"
    )

    bpy.types.Scene.datalogger_name = bpy.props.StringProperty(
        name="datalogger_name", default = "dining_room_dataset_logger"
    )


def unregister():
    # PROPERTIES
    del bpy.types.Scene.render_index
    del bpy.types.Scene.amount_of_imgs
    del bpy.types.Scene.render_filepath
    del bpy.types.Scene.datalogger_name
    class_unregister()


if __name__ == "__main__":
    register()
    print("run as script")
