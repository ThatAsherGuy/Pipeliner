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

bl_info = {
    "name" : "Pipeliner",
    "author" : "ThatAsherGuy",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Yes"
}

import bpy

from .operators import PIPELINER_OT_SetDimensions
from .operators import PIPELINER_OT_ChurnNext
from .operators import PIPELINER_OT_SetChurnList
from .operators import PIPELINER_OT_MeshExport
from .operators import PIPELINER_OT_BulkExport
from .operators import PIPELINER_OT_UVSetup

from .properties import PIPELINER_File
from .properties import PIPELINER_TaskProps
from .properties import PIPELINER_ExportProps
from .properties import PIPELINER_CollectionExtras

from .interface import PL_PT_MainPanel
from .interface import PL_PT_ExportPanel
from .interface import PL_PT_CollectionExtras

from . preferences import PipelinerAddonPrefs

classes = (
    # Preferences
    PipelinerAddonPrefs,
    # Ops
    PIPELINER_OT_SetDimensions,
    PIPELINER_OT_ChurnNext,
    PIPELINER_OT_SetChurnList,
    PIPELINER_OT_MeshExport,
    PIPELINER_OT_BulkExport,
    PIPELINER_OT_UVSetup,
    # Props
    PIPELINER_File,
    PIPELINER_TaskProps,
    PIPELINER_ExportProps,
    PIPELINER_CollectionExtras,
    # UI
    PL_PT_MainPanel,
    PL_PT_ExportPanel,
    PL_PT_CollectionExtras,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.PIPE = bpy.props.PointerProperty(type=PIPELINER_TaskProps)
    bpy.types.Object.PIPE = bpy.props.PointerProperty(type=PIPELINER_ExportProps)
    bpy.types.Collection.PIPE = bpy.props.PointerProperty(type=PIPELINER_ExportProps)
    bpy.types.Collection.PIPE_extras = bpy.props.PointerProperty(type=PIPELINER_CollectionExtras)

def unregister():

    del bpy.types.Scene.PIPE
    del bpy.types.Object.PIPE
    del bpy.types.Collection.PIPE
    del bpy.types.Collection.PIPE_extras

    for cls in classes:
        bpy.utils.unregister_class(cls)
