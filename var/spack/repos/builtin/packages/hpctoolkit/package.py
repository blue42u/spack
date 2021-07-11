# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hpctoolkit(MesonPackage):
    """HPCToolkit is an integrated suite of tools for measurement and analysis
    of program performance on computers ranging from multicore desktop systems
    to the nation's largest supercomputers. By using statistical sampling of
    timers and hardware performance counters, HPCToolkit collects accurate
    measurements of a program's work, resource consumption, and inefficiency
    and attributes them to the full calling context in which they occur."""

    homepage = "http://hpctoolkit.org"
    git      = "https://github.com/HPCToolkit/hpctoolkit.git"
    maintainers = ['mwkrentel']

    tags = ['e4s']

    version('master', branch='new-buildsys', git='https://github.com/blue42u/hpctoolkit.git')

    # Options for MPI and hpcprof-mpi.  We always support profiling
    # MPI applications.  These options add hpcprof-mpi, the MPI
    # version of hpcprof.  Cray and Blue Gene need separate options
    # because an MPI module in packages.yaml doesn't work on these
    # systems.
    variant('cray', default=False,
            description='Build for Cray compute nodes, including '
            'hpcprof-mpi.')

    variant('mpi', default=False,
            description='Build hpcprof-mpi, the MPI version of hpcprof.')

    # We can't build with both PAPI and perfmon for risk of segfault
    # from mismatched header files (unless PAPI installs the perfmon
    # headers).
    variant('papi', default=True,
            description='Use PAPI instead of perfmon for access to '
            'the hardware performance counters.')

    variant('all-static', default=False,
            description='Needed when MPICXX builds static binaries '
            'for the compute nodes.')

    variant('cuda', default=False,
            description='Support CUDA on NVIDIA GPUs (2020.03.01 or later).')

    variant('rocm', default=False,
            description='Support ROCM on AMD GPUs, requires ROCM as '
            'external packages (2021.03.01 or later).')

    variant('debug', default=False,
            description='Build in debug (develop) mode.')

    variant('viewer', default=True, description='Include hpcviewer.')

    boost_libs = (
        '+atomic +chrono +date_time +filesystem +system +thread +timer'
        ' +graph +regex +shared +multithreaded visibility=global'
    )

    depends_on('binutils +libiberty', type='link', when='@2021.00:')
    depends_on('binutils +libiberty~nls', type='link', when='@2020.04:2020')
    depends_on('binutils@:2.33.1 +libiberty~nls', type='link', when='@:2020.03')
    depends_on('boost' + boost_libs)
    depends_on('bzip2+shared', type='link')
    depends_on('cmake', type='build')
    depends_on('dyninst@10.2.0:', when='@2021.00:')
    depends_on('dyninst@9.3.2:', when='@:2020')
    depends_on('elfutils+bzip2+xz~nls', type='link')
    depends_on('gotcha@1.0.3:')
    depends_on('intel-tbb+shared')
    depends_on('libdwarf')
    depends_on('libmonitor+hpctoolkit~dlopen', when='@2021.00:')
    depends_on('libmonitor+hpctoolkit+dlopen', when='@:2020')
    depends_on('libunwind@1.4: +xz+pic')
    depends_on('mbedtls+pic')
    depends_on('meson@0.57:')
    depends_on('pkgconf', type='build')
    depends_on('xerces-c transcoder=iconv')
    depends_on('xz+pic', type='link')
    depends_on('zlib+shared')

    depends_on('cuda', when='+cuda')
    depends_on('intel-xed', when='target=x86_64:')
    depends_on('memkind', type=('build', 'run'), when='@2021.05.01:')
    depends_on('papi', when='+papi')
    depends_on('libpfm4', when='~papi')
    depends_on('mpi', when='+mpi')
    depends_on('hpcviewer', type='run', when='+viewer')

    depends_on('hip', when='+rocm')
    depends_on('rocm-dbgapi', when='+rocm')
    depends_on('roctracer-dev', when='+rocm')

    conflicts('%gcc@:4.7', when='^dyninst@10.0.0:',
              msg='hpctoolkit requires gnu gcc 4.8.x or later')

    conflicts('%gcc@:4', when='@2020.03:2020',
              msg='hpctoolkit requires gnu gcc 5.x or later')

    conflicts('%gcc@:6', when='@2021.00:',
              msg='hpctoolkit requires gnu gcc 7.x or later')

    conflicts('+cuda', when='@:2019',
              msg='cuda requires 2020.03.01 or later')

    conflicts('+rocm', when='@:2020',
              msg='rocm requires 2021.03.01 or later')

    conflicts('^binutils@2.35:2.35.1',
              msg='avoid binutils 2.35 and 2.35.1 (spews errors)')

    # Fix the build for old revs with gcc 10.x.
    patch('gcc10-enum.patch', when='@2020.01.01:2020.08 %gcc@10.0:')

    patch('https://github.com/HPCToolkit/hpctoolkit/commit/511afd95b01d743edc5940c84e0079f462b2c23e.patch',
          sha256='fd0fd7419f66a1feba8046cff9df7f27abce8629ee2708b8a9daa12c1b51243c',
          when='@2019.08.01:2021.03 %gcc@11.0:')

    def meson_args(self):
      args = [
        '-Dhpcrun=enabled', '-Dhpclink=enabled', '-Dhpcstruct=enabled',
        '-Dhpcstruct=enabled',
        '-Dcuda-monitoring=%s' % ('enabled' if '+cuda' in self.spec else 'disabled'),
        '-Dmpi=%s' % ('enabled' if '+mpi' in self.spec else 'disabled'),
        '-Dversion_spack_spec=%s' % self.spec.format('{@version} {variants} {/hash:7} {%compiler.name}{@compiler.version}'),
      ]
      return args

    # We only want hpctoolkit and hpcviewer paths and man paths in the
    # module file.  The run dependencies are all curried into hpctoolkit
    # and we don't want to risk exposing a package if the application
    # uses a different version of the same package.
    def setup_run_environment(self, env):
        spec = self.spec
        env.clear()
        env.prepend_path('PATH', spec.prefix.bin)
        env.prepend_path('MANPATH', spec.prefix.share.man)
        if '+viewer' in spec:
            env.prepend_path('PATH', spec['hpcviewer'].prefix.bin)
            env.prepend_path('MANPATH', spec['hpcviewer'].prefix.share.man)
