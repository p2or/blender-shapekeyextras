# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Shape Key Extras",
    "description": "Shape Key Extras",
    "author": "Christian Brinkmann",
    "version": (0, 0, 6),
    "blender": (2, 74, 0),
    "location": "Properties > Object Data > Shape Keys",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}

import bpy
import random

from bpy.props import (IntProperty,
                       BoolProperty,
                       FloatProperty,
                       StringProperty,
                       PointerProperty,
                       EnumProperty
                       )

from bpy.types import (Operator,
                       PropertyGroup)

# -------------------------------------------------------------------
# helper    
# -------------------------------------------------------------------

def search_chars(char_sequence, name):
    if char_sequence:
        
        if char_sequence.endswith(','):
            char_sequence = char_sequence[:-1]
        if char_sequence.startswith(','):
            char_sequence = char_sequence[-1:]
            
        char_list = [i.strip() for i in char_sequence.split(",")]
        if name.startswith(tuple(char_list)) or name.endswith(tuple(char_list)):
            return True
        else: 
            return False
    else: 
        return False

def shape_key_selection(op, context):
    scn = context.scene
    ske = scn.shape_key_extras
    shape_key_names = []
    
    if not ske.only:
        for shapekey in context.object.data.shape_keys.key_blocks:
            exclude_char = search_chars(ske.exclude, shapekey.name)
            if exclude_char is not True:
                if ske.selection == 'ALL':
                    shape_key_names.append(shapekey.name)
                if ske.selection == 'ENABLED':
                    if shapekey.mute is False:
                        shape_key_names.append(shapekey.name)
                if ske.selection == 'DISABLED':
                    if shapekey.mute is True:
                        shape_key_names.append(shapekey.name)                  
    else:
        for shapekey in context.object.data.shape_keys.key_blocks:
            only_char = search_chars(ske.only, shapekey.name)
            if only_char is True:
                if ske.selection == 'ALL':
                    shape_key_names.append(shapekey.name)
                if ske.selection == 'ENABLED':
                    if shapekey.mute is False:
                        shape_key_names.append(shapekey.name)
                if ske.selection == 'DISABLED':
                    if shapekey.mute is True:
                        shape_key_names.append(shapekey.name)    
                
    return shape_key_names

# -------------------------------------------------------------------
# properties    
# -------------------------------------------------------------------

class ShapeKeyExtrasSettings(PropertyGroup):

    value = FloatProperty(
        name = "Value",
        description = "Set static value",
        default = 0,
        #min = 0,
        #max =1
        )
    random_min = FloatProperty(
        name = "Min",
        description = "Set minimum random value",
        default = 0,
        #min = 0,
        #max =1
        )
    random_max = FloatProperty(
        name = "Max",
        description = "Set maximum random value",
        default = 1,
        #min = 0,
        #max =1
        )
    apply_enabled = BoolProperty (
        name = "Apply values for enabled Keys only",
        description = "Apply values for enabled Keys only",
        default = True 
        )
    exclude = StringProperty (
        name = "Exclude",
        description = "Exclude by first character",
        default = "Basis, #, *"
        )
    only = StringProperty (
        name = "Include only",
        description = "Include by first character",
        default = ""
        )
    selection = EnumProperty(
        name="Selection",
        description="Shape Key Selection",
        items = (('ALL', "All", ""),
                ('ENABLED', "Enabled", ""),
                ('DISABLED', "Disabled", ""),
                ),default='ALL')

# -------------------------------------------------------------------
# operators    
# -------------------------------------------------------------------

class EnableAllButton (Operator):
    bl_idname = "shapekeyextras.enable_all"
    bl_label = "Enable All"
    bl_description = "Enable all Shape Keys"

    def execute(self, context):
        scn = context.scene
        ske = scn.shape_key_extras
        
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            shapekey = context.object.data.shape_keys.key_blocks[i]
            shapekey.mute = False

        self.report({'INFO'}, "All Shape Keys enabled")     
        return {'FINISHED'}

class DisableAllButton (Operator):
    bl_idname = "shapekeyextras.disable_all"
    bl_label = "Disable All"
    bl_description = "Disable all Shape Keys"
    
    def execute(self, context):
        scn = context.scene
        ske = scn.shape_key_extras
        
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            shapekey = context.object.data.shape_keys.key_blocks[i]
            shapekey.mute = True

        self.report({'INFO'}, "All Shape Keys disabled")        
        return {'FINISHED'}
   
class ToggleAllButton (Operator):
    bl_idname = "shapekeyextras.toggle_mute"
    bl_label = "Toggle Visibility"
    bl_description = "Toggle Mute of all Shape Keys"
    
    def execute(self, context):
        scn = context.scene
        ske = scn.shape_key_extras
        
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            shapekey = context.object.data.shape_keys.key_blocks[i]
            shapekey.mute = not shapekey.mute

        self.report({'INFO'}, "Enabled Shape Keys disabled and Disabled Shape Keys enabled")          
        return {'FINISHED'}
    
class RandomEnableButton (Operator):
    bl_idname = "shapekeyextras.random_visibility"
    bl_label = "Random Visibility"
    bl_description = "Random Visibility for all Shape Keys"

    def execute(self, context):
        scn = context.scene
        ske = scn.shape_key_extras
        
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            shapekey = context.object.data.shape_keys.key_blocks[i]
            shapekey.mute = bool(random.getrandbits(1))

        self.report({'INFO'}, "Ramdomized Shape Key Visibility")          
        return {'FINISHED'}

class RandomizeValueButton (Operator):
    bl_idname = "shapekeyextras.randomize"
    bl_label = "Randomize Shape Key Values"
    bl_description = "Randomize Shape Key Values"

    def execute(self, context):
        scn = context.scene
        ske = scn.shape_key_extras
        
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            if i != 'Basis':
                shapekey = context.object.data.shape_keys.key_blocks[i]
                shapekey.value = random.uniform(ske.random_min, ske.random_max)

        self.report({'INFO'}, "Values for Shape Keys generated")
        return {'FINISHED'}

class ApplyValueButton (Operator):
    bl_idname = "shapekeyextras.set_values"
    bl_label = "Set Shape Key Values"
    bl_description = "Apply a static Value to Shape Keys"

    def execute(self, context):
        scn = context.scene
        ske = scn.shape_key_extras
        
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            if i != 'Basis':
                shapekey = context.object.data.shape_keys.key_blocks[i]
                shapekey.value = ske.value
                
        self.report({'INFO'}, "Value assigned to Shape Keys")        
        return {'FINISHED'}
    
class RemoveDriversFromShapeKeysButton (Operator):
    bl_idname = "shapekeyextras.remove_drivers"
    bl_label = "Remove Drivers"
    bl_description = "Remove Drivers from Shapekeys"

    def execute(self, context):
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            if i != 'Basis':
                context.object.data.shape_keys.key_blocks[i].driver_remove("value")
        
        self.report({'INFO'}, "Drivers Removed")
        return {'FINISHED'}
     
class AddDriversToShapeKeysButton (Operator):
    bl_idname = "shapekeyextras.add_drivers"
    bl_label = "Add Drivers"
    bl_description = "Add Drivers to Shapekeys"
    
    def execute(self, context):       
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            if i != 'Basis':
                context.object.data.shape_keys.key_blocks[i].driver_add("value")
        
        self.report({'INFO'}, "Drivers added")
        return {'FINISHED'}

# http://stackoverflow.com/questions/7977550/how-to-change-the-value-of-the-shape-key-in-blender-script
class InsertKeyframeButton (Operator):
    bl_idname = "shapekeyextras.insert_keyframe"
    bl_label = "Insert Keyframe"
    bl_description = "Insert Keyframe for value"
    
    def execute(self, context):       
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            if i != 'Basis':
                context.object.data.shape_keys.key_blocks[i].keyframe_insert(data_path="value")
        
        self.report({'INFO'}, "Keyframes inserted")
        return {'FINISHED'}

class DeleteKeyframeButton (Operator):
    bl_idname = "shapekeyextras.delete_keyframe"
    bl_label = "Delete current Keyframe"
    bl_description = "Delete Keyframe for value"
    
    def execute(self, context):       
        shape_keys = (shape_key_selection(self, context))
        for i in shape_keys:
            if i != 'Basis':
                context.object.data.shape_keys.key_blocks[i].keyframe_delete(data_path="value")
        
        self.report({'INFO'}, "Keyframes deleted")
        return {'FINISHED'}


# http://blender.stackexchange.com/questions/5827/get-shape-key-from-action-or-fcurve-in-python
class DeleteAllKeyframesButton (Operator):
    bl_idname = "shapekeyextras.delete_all_keyframes"
    bl_label = "Delete all Keyframes"
    bl_description = "Delete all Keyframes for value"
    
    def execute(self, context):
        sce = context.scene       
        shape_keys = (shape_key_selection(self, context))
        sk_data = context.object.data.shape_keys
        
        for i in shape_keys:
            if i != 'Basis':
                for f in range(sce.frame_start, sce.frame_end+1):
                    if sk_data.animation_data.action != None:
                        sk_data.key_blocks[i].keyframe_delete(data_path="value", frame=f) #returns a bool
                    else:
                        break
                        
        self.report({'INFO'}, "All Keyframes deleted")

        return {'FINISHED'}
    
    
class PrintShapeKeySelectionButton (Operator):
    bl_idname = "shapekeyextras.print_shape_key_selection"
    bl_label = "Print Selection to the Console"
    bl_description = "Print Shape Key Selection to the Console"
    
    def execute(self, context):       
        shape_keys = (shape_key_selection(self, context))
        print (shape_keys)
                
        self.report({'INFO'}, "Shape Keys printed")
        return {'FINISHED'}
    
# -------------------------------------------------------------------
# ui    
# -------------------------------------------------------------------

def draw_shapekey_extras(self, context):

    scn = context.scene
    layout = self.layout
    ske = scn.shape_key_extras

    layout.separator()

    row = layout.row()
    row.label("Visibility:")
    col = layout.column(align=True)
    rowsub = col.row(align=True)
    rowsub.operator("shapekeyextras.enable_all", icon="RESTRICT_VIEW_OFF")
    rowsub.operator("shapekeyextras.toggle_mute", icon="FILE_REFRESH")
    rowsub = col.row(align=True)
    rowsub.operator("shapekeyextras.disable_all", icon="RESTRICT_VIEW_ON")
    rowsub.operator("shapekeyextras.random_visibility", icon="RESTRICT_VIEW_OFF")
    
    row = layout.row()   
    row.label("Set Attributes:")
    col = layout.column(align=True)
    row = col.row(align=True)
    row.prop(ske, "selection", expand=True)
    
    row = layout.row()
    col = layout.column(align=True)
    col.prop(ske, "value")
    col.operator("shapekeyextras.set_values", icon="KEY_HLT")
    rowsub = col.row(align=True)
    rowsub.prop(ske, "random_min")
    rowsub.prop(ske, "random_max")
    col.operator("shapekeyextras.randomize", icon="KEYINGSET")
   
    row = layout.row()
    col = layout.column(align=True)
    rowsub = col.row(align=True)
    rowsub.operator("shapekeyextras.insert_keyframe", icon="ACTION")
    rowsub = col.row(align=True)
    rowsub.operator("shapekeyextras.delete_keyframe", icon="PANEL_CLOSE")
    rowsub.operator("shapekeyextras.delete_all_keyframes", icon="PANEL_CLOSE")
    
    row = layout.row()
    col = layout.column(align=True)
    rowsub = col.row(align=True)
    rowsub.operator("shapekeyextras.add_drivers", icon="DRIVER")
    rowsub = col.row(align=True)
    rowsub.operator("shapekeyextras.remove_drivers", icon="PANEL_CLOSE")
    
    row = layout.row()
    col = layout.column(align=True)
    row = col.row(align=True)
    col.prop(ske, "exclude")
    col = layout.column(align=True)
    col.prop(ske, "only")
    
    #row = layout.row()
    #row.operator("shapekeyextras.print_shape_key_selection")
    layout.separator()

# -------------------------------------------------------------------
# register    
# -------------------------------------------------------------------

def register():
    bpy.utils.register_module(__name__)
    bpy.types.DATA_PT_shape_keys.append(draw_shapekey_extras)
    bpy.types.Scene.shape_key_extras = PointerProperty(type=ShapeKeyExtrasSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.DATA_PT_shape_keys.remove(draw_shapekey_extras)
    del bpy.types.Scene.shape_key_extras

if __name__ == "__main__":
    register()
