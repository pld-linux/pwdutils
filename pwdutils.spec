# TODO:
# - finish it
# - use the same *.pam files as in shadow.spec
# - subpackage with rpasswd daemon
#
Summary:	Utilities to manage the passwd and shadow user information
Summary(pl):	Narz�dzia do zarz�dzania informacjami o u�ytkownikach z passwd i shadow
Name:		pwdutils
Version:	2.3.90
Release:	1
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2
Patch0:		%{name}-userbuild.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
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

%prep
%setup -q
%patch0 -p1

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-rpath
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{?_without_static:/sbin/ldconfig}
if [ ! -f /etc/shadow ]; then
	%{_sbindir}/pwconv
fi

%{!?_without_static:%postun -p /sbin/ldconfig}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README THANKS TODO
%attr(750,root,root) %dir %{_sysconfdir}/default
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/default/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/chage
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/passwd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/shadow
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/useradd
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/login.defs
%attr(600,root,root) %ghost %{_sysconfdir}/shadow
%dir /etc/skel
%{?_without_static:%attr(755,root,root) %{_libdir}/lib*}
%attr(755,root,root) %{_sbindir}/chpasswd
%attr(755,root,root) %{_sbindir}/group*
%attr(755,root,root) %{_sbindir}/grpck
%attr(755,root,root) %{_sbindir}/pwck
%attr(755,root,root) %{_sbindir}/*conv
%attr(4755,root,root) %{_bindir}/passwd
