#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	UI accessibility infrastructure (C API library)
Summary(pl.UTF-8):	Infrastruktura dostępności UI (biblioteka API dla języka C)
Name:		accesskit-c
# gtk4 4.22 expects 0.18.x
Version:	0.18.0
Release:	1
License:	Apache v2.0 or MIT, BSD
Group:		Libraries
#Source0Download: https://github.com/AccessKit/accesskit-c/releases
Source0:	https://github.com/AccessKit/accesskit-c/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	84e24c109ff702aa971ece9108bb470a
# cargo vendor-filterer --platform='*-unknown-linux-*' --tier=2
Source1:	%{name}-%{version}-vendor.tar.xz
# Source1-md5:	fa1d4ca2423264a17a13ece851331df9
URL:		https://github.com/AccessKit/accesskit-c
BuildRequires:	cargo
BuildRequires:	meson >= 1.3.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust >= 1.77.2
%{?rust_req}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bindings to use AccessKit from other languages through FFI such as in
C.

%description -l pl.UTF-8
Wiązania do używania biblioteki AccessKit z innych języków porrzez
FFI, jak w C.

%package devel
Summary:	UI accessibility infrastructure (C API)
Summary(pl.UTF-8):	Infrastruktura dostępności UI (API dla języka C)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
UI accessibility infrastructure (C API).

%description devel -l pl.UTF-8
Infrastruktura dostępności UI (API dla języka C).

%package static
Summary:	UI accessibility infrastructure (C API static library)
Summary(pl.UTF-8):	Infrastruktura dostępności UI (biblioteka statyczna API dla języka C)
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
UI accessibility infrastructure (C API static library).

%description static -l pl.UTF-8
Infrastruktura dostępności UI (biblioteka statyczna API dla języka C).

%prep
%setup -q -a1

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config.toml <<EOF
[source.crates-io]
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"
export PKG_CONFIG_ALLOW_CROSS=1

%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Dtriplet=%{rust_target}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

export CARGO_HOME="$(pwd)/.cargo"
export PKG_CONFIG_ALLOW_CROSS=1

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md LICENSE-MIT LICENSE.chromium README.md
%{_libdir}/libaccesskit-c-0.18.so.*.*.*
%ghost %{_libdir}/libaccesskit-c-0.18.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libaccesskit-c-0.18.so
%{_includedir}/accesskit-c-0.18
%{_pkgconfigdir}/accesskit-c-0.18.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libaccesskit-c-0.18.a
%endif
