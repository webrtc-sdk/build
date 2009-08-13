# Copyright (c) 2009 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    # .gyp files should set chromium_code to 1 if they build Chromium-specific
    # code, as opposed to external code.  This variable is used to control
    # such things as the set of warnings to enable, and whether warnings are
    # treated as errors.
    'chromium_code%': 0,

    # Variables expected to be overriden on the GYP command line (-D) or by
    # ~/.gyp/include.gypi.

    # Putting a variables dict inside another variables dict looks kind of
    # weird.  This is done so that "branding" and "buildtype" are defined as
    # variables within the outer variables dict here.  This is necessary
    # to get these variables defined for the conditions within this variables
    # dict that operate on these variables.
    'variables': {
      # Override branding to select the desired branding flavor.
      'branding%': 'Chromium',

      # Override buildtype to select the desired build flavor.
      # Dev - everyday build for development/testing
      # Official - release build (generally implies additional processing)
      # TODO(mmoss) Once 'buildtype' is fully supported (e.g. Windows gyp
      # conversion is done), some of the things which are now controlled by
      # 'branding', such as symbol generation, will need to be refactored based
      # on 'buildtype' (i.e. we don't care about saving symbols for non-Official
      # builds).
      'buildtype%': 'Dev',
    },

    # Define branding and buildtype on the basis of their settings within the
    # variables sub-dict above, unless overridden.
    'branding%': '<(branding)',
    'buildtype%': '<(buildtype)',

    # Override chromium_mac_pch and set it to 0 to suppress the use of
    # precompiled headers on the Mac.  Prefix header injection may still be
    # used, but prefix headers will not be precompiled.  This is useful when
    # using distcc to distribute a build to compile slaves that don't
    # share the same compiler executable as the system driving the compilation,
    # because precompiled headers rely on pointers into a specific compiler
    # executable's image.  Setting this to 0 is needed to use an experimental
    # Linux-Mac cross compiler distcc farm.
    'chromium_mac_pch%': 1,

    # Set to 1 to enable code coverage.  In addition to build changes
    # (e.g. extra CFLAGS), also creates a new target in the src/chrome
    # project file called "coverage".
    # Currently ignored on Windows.
    'coverage%': 0,

    # Overridable specification for potential use of alternative
    # JavaScript engines.
    'javascript_engine%': 'v8',

    # To do a shared build on linux we need to be able to choose between type
    # static_library and shared_library. We default to doing a static build
    # but you can override this with "gyp -Dlibrary=shared_library" or you
    # can add the following line (without the #) to ~/.gyp/include.gypi
    # {'variables': {'library': 'shared_library'}}
    # to compile as shared by default
    'library%': 'static_library',

    # TODO(bradnelson): eliminate this when possible.
    # To allow local gyp files to prevent release.vsprops from being included.
    # Yes(1) means include release.vsprops.
    # Once all vsprops settings are migrated into gyp, this can go away.
    'msvs_use_common_release%': 1,

    # TODO(bradnelson): eliminate this when possible.    
    # To allow local gyp files to override additional linker options for msvs. 
    # Yes(1) means set use the common linker options.        
    'msvs_use_common_linker_extras%': 1,

    # TODO(sgk): eliminate this if possible.
    # It would be nicer to support this via a setting in 'target_defaults'
    # in chrome/app/locales/locales.gypi overriding the setting in the
    # 'Debug' configuration in the 'target_defaults' dict below,
    # but that doesn't work as we'd like.
    'msvs_debug_link_incremental%': '2',

    # The architecture that we're building on.
    'target_arch%': 'ia32',

    # By default linux does not use views. To turn on views in Linux
    # set the variable GYP_DEFINES to "toolkit_views=1", or modify
    # ~/.gyp/include.gypi .
    'toolkit_views%': 0,

    'chromeos%': 0,

    # Set the restrictions on the SUID sandbox binary.
    #  Path: only exec the hard coded chrome binary path
    #  User: only exec binaries owned by the running user.
    #
    # Developers should read
    #  http://code.google.com/p/chromium/wiki/LinuxSUIDSandboxDevelopment
    'linux_suid_sandbox_restrictions%': 'Path',

    # This is the location of the sandbox binary. Chrome looks for this before
    # running the zygote process. If found, and SUID, it will be used to
    # sandbox the zygote process and, thus, all renderer processes.
    'linux_sandbox_path%': '',

    # If |linux_suid_sandbox_restrictions|, above, is 'Path' then only a single
    # path is allowed to be exec'ed by the sandbox for security reasons. That
    # path is set here. It should be the final location of the Chromium binary
    # on the system.
    'linux_sandbox_chrome_path%': '/opt/google/chrome/chrome',

    'conditions': [
      ['OS=="mac"', {
        'conditions': [
          # mac_product_name is set to the name of the .app bundle as it should
          # appear on disk.  This duplicates data from
          # chrome/app/theme/chromium/BRANDING and
          # chrome/app/theme/google_chrome/BRANDING, but is necessary to get
          # these names into the build system.
          ['branding=="Chrome"', {
            'mac_product_name%': 'Google Chrome',
          }, { # else: branding!="Chrome"
            'mac_product_name%': 'Chromium',
          }],

          # Feature variables for enabling Mac Breakpad and Keystone auto-update
          # support.  Both features are on by default in official builds with
          # Chrome branding.
          ['branding=="Chrome" and buildtype=="Official"', {
            'mac_breakpad%': 1,
            'mac_keystone%': 1,
          }, { # else: branding!="Chrome" or buildtype!="Official"
            'mac_breakpad%': 0,
            'mac_keystone%': 0,
          }],
        ],
      }],  # OS=="mac"
      # Whether to use multiple cores to compile with visual studio. This is
      # optional because it sometimes causes corruption on VS 2005.
      # It is on by default on VS 2008 and off on VS 2005.
      ['OS=="win"', {
        'conditions': [
          ['MSVS_VERSION=="2005"', {
            'msvs_multi_core_compile%': 0,
          },{
            'msvs_multi_core_compile%': 1,
          }],
          # Don't do incremental linking for large modules on 32-bit.
          ['MSVS_OS_BITS==32', {
            'msvs_large_module_debug_link_mode%': '1',  # No
          },{
            'msvs_large_module_debug_link_mode%': '2',  # Yes
          }],
        ],
      }],
    ],
  },
  'target_defaults': {
    'conditions': [
      ['branding=="Chrome"', {
        'defines': ['GOOGLE_CHROME_BUILD'],
        'conditions': [
          ['OS=="linux"', {
            'cflags': [ '-gstabs' ],
          }],
        ],
      }, {  # else: branding!="Chrome"
        'defines': ['CHROMIUM_BUILD'],
      }],
      ['toolkit_views==1', {
        'defines': ['TOOLKIT_VIEWS=1'],
      }],
      ['chromeos==1', {
        'defines': ['OS_CHROMEOS=1'],
      }],
      ['coverage!=0', {
        'conditions': [
          ['OS=="mac"', {
            'xcode_settings': {
              'GCC_INSTRUMENT_PROGRAM_FLOW_ARCS': 'YES',  # -fprofile-arcs
              'GCC_GENERATE_TEST_COVERAGE_FILES': 'YES',  # -ftest-coverage
            },
            # Add -lgcov for executables, not for static_libraries.
            # This is a delayed conditional.
            'target_conditions': [
              ['_type=="executable"', {
                'xcode_settings': { 'OTHER_LDFLAGS': [ '-lgcov' ] },
              }],
            ],
          }],
          # Linux gyp (into scons) doesn't like target_conditions?
          # TODO(???): track down why 'target_conditions' doesn't work
          # on Linux gyp into scons like it does on Mac gyp into xcodeproj.
          ['OS=="linux"', {
            'cflags': [ '-ftest-coverage',
                        '-fprofile-arcs' ],
            'link_settings': { 'libraries': [ '-lgcov' ] },
          }],
          # Finally, for Windows, we simply turn on profiling.
          ['OS=="win"', {
            'msvs_settings': {
              'VCLinkerTool': {
                'Profile': 'true',
              },
              'VCCLCompilerTool': {
                # /Z7, not /Zi, so coverage is happyb
                'DebugInformationFormat': '1',
                'AdditionalOptions': '/Yd',
              }
            }
         }],  # OS==win
        ],  # conditions for coverage
      }],  # coverage!=0
    ],  # conditions for 'target_defaults'
    'default_configuration': 'Debug',
    'configurations': {
       # VCLinkerTool LinkIncremental values below:
       #   0 == default
       #   1 == /INCREMENTAL:NO
       #   2 == /INCREMENTAL
       # Debug links incremental, Release does not.
      'Debug': {
        'conditions': [
          [ 'OS=="mac"', {
            'xcode_settings': {
              'COPY_PHASE_STRIP': 'NO',
              'GCC_OPTIMIZATION_LEVEL': '0',  # -O0
            }
          }],
          [ 'OS=="win"', {
            'configuration_platform': 'Win32',
            'msvs_configuration_attributes': {
              'OutputDirectory': '$(SolutionDir)$(ConfigurationName)',
              'IntermediateDirectory': '$(OutDir)\\obj\\$(ProjectName)',
              'CharacterSet': '1',
            },
            'msvs_settings': {
              'VCCLCompilerTool': {
                'Optimization': '0',
                'PreprocessorDefinitions': ['_DEBUG'],
                'BasicRuntimeChecks': '3',
                'RuntimeLibrary': '1',
              },
              'VCLinkerTool': {
                'LinkIncremental': '<(msvs_debug_link_incremental)',
              },
              'VCResourceCompilerTool': {
                'PreprocessorDefinitions': ['_DEBUG'],
              },
            },
          }],
        ],
      },
      'Release': {
        'defines': [
          'NDEBUG',
        ],
        'conditions': [
          [ 'OS=="mac"', {
            'xcode_settings': {
              'DEAD_CODE_STRIPPING': 'YES',  # -Wl,-dead_strip
              'conditions': [
                ['mac_release_optimization != "UNSET"',
                  {'GCC_OPTIMIZATION_LEVEL': '<(mac_release_optimization)'}],
              ],
            }
          }],
          [ 'OS=="win" and msvs_use_common_release', {
            'configuration_platform': 'Win32',
            'msvs_props': ['release.vsprops'],
          }],
          [ 'OS=="win"', {
            'msvs_settings': {
              'VCLinkerTool': {
                'LinkIncremental': '1',
              },
            },
          }],
        ],
      },
      'conditions': [
        [ 'OS=="win"', {
          # TODO(bradnelson): add a gyp mechanism to make this more graceful.
          'Purify': {
            'defines': [
              'NDEBUG',
              'PURIFY',
              'NO_TCMALLOC',
            ],
            'msvs_settings': {
              'VCCLCompilerTool': {
                'Optimization': '0',
                'RuntimeLibrary': '0',
                'BufferSecurityCheck': 'false',
              },
              'VCLinkerTool': {
                'EnableCOMDATFolding': '1',
                'LinkIncremental': '1',
              },
            },
            'conditions': [
              [ 'msvs_use_common_release', {
                'configuration_platform': 'Win32',
                'msvs_props': ['release.vsprops'],
              }],
            ],
          },
          'Release - no tcmalloc': {
            'defines': [
              'NDEBUG',
              'NO_TCMALLOC',
            ],
            'conditions': [
              [ 'msvs_use_common_release', {
                'configuration_platform': 'Win32',
                'msvs_props': ['release.vsprops'],
              }],
            ],
            'msvs_settings': {
              'VCLinkerTool': {
                'LinkIncremental': '1',
              },
            },
          },
        }],
      ],
    },
  },
  'conditions': [
    ['OS=="linux"', {
      'target_defaults': {
        # Enable -Werror by default, but put it in a variable so it can
        # be disabled in ~/.gyp/include.gypi on the valgrind builders.
        'variables': {
          'werror%': '-Werror',
        },
        'cflags': [
          '<(werror)',  # See note above about the werror variable.
          '-pthread',
          '-fno-exceptions',
          '-Wall',
          '-D_FILE_OFFSET_BITS=64',
        ],
        'cflags_cc': [
          '-fno-rtti',
          '-fno-threadsafe-statics',
        ],
        'ldflags': [
          '-pthread',
        ],
        'scons_variable_settings': {
          'LIBPATH': ['$LIB_DIR'],
          # Linking of large files uses lots of RAM, so serialize links
          # using the handy flock command from util-linux.
          'FLOCK_LINK': ['flock', '$TOP_BUILDDIR/linker.lock', '$LINK'],
          'FLOCK_SHLINK': ['flock', '$TOP_BUILDDIR/linker.lock', '$SHLINK'],
          'FLOCK_LDMODULE': ['flock', '$TOP_BUILDDIR/linker.lock', '$LDMODULE'],

          # We have several cases where archives depend on each other in
          # a cyclic fashion.  Since the GNU linker does only a single
          # pass over the archives we surround the libraries with
          # --start-group and --end-group (aka -( and -) ). That causes
          # ld to loop over the group until no more undefined symbols
          # are found. In an ideal world we would only make groups from
          # those libraries which we knew to be in cycles. However,
          # that's tough with SCons, so we bodge it by making all the
          # archives a group by redefining the linking command here.
          #
          # TODO:  investigate whether we still have cycles that
          # require --{start,end}-group.  There has been a lot of
          # refactoring since this was first coded, which might have
          # eliminated the circular dependencies.
          #
          # Note:  $_LIBDIRFLAGS comes before ${LINK,SHLINK,LDMODULE}FLAGS
          # so that we prefer our own built libraries (e.g. -lpng) to
          # system versions of libraries that pkg-config might turn up.
          # TODO(sgk): investigate handling this not by re-ordering the
          # flags this way, but by adding a hook to use the SCons
          # ParseFlags() option on the output from pkg-config.
          'LINKCOM': [['$FLOCK_LINK', '-o', '$TARGET', '$_LIBDIRFLAGS', '$LINKFLAGS', '$SOURCES', '-Wl,--start-group', '$_LIBFLAGS', '-Wl,--end-group']],
          'SHLINKCOM': [['$FLOCK_SHLINK', '-o', '$TARGET', '$_LIBDIRFLAGS', '$SHLINKFLAGS', '$SOURCES', '-Wl,--start-group', '$_LIBFLAGS', '-Wl,--end-group']],
          'LDMODULECOM': [['$FLOCK_LDMODULE', '-o', '$TARGET', '$_LIBDIRFLAGS', '$LDMODULEFLAGS', '$SOURCES', '-Wl,--start-group', '$_LIBFLAGS', '-Wl,--end-group']],
          'IMPLICIT_COMMAND_DEPENDENCIES': 0,
          # -rpath is only used when building with shared libraries.
          'conditions': [
            [ 'library=="shared_library"', {
              'RPATH': '$LIB_DIR',
            }],
          ],
        },
        'scons_import_variables': [
          'AS',
          'CC',
          'CXX',
          'LINK',
        ],
        'scons_propagate_variables': [
          'AS',
          'CC',
          'CCACHE_DIR',
          'CXX',
          'DISTCC_DIR',
          'DISTCC_HOSTS',
          'HOME',
          'INCLUDE_SERVER_ARGS',
          'INCLUDE_SERVER_PORT',
          'LINK',
          'CHROME_BUILD_TYPE',
          'CHROMIUM_BUILD',
          'OFFICIAL_BUILD',
        ],
        'configurations': {
          'Debug': {
            'variables': {
              'debug_optimize%': '0',
            },
            'defines': [
              '_DEBUG',
            ],
            'cflags': [
              '-O<(debug_optimize)',
              '-g',
              # One can use '-gstabs' to enable building the debugging
              # information in STABS format for breakpad's dumpsyms.
            ],
            'ldflags': [
              '-rdynamic',  # Allows backtrace to resolve symbols.
            ],
          },
          'Release': {
            'variables': {
              'release_optimize%': '2',
              'release_extra_cflags%': '',
            },
            'cflags': [
              '-O<(release_optimize)',
              # Don't emit the GCC version ident directives, they just end up
              # in the .comment section taking up binary size.
              '-fno-ident',
              # Put data and code in their own sections, so that unused symbols
              # can be removed at link time with --gc-sections.
              '-fdata-sections',
              '-ffunction-sections',
              '<(release_extra_cflags)',
            ],
          },
        },
        'variants': {
          'coverage': {
            'cflags': ['-fprofile-arcs', '-ftest-coverage'],
            'ldflags': ['-fprofile-arcs'],
          },
          'profile': {
            'cflags': ['-pg', '-g'],
            'ldflags': ['-pg'],
          },
          'symbols': {
            'cflags': ['-g'],
          },
        },
        'conditions': [
          [ 'target_arch=="ia32"', {
            'asflags': [
              # Needed so that libs with .s files (e.g. libicudata.a)
              # are compatible with the general 32-bit-ness.
              '-32',
            ],
            # All floating-point computations on x87 happens in 80-bit
            # precision.  Because the C and C++ language standards allow
            # the compiler to keep the floating-point values in higher
            # precision than what's specified in the source and doing so
            # is more efficient than constantly rounding up to 64-bit or
            # 32-bit precision as specified in the source, the compiler,
            # especially in the optimized mode, tries very hard to keep
            # values in x87 floating-point stack (in 80-bit precision)
            # as long as possible. This has important side effects, that
            # the real value used in computation may change depending on
            # how the compiler did the optimization - that is, the value
            # kept in 80-bit is different than the value rounded down to
            # 64-bit or 32-bit. There are possible compiler options to make
            # this behavior consistent (e.g. -ffloat-store would keep all
            # floating-values in the memory, thus force them to be rounded
            # to its original precision) but they have significant runtime
            # performance penalty.
            #
            # -mfpmath=sse -msse2 makes the compiler use SSE instructions
            # which keep floating-point values in SSE registers in its
            # native precision (32-bit for single precision, and 64-bit for
            # double precision values). This means the floating-point value
            # used during computation does not change depending on how the
            # compiler optimized the code, since the value is always kept
            # in its specified precision.
            'conditions': [
              ['branding=="Chromium"', {
                'cflags': [
                  '-march=pentium4',
                  '-msse2',
                  '-mfpmath=sse',
                ],
              }],
            ],
            'cflags': [
              '-m32',
            ],
            'ldflags': [
              '-m32',
            ],
          }],
          ['target_arch=="arm"', {
            'conditions': [
              ['chromeos==1', {
                'cflags': [
                  '-march=armv7-a',
                  '-mtune=cortex-a8',
                  '-mfpu=vfp',
                  '-mfloat-abi=softfp',
                ],
              }],
            ],
          }],
        ],
      },
    }],
    ['OS=="mac"', {
      'target_defaults': {
        'variables': {
          # This should be 'mac_real_dsym%', but there seems to be a bug
          # with % in variables that are intended to be set to different
          # values in different targets, like this one.
          'mac_real_dsym': 0,  # Fake .dSYMs are fine in most cases.
          # Release defaults to the Xcode optimization default, this var
          # lets you force the value.
          'mac_release_optimization%': 'UNSET'
        },
        'mac_bundle': 0,
        'xcode_settings': {
          'ALWAYS_SEARCH_USER_PATHS': 'NO',
          'GCC_C_LANGUAGE_STANDARD': 'c99',         # -std=c99
          'GCC_CW_ASM_SYNTAX': 'NO',                # No -fasm-blocks
          'GCC_DYNAMIC_NO_PIC': 'NO',               # No -mdynamic-no-pic
                                                    # (Equivalent to -fPIC)
          'GCC_ENABLE_CPP_EXCEPTIONS': 'NO',        # -fno-exceptions
          'GCC_ENABLE_CPP_RTTI': 'NO',              # -fno-rtti
          'GCC_ENABLE_PASCAL_STRINGS': 'NO',        # No -mpascal-strings
          'GCC_INLINES_ARE_PRIVATE_EXTERN': 'YES',  # -fvisibility-inlines-hidden
          'GCC_OBJC_CALL_CXX_CDTORS': 'YES',        # -fobjc-call-cxx-cdtors
          'GCC_SYMBOLS_PRIVATE_EXTERN': 'YES',      # -fvisibility=hidden
          'GCC_THREADSAFE_STATICS': 'NO',           # -fno-threadsafe-statics
          'GCC_TREAT_WARNINGS_AS_ERRORS': 'YES',    # -Werror
          'GCC_VERSION': '4.2',
          'GCC_WARN_ABOUT_MISSING_NEWLINE': 'YES',  # -Wnewline-eof
          'MACOSX_DEPLOYMENT_TARGET': '10.5',       # -mmacosx-version-min=10.5
          'PREBINDING': 'NO',                       # No -Wl,-prebind
          'SDKROOT': 'macosx10.5',                  # -isysroot
          'USE_HEADERMAP': 'NO',
          'WARNING_CFLAGS': ['-Wall', '-Wendif-labels'],
          'conditions': [
            ['chromium_mac_pch', {'GCC_PRECOMPILE_PREFIX_HEADER': 'YES'},
                                 {'GCC_PRECOMPILE_PREFIX_HEADER': 'NO'}],
          ],
        },
        'target_conditions': [
          ['_type!="static_library"', {
            'xcode_settings': {'OTHER_LDFLAGS': ['-Wl,-search_paths_first']},
          }],
          ['_mac_bundle', {
            'xcode_settings': {'OTHER_LDFLAGS': ['-Wl,-ObjC']},
          }],
          ['_type=="executable" or _type=="shared_library"', {
            'target_conditions': [
              ['mac_real_dsym == 1', {
                # To get a real .dSYM bundle produced by dsymutil, set the
                # debug information format to dwarf-with-dsym.  Since
                # strip_from_xcode will not be used, set Xcode to do the
                # stripping as well.
                'configurations': {
                  'Release': {
                    'xcode_settings': {
                      'DEBUG_INFORMATION_FORMAT': 'dwarf-with-dsym',
                      'DEPLOYMENT_POSTPROCESSING': 'YES',
                      'STRIP_INSTALLED_PRODUCT': 'YES',
                      'target_conditions': [
                        ['_type=="shared_library"', {
                          # The Xcode default is to strip debugging symbols
                          # only (-S).  Local symbols should be stripped as
                          # well, which will be handled by -x.  Xcode will
                          # continue to insert -S when stripping even when
                          # additional flags are added with STRIPFLAGS.
                          'STRIPFLAGS': '-x',
                        }],  # _type=="shared_library"
                      ],  # target_conditions
                    },  # xcode_settings
                  },  # configuration "Release"
                },  # configurations
              }, {  # mac_real_dsym != 1
                # To get a fast fake .dSYM bundle, use a post-build step to
                # produce the .dSYM and strip the executable.  strip_from_xcode
                # only operates in the Release configuration.
                'postbuilds': [
                  {
                    'variables': {
                      # Define strip_from_xcode in a variable ending in _path
                      # so that gyp understands it's a path and performs proper
                      # relativization during dict merging.
                      'strip_from_xcode_path': 'mac/strip_from_xcode',
                    },
                    'postbuild_name': 'Strip If Needed',
                    'action': ['<(strip_from_xcode_path)'],
                  },
                ],  # postbuilds
              }],  # mac_real_dsym
            ],  # target_conditions
          }],  # _type=="executable" or _type=="shared_library"
        ],  # target_conditions
      },  # target_defaults
    }],  # OS=="mac"
    ['OS=="win"', {
      'target_defaults': {
        'defines': [
          '_WIN32_WINNT=0x0600',
          'WINVER=0x0600',
          'WIN32',
          '_WINDOWS',
          '_HAS_EXCEPTIONS=0',
          'NOMINMAX',
          '_CRT_RAND_S',
          'CERT_CHAIN_PARA_HAS_EXTRA_FIELDS',
          'WIN32_LEAN_AND_MEAN',
          '_SECURE_ATL',
          '_HAS_TR1=0',
        ],
        'msvs_system_include_dirs': [
          '<(DEPTH)/third_party/platformsdk_win2008_6_1/files/Include',
          '$(VSInstallDir)/VC/atlmfc/include',
        ],
        'msvs_cygwin_dirs': ['../third_party/cygwin'],
        'msvs_disabled_warnings': [4396, 4503, 4819],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'MinimalRebuild': 'false',
            'ExceptionHandling': '0',
            'BufferSecurityCheck': 'true',
            'EnableFunctionLevelLinking': 'true',
            'RuntimeTypeInfo': 'false',
            'WarningLevel': '3',
            'WarnAsError': 'true',
            'DebugInformationFormat': '3',
            'conditions': [
              [ 'msvs_multi_core_compile', {
                'AdditionalOptions': '/MP',
              }],
            ],
          },
          'VCLibrarianTool': {
            'AdditionalOptions': '/ignore:4221',
            'AdditionalLibraryDirectories':
              ['<(DEPTH)/third_party/platformsdk_win2008_6_1/files/Lib'],
          },
          'VCLinkerTool': {
            'AdditionalDependencies': [
              'wininet.lib',
              'version.lib',
              'msimg32.lib',
              'ws2_32.lib',
              'usp10.lib',
              'psapi.lib',
              'dbghelp.lib',
            ],
            'AdditionalLibraryDirectories':
              ['<(DEPTH)/third_party/platformsdk_win2008_6_1/files/Lib'],
            'GenerateDebugInformation': 'true',
            'MapFileName': '$(OutDir)\\$(TargetName).map',
            'ImportLibrary': '$(OutDir)\\lib\\$(TargetName).lib',
            'TargetMachine': '1',
            'FixedBaseAddress': '1',
            # SubSystem values:
            #   0 == not set
            #   1 == /SUBSYSTEM:CONSOLE
            #   2 == /SUBSYSTEM:WINDOWS
            # Most of the executables we'll ever create are tests
            # and utilities with console output.
            'SubSystem': '1',
          },
          'VCMIDLTool': {
            'GenerateStublessProxies': 'true',
            'TypeLibraryName': '$(InputName).tlb',
            'OutputDirectory': '$(IntDir)',
            'HeaderFileName': '$(InputName).h',
            'DLLDataFileName': 'dlldata.c',
            'InterfaceIdentifierFileName': '$(InputName)_i.c',
            'ProxyFileName': '$(InputName)_p.c',
          },
          'VCResourceCompilerTool': {
            'Culture' : '1033',
            'AdditionalIncludeDirectories': ['<(DEPTH)'],
          },
        },
      },
    }],
    ['chromium_code==0', {
      # This section must follow the other conditon sections above because
      # external_code.gypi expects to be merged into those settings.
      'includes': [
        'external_code.gypi',
      ],
    }, {
      'target_defaults': {
        # In Chromium code, we define __STDC_FORMAT_MACROS in order to get the
        # C99 macros on Mac and Linux.
        'defines': [
          '__STDC_FORMAT_MACROS',
        ],
      },
    }],
    ['msvs_use_common_linker_extras', {
      'target_defaults': {
        'msvs_settings': {
          'VCLinkerTool': {
            'AdditionalOptions':
              '/safeseh /dynamicbase /ignore:4199 /ignore:4221 /nxcompat',
            'DelayLoadDLLs': [
              'dbghelp.dll',
              'dwmapi.dll',
              'uxtheme.dll',
            ],
          },
        },
      },
    }],
  ],
  'scons_settings': {
    'sconsbuild_dir': '<(DEPTH)/sconsbuild',
    'tools': ['ar', 'as', 'gcc', 'g++', 'gnulink', 'chromium_builders'],
  },
  'xcode_settings': {
    # The Xcode generator will look for an xcode_settings section at the root
    # of each dict and use it to apply settings on a file-wide basis.  Most
    # settings should not be here, they should be in target-specific
    # xcode_settings sections, or better yet, should use non-Xcode-specific
    # settings in target dicts.  SYMROOT is a special case, because many other
    # Xcode variables depend on it, including variables such as
    # PROJECT_DERIVED_FILE_DIR.  When a source group corresponding to something
    # like PROJECT_DERIVED_FILE_DIR is added to a project, in order for the
    # files to appear (when present) in the UI as actual files and not red
    # red "missing file" proxies, the correct path to PROJECT_DERIVED_FILE_DIR,
    # and therefore SYMROOT, needs to be set at the project level.
    'SYMROOT': '<(DEPTH)/xcodebuild',
  },
}
