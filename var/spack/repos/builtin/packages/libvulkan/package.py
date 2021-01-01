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
#     spack install libvulkan
#
# You can edit this file again by typing:
#
#     spack edit libvulkan
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Libvulkan(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.khronos.org/vulkan/"
    git      = "https://github.com/KhronosGroup/Vulkan-Loader.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions and checksums here.
    version('1.2.158', tag='v1.2.158')

    # FIXME: Add dependencies if required.
    depends_on('vulkan-headers', type='build')
    depends_on('libx11', type='link')
    depends_on('libxrandr', type='link')
    depends_on('libxcb', type='link')
    depends_on('wayland', type='link')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = [
            '-DVULKAN_HEADERS_INSTALL_DIR=%s' % self.spec['vulkan-headers'].prefix,
            '-DBUILD_TESTS=OFF',
        ]
        return args
