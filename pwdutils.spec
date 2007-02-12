# TODO:
# - review default login.defs
#
# Conditional build:
%bcond_without	audit		# don't build audit log plugin
%bcond_without	ldap		# build without LDAP support
%bcond_without	selinux		# build without SELinux support
%bcond_with	bioapi		# with BioAPI support in passwd
%bcond_with	gnutls		# use GnuTLS instead of OpenSSL
#
Summary:	Utilities to manage the passwd and shadow user information
Summary(pl.UTF-8):   Narzędzia do zarządzania informacjami o użytkownikach z passwd i shadow
Name:		pwdutils
Version:	3.1.3
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2
# Source0-md5:	b18c601e282d8695cbb5ddd87eaa473c
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
Patch1:		%{name}-no_bash.patch
Patch2:		%{name}-silent_crontab.patch
Patch3:		%{name}-pl.po-update.patch
URL:		http://www.thkukuk.de/pam/pwdutils/
%{?with_audit:BuildRequires:	audit-libs-devel}
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.7
%{?with_bioapi:BuildRequires:	bioapi-devel}
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gettext-devel
%{?with_gnutls:BuildRequires:	gnutls-devel >= 1.0.0}
BuildRequires:	libnscd-devel
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	libtool
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
BuildRequires:	openslp-devel
%{!?with_gnutls:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	pam >= 0.99.7.1
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

%description -l pl.UTF-8
pwdutils to zestaw narzędzi do zarządzania informacjami o
użytkownikach z passwd i shadow. Różnica w stosunku do pakietu shadow
polega na tym, że te narzędzia mogą także modyfikować informacje
zapisane w bazie NIS, NIS+ lub LDAP. PAM jest używany do
uwierzytelniania użytkowników i zmiany haseł. Zestaw zawiera passwd,
chage, chfn, chsh oraz demona do zmiany hasła na zdalnej maszynie po
bezpiecznym połączeniu SSL. Demon także używa PAM, więc można zmieniać
hasła niezależnie od tego, gdzie są przechowywane.

%package log-audit
Summary:	audit log plugin for pwdutils
Summary(pl.UTF-8):   Wtyczka logująca audit dla pwdutils
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description log-audit
audit log plugin for pwdutils.

%description log-audit -l pl.UTF-8
Wtyczka logująca audit dla pwdutils.

%package -n rpasswd
Summary:	Remote password update client
Summary(pl.UTF-8):   Klient do zdalnego uaktualniania haseł
Group:		Applications/System

%description -n rpasswd
rpasswd changes passwords for user accounts on a remote server over a
secure SSL connection. A normal user may only change the password for
their own account, if the user knows the password of the administrator
account (in the moment this is the root password on the server), he may
change the password for any account if he calls rpasswd with the -a
option.

%description -n rpasswd -l pl.UTF-8
rpasswd pozwala zmieniać hasła użytkowników na zdalnym serwerze przy
użyciu bezpiecznego połączenia SSL. Zwykły użytkownik może zmienić
jedynie swoje hasło, a jeśli zna hasło administratora (obecnie jest to
hasło roota na serwerze), może zmienić hasło dla dowolnego konta
wywołując rpasswd z opcją -a.

%package -n rpasswdd
Summary:	Remote password update daemon
Summary(pl.UTF-8):   Demon do zdalnego uaktualniania haseł
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description -n rpasswdd
rpasswdd is a daemon that lets users change their passwords in the
presence of a directory service like NIS, NIS+ or LDAP over a secure
SSL connection. rpasswdd behaves like the normal passwd(1) program and
uses PAM for authentication and changing the password, so it can be
configured very flexible for the local requirements.

%description -n rpasswdd -l pl.UTF-8
rpasswdd to demon pozwalający użytkownikom zmieniać hasła w obecności
usług katalogowych takich jak NIS, NIS+ czy LDAP po bezpiecznym
połączeniu SSL. rpasswdd zachowuje się tak, jak normalny program
passwd(1) i używam PAM do uwierzytelniania i zmiany haseł, więc może
być bardzo elastycznie konfigurowany dla lokalnych wymagań.

%package -n pam-pam_rpasswd
Summary:	pam_rpasswd - PAM module to change remote password
Summary(pl.UTF-8):   pam_rpasswd - moduł PAM do zdalnej zmiany hasła
Group:		Base
# rpasswd.conf is in rpasswd
Requires:	rpasswd = %{version}-%{release}

%description -n pam-pam_rpasswd
The pam_rpasswd PAM module is for changing the password of user
accounts on a remote server over a secure SSL connection. It only
provides functionality for one PAM management group: password
changing.

%description -n pam-pam_rpasswd -l pl.UTF-8
Moduł PAM pam_rpasswd służy do zmiany haseł dla kont użytkowników na
zdalnym serwerze po bezpiecznym połączeniu SSL. Udostępnia
funkcjonalność tylko dla jednej grupy zarządzania PAM: zmiany haseł.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

sed -i -e 's/-Werror //' configure.in

rm -f po/stamp-po

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_bioapi:CPPFLAGS="-I/usr/include/bioapi"} \
	%{!?with_bioapi:ac_cv_header_bioapi_h=no ac_cv_lib_bioapi100_BioAPI_Init=no} \
	%{?with_audit:--enable-audit-plugin} \
	%{!?with_gnutls:--disable-gnutls} \
	--%{?with_ldap:en}%{!?with_ldap:dis}able-ldap \
	--enable-nls \
	--enable-pam_rpasswd \
	--%{?with_selinux:en}%{!?with_selinux:dis}able-selinux \
	--enable-slp \
	--disable-rpath
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,pwdutils,security,skel/tmp}

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
rm -f $RPM_BUILD_ROOT/etc/init.d/rpasswdd

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
%service rpasswdd restart "rpasswdd daemon"

%preun -n rpasswdd
if [ "$1" = "0" ]; then
	%service rpasswdd stop
	/sbin/chkconfig --del rpasswdd
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/chfn.allow
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/chsh.allow
%dir /etc/skel
%dir /etc/skel/tmp
%attr(755,root,root) %{_bindir}/chage
%attr(4755,root,root) %{_bindir}/chfn
%attr(4755,root,root) %{_bindir}/chsh
%attr(4755,root,root) %{_bindir}/expiry
%attr(4755,root,root) %{_bindir}/gpasswd
%attr(755,root,root) %{_bindir}/newgrp
%attr(4755,root,root) %{_bindir}/passwd
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
%attr(755,root,root) %{_sbindir}/useradd
%attr(755,root,root) %{_sbindir}/userdel
%attr(755,root,root) %{_sbindir}/usermod
%attr(755,root,root) %{_sbindir}/vigr
%attr(755,root,root) %{_sbindir}/vipw
%dir %{_libdir}/pwdutils
%attr(755,root,root) %{_libdir}/pwdutils/liblog_syslog.so*
%{_mandir}/man?/*
%exclude %{_mandir}/man1/rpasswd.1*
%exclude %{_mandir}/man5/rpasswd.conf.5*
%exclude %{_mandir}/man8/rpasswdd.8*
%exclude %{_mandir}/man8/pam_rpasswd.8*

%if %{with audit}
%files log-audit
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pwdutils/liblog_audit.so*
%endif

%files -n rpasswd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpasswd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/rpasswd.conf
%{_mandir}/man1/rpasswd.1*
%{_mandir}/man5/rpasswd.conf.5*

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
