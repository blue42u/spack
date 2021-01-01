# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install spirv-tools
#
# You can edit this file again by typing:
#
#     spack edit spirv-tools
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class SpirvTools(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    git      = "https://github.com/KhronosGroup/SPIRV-Tools.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions and checksums here.
    version('master', branch='master')

    # FIXME: Add dependencies if required.
    depends_on('spirv-headers')

    patch('cmake-target-fix.patch')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = [
            '-DSPIRV-Headers_SOURCE_DIR=%s' % self.spec['spirv-headers'].prefix,
            '-DSPIRV_SKIP_TESTS=ON',
        ]
        return args
