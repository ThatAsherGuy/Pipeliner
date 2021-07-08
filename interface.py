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

class View3dPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        if context.view_layer.objects.active:
            return True

class OverridePanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "PL_PT_MainPanel"


class PL_PT_MainPanel(View3dPanel, bpy.types.Panel):
    bl_idname = "PL_PT_MainPanel"
    bl_label = "Pipeliner Tools"

    def draw(self, context):
        obj = context.view_layer.objects.active
        exp = obj.PIPE

        layout = self.layout
        root = layout.column(align=True)

        row = root.column(align=True)

        op = row.operator(
            "pipe.mesh_export",
            text="Export Selected"
        )
        op.export_mode = 'SELECTED'

        op = row.operator(
            "pipe.mesh_export",
            text=" Auto Export"
        )
        op.export_mode = 'AUTO'

        # root.prop(op, "export_mode", expand=True)

        # root.prop(op, "export_target", expand =True)
        


def draw_export_overrides(context, layout, target):
    exp = target.PIPE

    layout = layout
    layout = layout.column(align=True)

    header = layout.row(align=True)
    header.prop(exp, "use_overrides")

    root = layout.column(align=True)
    root.enabled = exp.use_overrides
    root.prop(exp, "triangulate")

    if exp.use_validation:
        row = root.split(factor=0.35, align=True)
        row.prop(exp, "use_validation", toggle=True)
        row.prop(exp, "validation_level", text="")
    else:
        row = root.row(align=True)
        row.prop(exp, "use_validation", text="Validate on Export")

    root.separator(factor=2.0)

    col = root.column(align=True, heading="Orientation Mangling")
    col.use_property_split = True
    col.use_property_decorate = False
    col.prop(exp, "forward_axis", text="")
    col.prop(exp, "up_axis", text="")
    col.separator(factor=2.0)

    col = root.column(align=True, heading="Worldspace Transforms")
    col.prop(exp, "clear_loc")
    col.prop(exp, "clear_rot")
    col.prop(exp, "clear_scale")
    col.separator(factor=2.0)

    col = root.column(align=True, heading="Delta Transforms")
    col.prop(exp, "do_delta_loc")
    if exp.do_delta_loc:
        col.prop(exp, "delta_loc", text="")
        col.separator(factor=2.0)

    col.prop(exp, "do_delta_rot")
    if exp.do_delta_rot:
        col.prop(exp, "delta_rot", text="")
        col.separator(factor=2.0)



class PL_PT_ExportPanel(View3dPanel, bpy.types.Panel):
    bl_idname = "PL_PT_ExportPanel"
    bl_label = "Object Export Overrides"
    bl_parent_id = "PL_PT_MainPanel"

    def draw(self, context):
        obj = context.view_layer.objects.active
        exp = obj.PIPE

        root = self.layout.column(align=True)
        root.label(text="Object Settings")

        col = root.column(align=True)
        col.use_property_split = True
        col.use_property_decorate = False

        col.prop(obj, "name")
        col.prop(exp, "export_mode")

        root.separator(factor=2.0)

        draw_export_overrides(context, root, obj)


class PL_PT_CollectionOverrides(OverridePanel, bpy.types.Panel):
    bl_idname = "PL_PT_CollectionOverrides"
    bl_label = "Colllection Export Overrides"

    @classmethod
    def poll(cls, context):
        if context.view_layer.active_layer_collection:
            return True

    def draw(self, context):
        collection = context.view_layer.active_layer_collection.collection
        exp = collection.PIPE

        root = self.layout.column(align=True)
        root.label(text="Collection Settings")

        col = root.column(align=True)
        col.use_property_split = True
        col.use_property_decorate = False

        col.prop(collection, "name")
        col.prop(exp, "export_mode")

        root.separator(factor=2.0)

        draw_export_overrides(context, root, context.view_layer.active_layer_collection.collection)


