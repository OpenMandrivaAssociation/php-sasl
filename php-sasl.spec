%define modname sasl
%define soname %{modname}.so
%define inifile A40_%{modname}.ini

Summary:	Cyrus SASL Extension
Name:		php-%{modname}
Epoch:		1
Version:	0.1.0
Release:	48
Group:		Development/PHP
License:	PHP License
Url:		http://pecl.php.net/package/sasl
Source0:	http://pecl.php.net/get/sasl-%{version}.tgz
Patch0:		sasl-0.1.0-lib64.diff
Patch1:		sasl-0.1.0-php54x.diff
Patch2:		sasl-0.1.0-sasl2_shared.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	sasl-devel

%description
SASL is the Simple Authentication and Security Layer (as defined by RFC 2222).
It provides a system for adding plugable authenticating support to
connection-based protocols. The SASL Extension for PHP makes the Cyrus SASL
library functions available to PHP. It aims to provide a 1-to-1 wrapper around
the SASL library to provide the greatest amount of implementation flexibility.
To that end, it is possible to build both a client-side and server-side SASL
implementation entirely in PHP.

%prep
%setup -qn sasl-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p0

%build
%serverbuild

export SASL_SUB="sasl"
export SASL_SHARED_LIBADD="-lsasl2"

phpize
%configure2_5x \
	--with-libdir=%{_lib} \
	--with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
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

%files 
%doc docs tests
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

