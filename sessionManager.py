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

#  __  __     __   ___      __
# |__)|_  /\ |  \   | |__||(_ 
# | \ |__/--\|__/   | |  ||__)
# 
# This module is likely a bad idea. Seriously.
# A 'sessionManager' is my fancy name for the global object pattern, AKA a stateful object
# that hangs out in memory, that isn't directly tied to a Blender property. It's hacky shit.

# This sessionManager lets me retain data as the exporter bounces from file-to-file, without having to
# cart that data around inside the export operator that's doing the file traversal.

import bpy
import os
import json
import datetime