# Install script for directory: /seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/lib/libsim_ana.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/lib/libsim_ana.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/lib/libsim_ana.so"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/lib/libsim_ana.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/lib" TYPE SHARED_LIBRARY FILES "/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/work/libsim_ana.so")
  if(EXISTS "$ENV{DESTDIR}/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/lib/libsim_ana.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/lib/libsim_ana.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/lib/libsim_ana.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/include/DoEmbedding.h;/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/include/SimAna.h")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/install/include" TYPE FILE FILES
    "/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/src/DoEmbedding.h"
    "/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/src/SimAna.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest/e1039-analysis/SimHits/work/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
