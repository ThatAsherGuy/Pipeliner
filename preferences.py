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

# Hell is other people's code

import bpy
import os

def get_prefs():
	# return bpy.context.preferences.addons[get_name()].preferences
	return bpy.context.preferences.addons[__package__].preferences

class PipelinerAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    default_dir: bpy.props.StringProperty(
        name="Default Bulk Export Directory",
        description="Where bulk exports go",
        subtype='DIR_PATH'
    )

    def draw(self, context):
        layout = self.layout
        root = layout.column(align=True)

        root.prop(self, 'default_dir')