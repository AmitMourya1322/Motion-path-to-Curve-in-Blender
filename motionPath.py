bl_info = {
    "name": "Motion Path to Curve",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

def convert_motion_path_to_curve(self, context):
    ob = bpy.context.object
    mp = ob.motion_path

    if mp:
        path = bpy.data.curves.new('path', 'CURVE')
        curve = bpy.data.objects.new('Curve', path)
        bpy.context.scene.collection.objects.link(curve)
        path.dimensions = '3D'
        spline = path.splines.new('BEZIER')
        spline.bezier_points.add(len(mp.points) - 1)

        for i, o in enumerate(spline.bezier_points):
            o.co = mp.points[i].co
            o.handle_right_type = 'AUTO'
            o.handle_left_type = 'AUTO'

class MotionPathToCurveOperator(bpy.types.Operator):
    bl_idname = "object.motion_path_to_curve"
    bl_label = "Convert Motion Path to Curve"

    def execute(self, context):
        convert_motion_path_to_curve(self, context)
        return {'FINISHED'}

class MotionPathToCurvePanel(bpy.types.Panel):
    bl_label = "Motion Path to Curve"
    bl_idname = "PT_MotionPathToCurve"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.motion_path_to_curve")

def menu_func(self, context):
    self.layout.operator(MotionPathToCurveOperator.bl_idname)

def register():
    bpy.utils.register_class(MotionPathToCurveOperator)
    bpy.utils.register_class(MotionPathToCurvePanel)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MotionPathToCurveOperator)
    bpy.utils.unregister_class(MotionPathToCurvePanel)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
