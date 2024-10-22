#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.2.2
%define		qtver		5.15.2
%define		kpname		kdecoration
Summary:	A plugin-based library to create window decorations
Name:		kp6-%{kpname}
Version:	6.2.2
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	6e3eccb09e74badb352fdd763054b070
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A plugin-based library to create window decorations.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kp5-%{kpname}-devel < %{version}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libkdecorations2.so.*.*
%ghost %{_libdir}/libkdecorations2.so.6
%attr(755,root,root) %{_libdir}/libkdecorations2private.so.*.*
%ghost %{_libdir}/libkdecorations2private.so.11

%files devel
%defattr(644,root,root,755)
%{_libdir}/libkdecorations2.so
%{_libdir}/libkdecorations2private.so
%{_includedir}/KDecoration2
%{_includedir}/KF6/kdecoration2_version.h
%{_libdir}/cmake/KDecoration2
