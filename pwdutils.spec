# TODO: review default login.defs
#
# Conditional build:
%bcond_without	ldap		# build without LDAP support
%bcond_without	selinux		# build without SELinux support
#
Summary:	Utilities to manage the passwd and shadow user information
Summary(pl):	Narzêdzia do zarz±dzania informacjami o u¿ytkownikach z passwd i shadow
Name:		pwdutils
Version:	3.0
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2
# Source0-md5:	be954620dfb8f2b36b398d7d4742d205
Source1:	%{name}.useradd
Source2:	%{name}.rpasswdd.init
Source3:	%{name}.login.defs
Source4:	chage.pamd
Source5:	chfn.pamd
Source6:	chsh.pamd
Source7:	passwd.pamd
Source8:	useradd.pamd
Source9:	userdb.pamd
Patch0:		%{name}-f-option.patch
Patch1:		%{name}-pl.po-update.patch
Patch2:		%{name}-no_bash.patch
Patch3:		%{name}-silent_crontab.patch
URL:		http://www.thkukuk.de/pam/pwdutils/
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.7
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gettext-devel
BuildRequires:	libnscd-devel
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	libtool
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	openslp-devel
BuildRequires:	pam-devel
BuildRequires:	sed >= 4.0
Provides:	shadow = 2:%{version}-%{release}
Provides:	shadow-extras = 2:%{version}-%{release}
Obsoletes:	shadow
Obsoletes:	shadow-extras
Obsoletes:	shadow-utils
Conflicts:	util-linux < 2.12-10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# for pam module in /%{_lib}/security
%define		_libdir		/%{_lib}

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
pwdutils to zestaw narzêdzi do zarz±dzania informacjami o
u¿ytkownikach z passwd i shadow. Ró¿nica w stosunku do pakietu shadow
polega na tym, ¿e te narzêdzia mog± tak¿e modyfikowaæ informacje
zapisane w bazie NIS, NIS+ lub LDAP. PAM jest u¿ywany do
uwierzytelniania u¿ytkowników i zmiany hase³. Zestaw zawiera passwd,
chage, chfn, chsh oraz demona do zmiany has³a na zdalnej maszynie po
bezpiecznym po³±czeniu SSL. Demon tak¿e u¿ywa PAM, wiêc mo¿na zmieniaæ
has³a niezale¿nie od tego, gdzie s± przechowywane.

%package -n rpasswdd
Summary:	Remote password update daemon
Summary(pl):	Demon do zdalnego uaktualniania hase³
Group:		Applications/System
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig

%description -n rpasswdd
rpasswdd is a daemon that lets users change their passwords in the
presence of a directory service like NIS, NIS+ or LDAP over a secure
SSL connection. rpasswdd behaves like the normal passwd(1) program and
uses PAM for authentication and changing the password, so it can be
configured very flexibel for the local requirements.

%description -n rpasswdd -l pl
rpasswdd to demon pozwalaj±cy u¿ytkownikom zmieniaæ has³a w obecno¶ci
us³ug katalogowych takich jak NIS, NIS+ czy LDAP po bezpiecznym
po³±czeniu SSL. rpasswdd zachowuje siê tak, jak normalny program
passwd(1) i u¿ywam PAM do uwierzytelniania i zmiany hase³, wiêc mo¿e
byæ bardzo elastycznie konfigurowany dla lokalnych wymagañ.

%package -n pam-pam_rpasswd
Summary:	pam_rpasswd - PAM module to change remote password
Summary(pl):	pam_rpasswd - modu³ PAM do zdalnej zmiany has³a
Group:		Base
# rpasswd.conf is in base
Requires:	%{name} = %{version}-%{release}

%description -n pam-pam_rpasswd
The pam_rpasswd PAM module is for changing the password of user
accounts on a remote server over a secure SSL connection. It only
provides functionality for one PAM management group: password
changing.

%description -n pam-pam_rpasswd -l pl
Modu³ PAM pam_rpasswd s³u¿y do zmiany hase³ dla kont u¿ytkowników na
zdalnym serwerze po bezpiecznym po³±czeniu SSL. Udostêpnia
funkcjonalno¶æ tylko dla jednej grupy zarz±dzania PAM: zmiany hase³.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

rm -f po/stamp-po

sed -i -e 's/-Werror //' configure.in

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-pam_rpasswd \
	--%{?with_selinux:en}%{!?with_selinux:dis}able-selinux \
	--enable-slp \
	--enable-ssl \
	--%{?with_ldap:en}%{!?with_ldap:dis}able-ldap \
	--enable-nls \
	--disable-rpath
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,pwdutils,security,skel}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_sbindir}/*.local $RPM_BUILD_ROOT%{_sysconfdir}/pwdutils
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/default/useradd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/rpasswdd
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/login.defs

install %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/chage
install %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/chfn
install %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/chsh
install %{SOURCE7} $RPM_BUILD_ROOT/etc/pam.d/passwd
install %{SOURCE8} $RPM_BUILD_ROOT/etc/pam.d/useradd
install %{SOURCE9} $RPM_BUILD_ROOT/etc/pam.d/shadow

rm -f $RPM_BUILD_ROOT%{_libdir}/pwdutils/*.{la,a}

:> $RPM_BUILD_ROOT%{_sysconfdir}/shadow
:> $RPM_BUILD_ROOT/etc/security/chfn.allow
:> $RPM_BUILD_ROOT/etc/security/chsh.allow

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
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %ghost %{_sysconfdir}/shadow
%attr(750,root,root) %dir %{_sysconfdir}/default
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default/*
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.local
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/logging
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/chage
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/chfn
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/chsh
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/passwd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/useradd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/shadow
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/login.defs
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/rpasswd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/chfn.allow
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/chsh.allow
%dir /etc/skel
%attr(755,root,root) %{_bindir}/chage
%attr(4755,root,root) %{_bindir}/chfn
%attr(4755,root,root) %{_bindir}/chsh
%attr(4755,root,root) %{_bindir}/expiry
%attr(4755,root,root) %{_bindir}/gpasswd
%attr(755,root,root) %{_bindir}/newgrp
%attr(4755,root,root) %{_bindir}/passwd
%attr(755,root,root) %{_bindir}/rpasswd
%attr(755,root,root) %{_bindir}/sg
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
%dir %{_libdir}/pwdutils
%attr(755,root,root) %{_libdir}/pwdutils/liblog_syslog.so*
%{_mandir}/man?/*
%exclude %{_mandir}/man8/rpasswdd.8*
%exclude %{_mandir}/man8/pam_rpasswd.8*

%files -n rpasswdd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/rpasswdd
%attr(754,root,root) /etc/rc.d/init.d/rpasswdd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/rpasswd
%{_mandir}/man8/rpasswdd.8*

%files -n pam-pam_rpasswd
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_rpasswd.so
%{_mandir}/man8/pam_rpasswd.8*
