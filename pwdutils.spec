Summary:	Utilities to manage the passwd and shadow user information
Summary(pl):	Narz�dzia do zarz�dzania informacjami o u�ytkownikach z passwd i shadow
Name:		pwdutils
Version:	2.6
Release:	1
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2
# Source0-md5:	8567328b1ad7609f8851eec57658f1a0
Source1:	%{name}.useradd
Source2:	%{name}.rpasswdd.init
Source3:	%{name}.login.defs
Source4:	chage.pamd
Source5:	chfn.pamd
Source6:	chsh.pamd
Source7:	passwd.pamd
Source8:	useradd.pamd
Source9:	userdb.pamd
URL:		http://www.thkukuk.de/pam/pwdutils/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gettext-devel
BuildRequires:	libselinux-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	openslp-devel
BuildRequires:	pam-devel
BuildRequires:	sed >= 4.0
Provides:	shadow = 2:%{version}-%{release}
Provides:	shadow-extras = 2:%{version}-%{release}
Obsoletes:	shadow
Obsoletes:	shadow-extras
Conflicts:	util-linux < 2.12-10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pwdutils is a collection of utilities to manage the passwd and shadow
user information. The difference to the shadow suite is that these
utilities can also modify the information stored in NIS, NIS+, or
LDAP. PAM is used for user authentication and changing the pasword. It
contains passwd, chage, chfn, chsh, and a daemon for changing the
password on a remote machine over a secure SSL connection. The daemon
also uses PAM so that it can change passwords independent of where
they are stored.

%description -l pl
pwdutils to zestaw narz�dzi do zarz�dzania informacjami o
u�ytkownikach z passwd i shadow. R�nica w stosunku do pakietu shadow
polega na tym, �e te narz�dzia mog� tak�e modyfikowa� informacje
zapisane w bazie NIS, NIS+ lub LDAP. PAM jest u�ywany do
uwierzytelniania u�ytkownik�w i zmiany hase�. Zestaw zawiera passwd,
chage, chfn, chsh oraz demona do zmiany has�a na zdalnej maszynie po
bezpiecznym po��czeniu SSL. Demon tak�e u�ywa PAM, wi�c mo�na zmienia�
has�a niezale�nie od tego, gdzie s� przechowywane.

%package -n rpasswdd
Summary:	Remote password update daemon
Summary(pl):	Demon do zdalnego uaktualniania hase�
Group:		Applications/System

%description -n rpasswdd
rpasswdd is a daemon that lets users change their passwords in the
presence of a directory service like NIS, NIS+ or LDAP over a secure
SSL connection. rpasswdd behaves like the normal passwd(1) program and
uses PAM for authentication and changing the password, so it can be
configured very flexibel for the local requirements.

%description -n rpasswdd -l pl
rpasswdd to demon pozwalaj�cy u�ytkownikom zmienia� has�a w obecno�ci
us�ug katalogowych takich jak NIS, NIS+ czy LDAP po bezpiecznym
po��czeniu SSL. rpasswdd zachowuje si� tak, jak normalny program
passwd(1) i u�ywam PAM do uwierzytelniania i zmiany hase�, wi�c mo�e
by� bardzo elastycznie konfigurowany dla lokalnych wymaga�.

%prep
%setup -q

%build
sed -i -e 's#EXTRA_CFLAGS=.*#EXTRA_CFLAGS="-W -Wall"#g' configure.in
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-pam_rpasswd \
	--enable-selinux \
	--enable-slp \
	--enable-ssl \
	--enable-ldap \
	--enable-nls \
	--disable-rpath
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d/,pwdutils,skel}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sbindir}/*.local $RPM_BUILD_ROOT%{_sysconfdir}/pwdutils
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/default/useradd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/rpasswdd
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/login.defs

install %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/chage
install %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/chfn
install %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/chsh
install %{SOURCE7} $RPM_BUILD_ROOT/etc/pam.d/passwd
install %{SOURCE8} $RPM_BUILD_ROOT/etc/pam.d/useradd
install %{SOURCE9} $RPM_BUILD_ROOT/etc/pam.d/shadow

:> $RPM_BUILD_ROOT/etc/shadow

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shadow ]; then
	%{_sbindir}/pwconv
fi

%post -n rpasswdd
/sbin/chkconfig --add rpasswdd
if [ -f /var/lock/subsys/rpasswdd ]; then
        /etc/rc.d/init.d/rpasswdd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/rpasswdd start\" to start rpasswdd daemon."
fi

%preun -n rpasswdd
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/rpasswdd ]; then
                /etc/rc.d/init.d/rpasswdd stop 1>&2
        fi
        /sbin/chkconfig --del rpasswdd
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README THANKS TODO
%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %ghost %{_sysconfdir}/shadow
%attr(750,root,root) %dir %{_sysconfdir}/default
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/default/*
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%attr(750,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}/*.local
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/chage
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/chfn
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/chsh
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/passwd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/useradd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/shadow
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/login.defs
%dir /etc/skel
%attr(755,root,root) %{_bindir}/chage
%attr(4755,root,root) %{_bindir}/chfn
%attr(4755,root,root) %{_bindir}/chsh
%attr(4755,root,root) %{_bindir}/expiry
%attr(4755,root,root) %{_bindir}/gpasswd
%attr(755,root,root) %{_bindir}/newgrp
%attr(4755,root,root) %{_bindir}/passwd
%attr(755,root,root) %{_bindir}/rpasswd
%attr(755,root,root) %{_sbindir}/chpasswd
%attr(755,root,root) %{_sbindir}/groupadd
%attr(755,root,root) %{_sbindir}/groupdel
%attr(755,root,root) %{_sbindir}/groupmod
%attr(755,root,root) %{_sbindir}/grpconv
%attr(755,root,root) %{_sbindir}/grpck
%attr(755,root,root) %{_sbindir}/grpunconv
%attr(755,root,root) %{_sbindir}/pwconv
%attr(755,root,root) %{_sbindir}/pwck
%attr(755,root,root) %{_sbindir}/pwunconv
%attr(755,root,root) %{_sbindir}/rpasswdd
%attr(755,root,root) %{_sbindir}/useradd
%attr(755,root,root) %{_sbindir}/userdel
%attr(755,root,root) %{_sbindir}/usermod
%attr(755,root,root) %{_sbindir}/vigr
%attr(755,root,root) %{_sbindir}/vipw
%{_mandir}/man?/*
%exclude %{_mandir}/man8/rpasswdd*

%files -n rpasswdd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/rpasswdd
%attr(754,root,root) /etc/rc.d/init.d/rpasswdd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/rpasswd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/rpasswd.conf
%{_mandir}/man8/rpasswdd*
