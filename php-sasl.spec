%define modname sasl
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A40_%{modname}.ini

Summary:	Cyrus SASL Extension
Name:		php-%{modname}
Version:	0.1.0
Release:	%mkrel 43
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/sasl
Source0:	sasl-%{version}.tar.bz2
Patch0:		sasl-0.1.0-lib64.diff
Patch1:		sasl-0.1.0-php54x.diff
Patch2:		sasl-0.1.0-sasl2_shared.diff
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
%patch1 -p0
%patch2 -p0

%build
%serverbuild

export SASL_SUB="sasl"
export SASL_SHARED_LIBADD="-lsasl2"

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


%changelog
* Wed May 02 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-43mdv2012.0
+ Revision: 795040
- fix build (sasl)
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-42
+ Revision: 761121
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-41
+ Revision: 696372
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-40
+ Revision: 695317
- rebuilt for php-5.3.7

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-39
+ Revision: 667706
- mass rebuild

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-38
+ Revision: 646556
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-37mdv2011.0
+ Revision: 629743
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-36mdv2011.0
+ Revision: 628049
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-35mdv2011.0
+ Revision: 600181
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-34mdv2011.0
+ Revision: 588719
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-33mdv2010.1
+ Revision: 514649
- rebuilt for php-5.3.2

* Mon Feb 22 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-32mdv2010.1
+ Revision: 509470
- rebuild
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-30mdv2010.1
+ Revision: 485263
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-29mdv2010.1
+ Revision: 468090
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-28mdv2010.0
+ Revision: 451220
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:0.1.0-27mdv2010.0
+ Revision: 397593
- Rebuild

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-26mdv2010.0
+ Revision: 375362
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-25mdv2009.1
+ Revision: 346605
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-24mdv2009.1
+ Revision: 341513
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-23mdv2009.1
+ Revision: 321945
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-22mdv2009.1
+ Revision: 310222
- rebuilt against php-5.2.7

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-21mdv2009.0
+ Revision: 235880
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-20mdv2009.0
+ Revision: 200116
- rebuilt against php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-19mdv2008.1
+ Revision: 161953
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-18mdv2008.1
+ Revision: 107573
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-17mdv2008.0
+ Revision: 77460
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-16mdv2008.0
+ Revision: 64304
- use the new %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-15mdv2008.0
+ Revision: 39387
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-14mdv2008.0
+ Revision: 33782
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-13mdv2008.0
+ Revision: 21032
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-12mdv2007.0
+ Revision: 117537
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-11mdv2007.0
+ Revision: 78292
- fix deps

* Tue Nov 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-10mdv2007.0
+ Revision: 77389
- rebuilt for php-5.2.0

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-9mdv2007.1
+ Revision: 75327
- Import php-sasl

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-9
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-8mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-7mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-6mdk
- rebuilt for php-5.1.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-5mdk
- new group (Development/PHP) and iurt rebuild

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-4mdk
- rebuilt against php-5.1.2

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-3mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-2mdk
- rebuilt against php-5.1.0

* Thu Nov 03 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-1mdk
- rebuilt against php-5.1.0RC4
- fix versioning

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.1.0-0.RC1.2mdk
- rebuilt to provide a -debug package too

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.1.0-0.RC1.1mdk
- rebuilt against php-5.1.0RC1
- fixed the lib64 patch

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5_0.1.0-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.1.0-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.1.0-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.1.0-2mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.1.0-1mdk
- initial Mandrakelinux package
- added P0

