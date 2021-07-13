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
from bpy.path import display_name
from bpy.types import PropertyGroup

class PIPELINER_File(PropertyGroup):
    name: bpy.props.StringProperty(
        name="File Name",
        default=""
    )

    path: bpy.props.StringProperty(
        name="File Path",
        description="",
        default="",
        subtype='FILE_PATH'
    )

class PIPELINER_TaskProps(PropertyGroup):
    churn_list: bpy.props.CollectionProperty(name="Churn List", type=PIPELINER_File)

    churn_index: bpy.props.IntProperty(
        name="Churn Index",
        description="Current position in the churn list",
        default=-1
    )

    def set_churn_list(self, new_list):
        self.churn_list.clear()

# Contains both overrides and general settings
class PIPELINER_ExportProps(PropertyGroup):

    export_mode_items = [
        ('NO_EXPORT', "Don't Export", "This item will not be exported; can't be overridden"),
        ('MANUAL_EXPORT', "Manual Export", "This item will only be exported when it is selected"),
        ('DEPENDENT_EXPORT', "Dependent Export", "This item will be exported if it is selected, or its parent is exported"),
        ('AUTO_EXPORT', "Auto-Export", "This item will be included in the automatic export list")
    ]

    export_mode: bpy.props.EnumProperty(
        items=export_mode_items,
        name="Export Mode",
        description="How Pipeliner should handle exporting this object",
        default='DEPENDENT_EXPORT'
    )

    # OVERRIDES START HERE

    use_overrides: bpy.props.BoolProperty(
        name="Use Overrides",
        description="Use this object's export property overrides",
        default=False
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

    clear_scale: bpy.props.BoolProperty(
        name="Clear Scale",
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

class PIPELINER_CollectionExtras(PropertyGroup):

    display_name: bpy.props.StringProperty(
        name="Display Name",
        description="The user-facing name for this asset",
        default="NULL"
    )