%define		realname	SDL
Summary:	SDL (Simple DirectMedia Layer) - Game/Multimedia Library
Summary(es):	Simple DirectMedia Layer
Summary(pl):	SDL (Simple DirectMedia Layer) - Biblioteka do gier/multimediów
Summary(pt_BR):	Simple DirectMedia Layer
Summary(ru):	Simple DirectMedia Layer
Summary(uk):	Simple DirectMedia Layer
Summary(zh_CN):	SDL (Simple DirectMedia Layer) Generic APIs - ÓÎÏ·/¶àÃ½Ìå¿â
Name:		crossmingw32-%{realname}
Version:	1.2.7
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://www.libsdl.org/cvs/SDL-1.2.tar.gz
# Source0-md5:	a925e42b258eb25d0041bd88d5704e8f
Patch0:		%{realname}-byteorder.patch
Patch1:		%{realname}-fixlibs.patch
Patch2:		%{realname}-amfix.patch
Patch3:		%{realname}-lpthread.patch
Patch4:		%{realname}-ac25x.patch
Patch5:		%{realname}-no_rpath_in_sdl-config.patch
URL:		http://www.libsdl.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
BuildRequires:	crossmingw32-w32api-dx
BuildRequires:	libtool >= 2:1.4d
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	perl-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%description
SDL (Simple DirectMedia Layer) is a library that allows you portable,
low level access to a video framebuffer, audio output, mouse, and
keyboard. It can support both windowed and DGA modes of XFree86, and
it is designed to be portable - applications linked with SDL can also
be built on Win32 and BeOS.

%description -l pl
SDL (Simple DirectMedia Layer) jest bibliotek± udostêpniaj±c±
przeno¶ny, niskopoziomowy dostêp do bufora ramki video, wyj¶cia audio,
myszy oraz klawiatury. Mo¿e obs³ugiwaæ zarówno okienkowy tryb XFree86
jak i DGA. Konstruuj±c j± miano na uwadze przeno¶no¶æ: aplikacje
konsolidowane z SDL mo¿na równie¿ budowaæ w systemach Win32 i BeOS.

%description -l pt_BR
Esse é o Simple DirectMedia Layer, uma API genérica que dá acesso de
baixo nível a áudio, teclado, mouse e vídeo em várias plataformas.

Essa biblioteca é usada por alguns jogos.

%package dll
Summary:	SDL - DLL library for Windows
Summary(pl):	SDL - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
SDL - DLL library for Windows.

%description dll -l pl
SDL - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-1.2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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
	-e 's@libdirs="-L/usr/lib"@libdirs="-L%{arch}/lib"@' > sdl.new
mv -f sdl.new sdl-config

%{target}-strip src/.libs/SDL.dll

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{bin,include/SDL,lib}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install include/*.h $RPM_BUILD_ROOT%{arch}/include/SDL
install sdl-config $RPM_BUILD_ROOT%{arch}/bin/sdl-config
install src/.libs/libSDL{,.dll}.a src/main/libSDLmain.a $RPM_BUILD_ROOT%{arch}/lib
install src/.libs/SDL.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system/

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
