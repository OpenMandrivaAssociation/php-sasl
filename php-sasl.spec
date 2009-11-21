%define modname sasl
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A40_%{modname}.ini

Summary:	Cyrus SASL Extension
Name:		php-%{modname}
Version:	0.1.0
Release:	%mkrel 29
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/sasl
Source0:	sasl-%{version}.tar.bz2
Patch0:		sasl-0.1.0-lib64.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libsasl-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SASL is the Simple Authentication and Security Layer (as defined by RFC 2222).
It provides a system for adding plugable authenticating support to
connection-based protocols. The SASL Extension for PHP makes the Cyrus SASL
library functions available to PHP. It aims to provide a 1-to-1 wrapper around
the SASL library to provide the greatest amount of implementation flexibility.
To that end, it is possible to build both a client-side and server-side SASL
implementation entirely in PHP.

%prep

%setup -q -n sasl-%{version}
%patch0 -p0

%build
%serverbuild

export SASL_SUB="sasl"

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc docs tests
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
