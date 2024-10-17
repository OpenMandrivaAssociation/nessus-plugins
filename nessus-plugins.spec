Summary:	Nessus security scanner plugins
Name:		nessus-plugins
Version:	2.2.10
Release:	%mkrel 7
License:	GPL
Group:		System/Servers
URL:		https://www.nessus.org
# http://cgi.tenablesecurity.com/nessus3dl.php?file=nessus-plugins-2.2.10.tar.gz&licence_accept=yes&t=5a144975306462c6d49d299ba1d6c0b2
Source0:	%{name}-%{version}.tar.gz
Source9:	plugins_api.txt.bz2
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	openssl-devel
BuildRequires:	libnasl-devel = %{version}
BuildRequires:	nessus-devel >= %{version} 
BuildRequires:	libnessus-devel >= %{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Nessus 2.2 is a free, up-to-date, and full featured remote security
scanner for Linux. It is multithreaded, plugin-based, and has a nice
GTK interface.  It has powerful reporting capabilities (HTML, LaTeX,
ASCII text) and not only points out problems, but suggests a solution
for each of them.

This package provides more then 1000 plugins for nessus.

%prep

%setup -q -n %{name}
bzip2 -cd %{SOURCE9} > ./`basename %{SOURCE9} .bz2`

# fix permissions
perl -pi -e "s|555|755|g" Makefile
perl -pi -e "s|444|644|g" Makefile

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure* aclocal.m4

%build
%define __libtoolize /bin/true

ac_cv_prog_cc_g=no ac_cv_prog_cxx_g=no \
%configure
perl -pi -e 's/-o root / /g; s/-o \$\(installuser\) / /g; y/{}/()/' Makefile
%make

%install
if [ -d %{buildroot} ]; then rm -rf %{buildroot}; fi

%makeinstall_std

mkdir -p %{buildroot}{%{_bindir},%{_libdir}/%{name}/reports,%{_sysconfdir}/nessus,%{_initrddir},%{_var}/log/nessus}
 
# Correct paths in devel stuff
perl -pi -e 's|^PREFIX=.*|PREFIX='%{_prefix}'|' \
 %{buildroot}%{_bindir}/*-config \

# remove unwanted files
rm -rf %{buildroot}%{_libdir}/nessus/plugins_factory

# why do they name their dl name to ".nes" ???
pushd %{buildroot}%{_libdir}/nessus/plugins
    for i in *.nes; do
	new_name=`echo $i|sed -e 's/\.nes/\.so/'`
	ln -s $i $new_name
	chmod 755 $i $new_name
    done
popd

%clean
if [ -d %{buildroot} ]; then rm -rf %{buildroot}; fi

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/nessus-build
%attr(0755,root,root) %{_sbindir}/nessus-update-plugins
%{_libdir}/nessus/plugins/*
%{_mandir}/man1/*
%{_mandir}/man8/*
