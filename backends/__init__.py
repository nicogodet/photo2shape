# -*- coding: utf-8 -*-

"""
***************************************************************************
    __init__.py
    ---------------------
    Date                 : April 2018
    Copyright            : (C) 2018 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'April 2018'
__copyright__ = '(C) 2018, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import inspect
from importlib import util

from qgis.core import Qgis, QgsMessageLog

from photo2shape.backends.backendbase import BackendBase


def loadBackends():
    folder = os.path.dirname(__file__)
    for fileName in os.listdir(folder):
        if fileName.endswith('.py') and fileName not in ['__init__.py']:
            moduleName = os.path.splitext(fileName)[0]
            spec = util.spec_from_file_location(moduleName, os.path.join(folder, fileName))
            module = util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                QgsMessageLog.logMessage('Could not load backend from "{filename}": {error}'.format(filename=os.path.join(folder, fileName), error=str(e)), 'Photo2Shape')
                continue

            for x in dir(module):
                obj = getattr(module, x)
                if inspect.isclass(obj) and issubclass(obj, BackendBase) and obj.__name__ != 'BackendBase':
                    w = obj()
                    backendsRegistry[w.name()] = w


backendsRegistry = dict()
loadBackends()
