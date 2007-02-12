%define		realname	SDL
Summary:	SDL (Simple DirectMedia Layer) - Game/Multimedia Library - Mingw32 cross version
Summary(pl.UTF-8):	SDL (Simple DirectMedia Layer) - Biblioteka do gier/multimediów - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	1.2.11
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.libsdl.org/release/%{realname}-%{version}.tar.gz
# Source0-md5:	418b42956b7cd103bfab1b9077ccc149
Patch0:		%{realname}-mmx-constraints.patch
Patch1:		%{realname}-acfix.patch
URL:		http://www.libsdl.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-runtime
BuildRequires:	crossmingw32-w32api
BuildRequires:	crossmingw32-w32api-dx
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	nasm
BuildRequires:	perl-modules
BuildConflicts:	crossmingw32-dx70
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
# alpha's -mieee and sparc's -mtune=* are not valid for target's gcc
%define		optflags	-O2
%endif

%description
SDL (Simple DirectMedia Layer) is a library that allows you portable,
low level access to a video framebuffer, audio output, mouse, and
keyboard. It can support both windowed and DGA modes of XFree86, and
it is designed to be portable - applications linked with SDL can also
be built on Win32 and BeOS.

%description -l pl.UTF-8
SDL (Simple DirectMedia Layer) jest biblioteką udostępniającą
przenośny, niskopoziomowy dostęp do bufora ramki video, wyjścia audio,
myszy oraz klawiatury. Może obsługiwać zarówno okienkowy tryb XFree86
jak i DGA. Konstruując ją miano na uwadze przenośność: aplikacje
konsolidowane z SDL można również budować w systemach Win32 i BeOS.

%description -l pt_BR.UTF-8
Esse é o Simple DirectMedia Layer, uma API genérica que dá acesso de
baixo nível a áudio, teclado, mouse e vídeo em várias plataformas.

Essa biblioteca é usada por alguns jogos.

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
%patch1 -p1

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

./autogen.sh
%configure \
	--target=%{target} \
	--host=%{target} \
	--build=i386-linux \
%ifarch %{ix86}
	--enable-nasm \
%else
	--disable-nasm \
%endif
	--prefix=%{arch} \
	--disable-stdio-redirect

%{__make}

cat sdl-config | sed -e 's@-I/usr/include/SDL@-I%{arch}/include/SDL@' \
	-e 's@ -L/usr/lib @ -L%{arch}/lib @' > sdl.new
mv -f sdl.new sdl-config

%if 0%{!?debug:1}
%{target}-strip build/.libs/SDL.dll
#%{target}-strip -g -R.comment -R.note build/.libs/*.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{bin,include/SDL,lib}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install include/*.h $RPM_BUILD_ROOT%{arch}/include/SDL
install sdl-config $RPM_BUILD_ROOT%{arch}/bin/sdl-config
install build/.libs/libSDL{,.dll}.a build/libSDLmain.a $RPM_BUILD_ROOT%{arch}/lib
install build/.libs/SDL.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

ln -s %{arch}/bin/sdl-config $RPM_BUILD_ROOT%{_bindir}/%{target}-sdl-config

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{arch}/bin/*
%{arch}/include/SDL
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
