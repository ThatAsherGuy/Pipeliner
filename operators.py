# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Hell is other people's code

import bpy
from bpy.props import BoolProperty, EnumProperty
import mathutils
import os


class PIPELINER_OT_SetDimensions(bpy.types.Operator):
    bl_idname = "pipe.set_dimensions"
    bl_label = "Pipeliner: Set Dimensions"
    bl_description = "Sets the dimensions of the selection"
    bl_options = {'REGISTER', 'UNDO'}

    dimensions: bpy.props.FloatVectorProperty(
        name="Dimensions",
        description="The target dimensions to achieve",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION' # needs to be a unit, rather than a factor
    )

    main_axis: bpy.props.EnumProperty(
        items = [("X", "X", ""),
                 ("Y", "Y", ""),
                 ("Z", "Z", "")],
        name="Main Axis",
        description="Which axis use as the basis for uniform scaling",
        default='X'
    )

    do_uniform: bpy.props.BoolProperty(
        name="Uniform Scale",
        description="Objects are scaled uniformly to fit the Main Axis",
        default=True
    )

    apply_scale: bpy.props.BoolProperty(
        name="Apply Scale",
        description="Automatically apply the scale to the selected objects",
        default=True
    )

    def invoke(self, context, event):
        # We do all of this in the invoke portion in order to pre-populate the dimensions field
        debug = -1
        # min/max pairs.
        x_val = [999999.0, -999999.0]
        y_val = [999999.0, -999999.0]
        z_val = [999999.0, -999999.0]

        # BBox corners are all in local-space
        tot_bounds = []
        for obj in context.selected_editable_objects:
            box = obj.bound_box
            for point in box:
                point = mathutils.Vector(point)
                point *= obj.matrix_world.to_scale()
                point.rotate(obj.matrix_world.to_quaternion())
                point += obj.location.copy()

                if debug > 1:
                    print(f"Point: {point}")

                if point[0] < x_val[0]:
                    x_val[0] = point[0]
                elif point[0] > x_val[1]:
                    x_val[1] = point[0]

                if point[1] < y_val[0]:
                    y_val[0] = point[1]
                elif point[1] > y_val[1]:
                    y_val[1] = point[1]

                if point[2] < z_val[0]:
                    z_val[0] = point[2]
                elif point[2] > z_val[1]:
                    z_val[1] = point[2]

                tot_bounds.append(point)

        x_size = abs((x_val[1]) - (x_val[0]))
        y_size = abs((y_val[1]) - (y_val[0]))
        z_size = abs((z_val[1]) - (z_val[0]))

        sizes = (x_size, y_size, z_size)
        vals = [x_val, y_val, z_val]

        self.dimensions = sizes
        self.current_sizes = sizes

        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        debug = -1

        # Blender handles enums as strings,
        # so we bullshit it with a dictionary
        hack = {
            'X': 0,
            'Y': 1,
            'Z': 2
        }

        if self.do_uniform:
            axis_index = hack.get(self.main_axis)
            current = self.current_sizes[axis_index]
            target = self.dimensions[axis_index]

            factor = abs(target/current)
            if debug > 0:
                print(f"Current length: {current}")
                print(f"Target length: {target}")
                print(f"Calculated Factor: {factor}")
            factor = (factor, factor, factor)

            bpy.ops.transform.resize(
                value=factor,
                orient_type='GLOBAL',
                orient_matrix=((1,0,0), (0,1,0), (0,0,1)),
                orient_matrix_type='GLOBAL',
                constraint_axis = (False, False, False),
                use_proportional_edit=False
            )

            if self.apply_scale:
                bpy.ops.object.transform_apply(
                    location=False,
                    rotation=False,
                    scale=True)

        return {'FINISHED'}


class PIPELINER_OT_ConformScene(bpy.types.Operator):
    bl_idname = "pipe.conform_scene"
    bl_label = "Pipeliner: conform_scene"
    bl_description = "Alters the current scene settings to match the active project"
    bl_options = {'REGISTER', 'UNDO'}


class PIPELINER_OT_BulkMarkAssets(bpy.types.Operator):
    bl_idname = "pipe.bulk_mark_assets"
    bl_label = "Pipeliner: Bulk Mark Assets"
    bl_description = "Churns through the .blend files in a directory and marks their collections as assets"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.blend'
    filter_glob: bpy.props.StringProperty(default='*.blend')

    files: bpy.props.CollectionProperty(name = 'Files', type= bpy.types.OperatorFileListElement)
    directory: bpy.props.StringProperty(subtype = 'DIR_PATH')
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for importing the file",
        maxlen=1024,
        subtype='FILE_PATH',
    )

    def invoke(self, context, _event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):

        for file in self.files:
            fpath = os.path.join(self.directory, file.name)
            bpy.ops.wm.open_mainfile(
                'EXEC_DEFAULT',
                True,
                filepath=fpath,
            )

            outliner = None
            ref_area = None
            for area in context.window_manager.windows[0].screen.areas:
                if area.type == 'OUTLINER':
                    ref_area = area
                    outliner = area.spaces[0]
                    break

            if outliner:
                outliner.use_filter_object = False
                override = bpy.context.copy()
                override['space_data'] = outliner
                override['area'] = ref_area
                override['window'] = context.window_manager.windows[0]
                override['screen'] = context.window_manager.windows[0].screen
                # override['collection']

                print(override['area'].type)
                for i in range(3):
                    bpy.ops.outliner.select_walk(override, 'EXEC_AREA', direction='DOWN')

                for lcol in context.view_layer.layer_collection.children:
                    override['collection'] = lcol
                    bpy.ops.asset.mark(
                        override,
                        'EXEC_SCREEN'
                    )

        return {'FINISHED'}


class PIPELINER_OT_ChurnNext(bpy.types.Operator):
    bl_idname = "pipe.churn_next"
    bl_label = "Pipeliner: Churn Next"
    bl_description = "Opens the next file in the churn list"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tasks = context.scene.PIPE
        list_length = len(tasks.churn_list) - 1

        if list_length > tasks.churn_index:
            tasks.churn_index += 1
            current_index = context.scene.PIPE.churn_index

            target_path = tasks.churn_list[current_index].path

            old_list = [entry.path for entry in tasks.churn_list]

            bpy.ops.wm.open_mainfile(
                'EXEC_DEFAULT',
                True,
                filepath=target_path,
            )

            tasks = context.scene.PIPE
            tasks.churn_list.clear()
            
            for old_thing in old_list:
                new_thing = tasks.churn_list.add()
                new_thing.path = old_thing

            context.scene.PIPE.churn_index = current_index

            return {'FINISHED'}
        else:
            self.report({'INFO'}, "End of List")
            return {'CANCELLED'}


class PIPELINER_OT_SetChurnList(bpy.types.Operator):
    bl_idname = "pipe.set_churn_list"
    bl_label = "Pipeliner: Set Churn List"
    bl_description = "Sets the churn list"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.blend'
    filter_glob: bpy.props.StringProperty(default='*.blend')

    files: bpy.props.CollectionProperty(name = 'Files', type= bpy.types.OperatorFileListElement)
    directory: bpy.props.StringProperty(subtype = 'DIR_PATH')
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for importing the file",
        maxlen=1024,
        subtype='FILE_PATH',
    )

    def invoke(self, context, _event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


    def execute(self, context):

        for file in self.files:
            item = context.scene.PIPE.churn_list.add()
            item.path = os.path.join(self.directory, file.name)

        context.scene.PIPE.churn_index = -1

        return {'FINISHED'}


class PIPELINER_OT_MeshExport(bpy.types.Operator):
    bl_idname = "pipe.mesh_export"
    bl_label = "Pipeliner: Mesh Export"
    bl_description = "Wraps the default FBX importer in a layer of bullshit"
    bl_options = {'REGISTER', 'UNDO'}

    # DIRECTORY STUFF
    filename_ext = ''
    filter_glob: bpy.props.StringProperty(default='', options={'HIDDEN'})

    files: bpy.props.CollectionProperty(name = 'Files', type= bpy.types.OperatorFileListElement)
    directory: bpy.props.StringProperty(subtype = 'DIR_PATH')
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for importing the file",
        maxlen=1024,
        subtype='FILE_PATH',
    )

    # EXPORTER MODE STUFF (Read: things not overridable)

    export_mode_items = [
        ('SELECTED', "Export Selected", ""),
        ('AUTO', "Auto Export", "Exports objects from the auto-list")
    ]

    export_mode: bpy.props.EnumProperty(
        items=export_mode_items,
        name="Export Mode",
        description="What kind of export to run",
        default='SELECTED',
        options={'HIDDEN'}
    )

    use_overrides: bpy.props.BoolProperty(
        name="Use Overrides",
        description="Let objects override the export settings",
        default=True
    )

    triangulate: bpy.props.BoolProperty(
        name="Auto-Triangulate",
        description="Throws a Triangulate modifier on there for you",
        default=True
    )

    expand_linked_instances: bpy.props.BoolProperty(
        name="Expand Linked Instances",
        description="Drills down into the source file for linked collection instances and exports using the local configuration",
        default=False
    )

    use_validation: bpy.props.BoolProperty(
        name="Validate",
        description="Blocks your bullshit",
        default=False
    )

    validation_level_items = [
        ('YOLO', "Permissive", "Blocks on show-stoppers"),
        ('MODERATE', "Moderate", "Blocks on show-stoppers and issues that can't be auto-fixed"),
        ('STRICT', "Strict", "Block on all issues")
    ]

    validation_level: bpy.props.EnumProperty(
        items=validation_level_items,
        name="Validation Level",
        description="How strictly the exporter should validate the mesh",
        default='MODERATE'
    )

    clear_loc: bpy.props.BoolProperty(
        name="Clear Location",
        description="",
        default=True
        )
    
    clear_rot: bpy.props.BoolProperty(
        name="Clear Rotation",
        description="",
        default=False
    )

    do_delta_loc: bpy.props.BoolProperty(
        name="Add Location Delta",
        description="Add an additional offset to the object location",
        default=False
    )

    delta_loc: bpy.props.FloatVectorProperty(
        name="Translation Delta",
        description="",
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION'
    )

    do_delta_rot: bpy.props.BoolProperty(
        name="Add Rotation Delta",
        description="Add an additional offset to the object rotation",
        default=False
    )

    delta_rot: bpy.props.FloatVectorProperty(
        name="Rotation Delta",
        description="",
        default=(0.0, 0.0, 0.0),
        subtype='EULER'
    )

    forward_axis_items = [
        ('POS_X', "+X Forward", ""),
        ('POS_Y', "+Y Forward", ""),
        ('POS_Z', "+Z Forward", ""),
        ('NEG_X', "-X Forward", ""),
        ('NEG_Y', "-Y Forward", ""),
        ('NEG_Z', "-Z Forward", "")]

    forward_axis: bpy.props.EnumProperty(
        items=forward_axis_items,
        name="Forward Axis",
        description="",
        default='POS_Y'
    )

    up_axis_items = [
        ('POS_X', "+X Up", ""),
        ('POS_Y', "+Y Up", ""),
        ('POS_Z', "+Z Up", ""),
        ('NEG_X', "-X Up", ""),
        ('NEG_Y', "-Y Up", ""),
        ('NEG_Z', "-Z Up", "")]

    up_axis: bpy.props.EnumProperty(
        items=up_axis_items,
        name="Up Axis",
        description="",
        default='POS_Z'
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        axis_hack = {
            'POS_X': 'X',
            'POS_Y': 'Y',
            'POS_Z': 'Z',
            'NEG_X': '-X',
            'NEG_Y': '-Y',
            'NEG_Z': '-Z',
        }

        target_dir = self.directory

        if not os.path.isdir(target_dir):
            self.report({'WARNING'}, "You fucking broke it.")
            return {'CANCELLED'}

        target_objs = context.selected_objects

        for obj in target_objs:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)

            if self.use_overrides:
                if obj.PIPE.use_overrides:
                    exp = obj.PIPE
                else:
                    exp = self
            else:
                exp = self

            file_name = obj.name + ".fbx"
            full_path = os.path.join(target_dir, file_name)

            mods = []

            if exp.triangulate:
                mod = obj.modifiers.new("triangulate", 'TRIANGULATE')
                mod.keep_custom_normals = True
                mods.append(mod)

            bpy.ops.export_scene.fbx(
                filepath=full_path,
                check_existing=False, #Auto-overwrite
                filter_glob='*.fbx',

                use_selection=True, # So we can do some macro-selecting to ensure the right export group
                object_types={'EMPTY', 'MESH', 'OTHER'}, # So we can use empties as sockets/locators

                apply_unit_scale=False,
                apply_scale_options='FBX_SCALE_UNITS',
                use_space_transform=True,

                use_mesh_modifiers=True,
                use_mesh_modifiers_render=True,
                mesh_smooth_type='FACE',

                batch_mode='OFF', # Batches are created manually

                axis_forward=axis_hack[exp.forward_axis],
                axis_up=axis_hack[exp.up_axis],
                bake_space_transform=False
            )

            for mod in mods:
                obj.modifiers.remove(mod)

        return {'FINISHED'}
