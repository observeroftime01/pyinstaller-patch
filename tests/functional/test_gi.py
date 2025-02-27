#-----------------------------------------------------------------------------
# Copyright (c) 2005-2023, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License (version 2
# or later) with exception for distributing the bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
#-----------------------------------------------------------------------------
"""
Functional tests for PyGObject.
"""

import pytest

from PyInstaller.utils.tests import importorskip, parametrize

# Names of all "gi.repository" packages provided by PyGObject  to be tested below, typically corresponding to
# those packages hooked by PyInstaller.
_gi_repositories = [
    ('Gst', '1.0'),
    ('GLib', '2.0'),
    ('GModule', '2.0'),
    ('GObject', '2.0'),
    ('GdkPixbuf', '2.0'),
    ('Gio', '2.0'),
    ('Clutter', '1.0'),
    ('GtkClutter', '1.0'),
    ('Champlain', '0.12'),
    ('GtkChamplain', '0.12'),
]


# Test the usability of "gi.repository" packages provided by PyGObject.
@importorskip('gi.repository')
@parametrize(
    ('repository_name', 'version'),
    [pytest.param(name, version, marks=importorskip(f'gi.repository.{name}')) for name, version in _gi_repositories],
    ids=[name for name, version in _gi_repositories],  # Ensure human-readable test parameter names.
)
def test_gi_repository(pyi_builder, repository_name, version):
    """
    Test the importability of the `gi.repository` subpackage with the passed name installed with PyGObject. For example,
    `GLib`, corresponds to the `gi.repository.GLib` subpackage. Version '1.0' are for PyGObject >=1.0,
    '2.0' for PyGObject >= 2.0. Some other libraries have strange version (e.g., Champlain).
    """

    # Test the importability of this subpackage.
    pyi_builder.test_source(
        f"""
        import gi
        gi.require_version('{repository_name}', '{version}')
        from gi.repository import {repository_name}
        print({repository_name})
        """
    )
