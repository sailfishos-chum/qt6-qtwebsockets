%global  qt_version 6.7.2

Summary: Qt6 - WebSockets component
Name:    qt6-qtwebsockets
Version: 6.7.2
Release: 0%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://qt-project.org/
Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_qt6_archdatadir}/qml/.*\\.so$

BuildRequires: cmake
BuildRequires: clang
BuildRequires: ninja
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-devel >= %{qt_version}
BuildRequires: qt6-qtbase-private-devel
#libQt6Core.so.6(Qt_5_PRIVATE_API)(64bit)
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: pkgconfig(xkbcommon) >= 0.5.0
BuildRequires: openssl-devel

%description
The QtWebSockets module implements the WebSocket protocol as specified in RFC
6455. It solely depends on Qt (no external dependencies).

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=OFF \
  -DQT_INSTALL_EXAMPLES_SOURCES=OFF

%cmake_build


%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/*
%{_qt6_libdir}/libQt6WebSockets.so.6*

%files devel
%{_qt6_headerdir}/QtWebSockets/
%{_qt6_libdir}/libQt6WebSockets.so
%{_qt6_libdir}/libQt6WebSockets.prl
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWebSocketsTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6WebSockets/
%{_qt6_libdir}/cmake/Qt6WebSockets/*.cmake
%{_qt6_libdir}/qt6/qml/QtWebSockets/
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_websockets*.pri
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc
