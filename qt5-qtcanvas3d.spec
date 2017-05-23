#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtcanvas3d
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Canvas 3D module
Summary(pl.UTF-8):	Moduł Qt5 Canvas 3D
Name:		qt5-%{orgname}
Version:	5.8.0
Release:	1
License:	LGPL v3 or GPL v2+ or commercial
Group:		X11/Libraries
Source0:	http://download.qt.io/official_releases/qt/5.8/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	94d6e0141711d3660e2872fbb051da5e
URL:		http://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5OpenGL-devel >= %{qtbase_ver}
BuildRequires:	Qt5OpenGLExtensions-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	pkgconfig
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Canvas 3D module.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera moduł Qt5 Canvas 3D.

%package -n Qt5Qml-module-QtCanvas3D
Summary:	The Qt5 Canvas 3D module
Summary(pl.UTF-8):	Moduł Qt5 Canvas 3D
Group:		X11/Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5OpenGL >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}

%description -n Qt5Qml-module-QtCanvas3D
Qt5 Canvas 3D module provides a way to make OpenGL-like 3D drawing
calls from Qt Quick JavaScript.

%description -n Qt5Qml-module-QtCanvas3D -l pl.UTF-8
Moduł Qt5 Canvas 3D daje możliwość wywoływania funkcji rysujących 3D
podobnych do OpenGL z poziomu JavaScriptu Qt Quick.

%package doc
Summary:	Qt5 Canvas 3D documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do modułu Qt5 Canvas 3D w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 Canvas 3D documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do modułu Qt5 Canvas 3D w formacie HTML.

%package doc-qch
Summary:	Qt5 Canvas 3D documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do modułu Qt5 Canvas 3D w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 Canvas 3D documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do modułu Qt5 Canvas 3D w formacie QCH.

%package examples
Summary:	Qt5 Canvas 3D examples
Summary(pl.UTF-8):	Przykłady do modułu Qt5 Canvas 3D
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Qt5 Canvas 3D examples.

%description examples -l pl.UTF-8
Przykłady do modułu Qt5 Canvas 3D.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/canvas3d

%clean
rm -rf $RPM_BUILD_ROOT

%files -n Qt5Qml-module-QtCanvas3D
%defattr(644,root,root,755)
%dir %{qt5dir}/qml/QtCanvas3D
%attr(755,root,root) %{qt5dir}/qml/QtCanvas3D/libqtcanvas3d.so
%{qt5dir}/qml/QtCanvas3D/plugins.qmltypes
%{qt5dir}/qml/QtCanvas3D/qmldir

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtcanvas3d

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtcanvas3d.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
