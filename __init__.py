import bpy
from mathutils import Vector


bl_info = {
    "name": "Ratio Scale",
    "author": "Thanh Phan <thanhph111@gmail.com>",
    "version": (1, 0),
    "blender": (2, 83, 0),
    "category": "Object",
    "location": "Object > Transform > Ratio Scale",
    "description": "Scale objects with specific X, Y or Z dimension",
    "warning": "",
    "doc_url": "https://github.com/thanhph111/ratio-scale",
    "tracker_url": "",
    "support": "COMMUNITY",
}


class MESH_OT_ratio_scale(bpy.types.Operator):
    """Scale objects with specific X, Y or Z dimension"""

    bl_idname = "mesh.ratio_scale"
    bl_label = "Ratio Scale"
    bl_options = {"REGISTER", "UNDO"}

    # Define Variables
    dimension_x: bpy.props.FloatProperty(
        name="X",
        description="Dimension X of the active object",
        unit="LENGTH",
    )
    dimension_y: bpy.props.FloatProperty(
        name="Y",
        description="Dimension Y of the active object",
        unit="LENGTH",
    )
    dimension_z: bpy.props.FloatProperty(
        name="Z",
        description="Dimension Z of the active object",
        unit="LENGTH",
    )

    @classmethod
    def poll(_cls, context):
        return (
            context.area.type == "VIEW_3D"
            and bool(context.active_object)
            and context.active_object.dimensions != Vector((0, 0, 0))
        )

    def execute(self, context):
        if self.dimension_x != self.old_dimensions.x:
            ratio = self.dimension_x / self.old_dimensions.x
            context.active_object.dimensions = self.old_dimensions * ratio
            self.dimension_y = self.old_dimensions.y * ratio
            self.dimension_z = self.old_dimensions.z * ratio

        if self.dimension_y != self.old_dimensions.y:
            ratio = self.dimension_y / self.old_dimensions.y
            context.active_object.dimensions = self.old_dimensions * ratio
            self.dimension_x = self.old_dimensions.x * ratio
            self.dimension_z = self.old_dimensions.z * ratio

        if self.dimension_z != self.old_dimensions.z:
            ratio = self.dimension_z / self.old_dimensions.z
            context.active_object.dimensions = self.old_dimensions * ratio
            self.dimension_x = self.old_dimensions.x * ratio
            self.dimension_y = self.old_dimensions.y * ratio

        self.old_dimensions = Vector(
            (self.dimension_x, self.dimension_y, self.dimension_z)
        )

        return {"FINISHED"}

    def invoke(self, context, _event):
        self.old_dimensions = context.active_object.dimensions

        self.dimension_x = self.old_dimensions.x
        self.dimension_y = self.old_dimensions.y
        self.dimension_z = self.old_dimensions.z

        return self.execute(context)

    def draw(self, _context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(align=True)
        col.prop(self, "dimension_x", text="Dimension X")
        col.prop(self, "dimension_y")
        col.prop(self, "dimension_z")


def object_menu_draw(self, _context):
    """Draw operator on Object Transform Menu"""
    self.layout.operator(
        operator=MESH_OT_ratio_scale.bl_idname, text="Ratio Scale"
    )


def register():
    bpy.utils.register_class(MESH_OT_ratio_scale)
    bpy.types.VIEW3D_MT_transform_object.append(object_menu_draw)


def unregister():
    bpy.types.VIEW3D_MT_transform_object.remove(object_menu_draw)
    bpy.utils.unregister_class(MESH_OT_ratio_scale)
