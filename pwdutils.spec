# TODO:
# - finish and test it
# - subpackage with rpasswd daemon
#
Summary:	Utilities to manage the passwd and shadow user information
Summary(pl):	Narzêdzia do zarz±dzania informacjami o u¿ytkownikach z passwd i shadow
Name:		pwdutils
Version:	2.4
Release:	1
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2
# Source0-md5:	7635c09b005f0e9447df8b42b3942187
Source1:	%{name}.useradd
# missing in repo
#Source2:	%{name}.rpasswdd.init
Source3:	%{name}.login.defs
Source4:	chage.pamd
Source5:	chfn.pamd
Source6:	chsh.pamd
Source7:	passwd.pamd
Source8:	useradd.pamd
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
Obsoletes:	shadow
Obsoletes:	shadow-extras
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
pwdutils to zestaw narzêdzi do zarz±dzania informacjami o
u¿ytkownikach z passwd i shadow. Ró¿nica w stosunku do pakietu shadow
polega na tym, ¿e te narzêdzia mog± tak¿e modyfikowaæ informacje
zapisane w bazie NIS, NIS+ lub LDAP. PAM jest u¿ywany do
uwierzytelniania u¿ytkowników i zmiany hase³. Zestaw zawiera passwd,
chage, chfn, chsh oraz demona do zmiany has³a na zdalnej maszynie po
bezpiecznym po³±czeniu SSL. Demon tak¿e u¿ywa PAM, wiêc mo¿na zmieniaæ
has³a niezale¿nie od tego, gdzie s± przechowywane.

%prep
%setup -q

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-rpath
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d/,pwdutils,skel}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sbindir}/*.local $RPM_BUILD_ROOT/etc/pwdutils
install %{SOURCE1} $RPM_BUILD_ROOT/etc/default/useradd
#install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/rpasswdd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/login.defs

install %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/chage
install %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/chfn
install %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/chsh
install %{SOURCE7} $RPM_BUILD_ROOT/etc/pam.d/passwd
install %{SOURCE8} $RPM_BUILD_ROOT/etc/pam.d/useradd

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ ! -f /etc/shadow ]; then
	%{_sbindir}/pwconv
fi

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README THANKS TODO
%attr(750,root,root) %dir %{_sysconfdir}/default
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/default/*
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%attr(750,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}/*.local
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/chage
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/chfn
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/chsh
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/passwd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/rpasswd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/useradd
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/login.defs
%dir /etc/skel
%attr(755,root,root) %{_bindir}/chage
%attr(4755,root,root) %{_bindir}/chfn
%attr(4755,root,root) %{_bindir}/chsh
%attr(4755,root,root) %{_bindir}/expiry
%attr(4755,root,root) %{_bindir}/gpasswd
%attr(4755,root,root) %{_bindir}/passwd
%attr(755,root,root) %{_bindir}/rpasswd
%attr(755,root,root) %{_sbindir}/chpasswd
%attr(755,root,root) %{_sbindir}/groupadd
%attr(755,root,root) %{_sbindir}/groupdel
%attr(755,root,root) %{_sbindir}/groupmod
%attr(755,root,root) %{_sbindir}/rpasswdd
%attr(755,root,root) %{_sbindir}/useradd
%attr(755,root,root) %{_sbindir}/userdel
%attr(755,root,root) %{_sbindir}/usermod
%attr(755,root,root) %{_sbindir}/vigr
%attr(755,root,root) %{_sbindir}/vipw
%{_mandir}/man?/*
#%attr(754,root,root) /etc/rc.d/init.d/rpasswdd
