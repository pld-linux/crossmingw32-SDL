%define		realname	SDL
Summary:	SDL (Simple DirectMedia Layer) - Game/Multimedia Library - MinGW32 cross version
Summary(pl.UTF-8):	SDL (Simple DirectMedia Layer) - Biblioteka do gier/multimediów - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	1.2.15
Release:	3
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.libsdl.org/release/%{realname}-%{version}.tar.gz
# Source0-md5:	9d96df8417572a2afb781a7c4c811a85
Patch0:		%{realname}-acfix.patch
URL:		http://www.libsdl.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-runtime
BuildRequires:	crossmingw32-w32api
BuildRequires:	crossmingw32-w32api-dx
BuildRequires:	libtool >= 2:2.0
BuildRequires:	nasm
BuildRequires:	perl-modules
BuildConflicts:	crossmingw32-dx70
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*
%define		filterout_cxx	-f[-a-z0-9=]*

%description
SDL (Simple DirectMedia Layer) is a library that allows you portable,
low level access to a video framebuffer, audio output, mouse, and
keyboard. It can support both windowed and DGA modes of XFree86, and
it is designed to be portable - applications linked with SDL can also
be built on Win32 and BeOS.

This package contains the cross version for Win32.

%description -l pl.UTF-8
SDL (Simple DirectMedia Layer) jest biblioteką udostępniającą
przenośny, niskopoziomowy dostęp do bufora ramki video, wyjścia audio,
myszy oraz klawiatury. Może obsługiwać zarówno okienkowy tryb XFree86
jak i DGA. Konstruując ją miano na uwadze przenośność: aplikacje
konsolidowane z SDL można również budować w systemach Win32 i BeOS.

Ten pakiet zawiera wersję skrośną dla Win32.

%description -l pt_BR.UTF-8
Esse é o Simple DirectMedia Layer, uma API genérica que dá acesso de
baixo nível a áudio, teclado, mouse e vídeo em várias plataformas.

Essa biblioteca é usada por alguns jogos.

%package static
Summary:	Static SDL library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka SDL (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static SDL library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka SDL (wersja skrośna MinGW32).

%package dll
Summary:	SDL - DLL library for Windows
Summary(pl.UTF-8):	SDL - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
SDL - DLL library for Windows.

%description dll -l pl.UTF-8
SDL - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1

: > acinclude.m4
echo 'AC_DEFUN([AM_PATH_ESD],[$3])' >> acinclude.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--target=%{target} \
	--host=%{target} \
	--enable-nasm \
	--disable-stdio-redirect

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_dlldir},%{_sysprefix}/bin}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}
ln -s %{_bindir}/sdl-config $RPM_BUILD_ROOT%{_sysprefix}/bin/%{target}-sdl-config

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{aclocal,man}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS CREDITS README README-SDL.txt TODO WhatsNew
%attr(755,root,root) %{_sysprefix}/bin/%{target}-sdl-config
%attr(755,root,root) %{_bindir}/sdl-config
%{_libdir}/libSDL.dll.a
%{_libdir}/libSDL.la
%{_libdir}/libSDLmain.a
%{_libdir}/libSDLmain.la
%{_includedir}/SDL
%{_pkgconfigdir}/sdl.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libSDL.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libSDL-1-2-0.dll
