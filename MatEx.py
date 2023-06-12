bl_info = {
    "name": "MatEx",
    "author": "metarex21",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "File > Export/Import",
    "description": "Effortlessly export and import Blender materials as a separate blend file.",
    "category": "Import-Export"
}

import bpy

class MaterialExporterOperator(bpy.types.Operator):
    bl_idname = "object.export_materials"
    bl_label = "Export Materials"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH", default=".blend")
    
    def execute(self, context):
        materials = []
        
        # Iterate over materials in the scene
        for material in bpy.data.materials:
            materials.append(material)
        
        # Save materials to a separate blend file
        bpy.ops.wm.save_as_mainfile(filepath=self.filepath, check_existing=False, compress=True, copy=False)
        
        self.report({'INFO'}, "Materials exported successfully.")
        return {'FINISHED'}

class MaterialImporterOperator(bpy.types.Operator):
    bl_idname = "object.import_materials"
    bl_label = "Import Materials"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH", default=".blend")
    
    def execute(self, context):
        # Append materials from the blend file to the current scene
        bpy.ops.wm.link(directory=self.filepath, filename="", link=False, autoselect=True)
        
        self.report({'INFO'}, "Materials imported successfully.")
        return {'FINISHED'}

def menu_func_export(self, context):
    self.layout.operator(MaterialExporterOperator.bl_idname, text="Export Materials")

def menu_func_import(self, context):
    self.layout.operator(MaterialImporterOperator.bl_idname, text="Import Materials")

classes = (
    MaterialExporterOperator,
    MaterialImporterOperator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
