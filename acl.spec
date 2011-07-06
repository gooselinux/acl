Summary: Access control list utilities
Name: acl
Version: 2.2.49
Release: 4%{?dist}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libattr-devel >= 2.4.1
BuildRequires: autoconf, libtool >= 1.5, gettext, gawk
Requires: libacl = %{version}-%{release}
Source: http://download.savannah.gnu.org/releases-noredirect/acl/acl-%{version}.src.tar.gz
Patch0: acl-2.2.3-multilib.patch
Patch1: acl-2.2.39-build.patch
Patch2: acl-2.2.49-setfacl-walk.patch
Patch3: acl-2.2.49-bz467936.patch
Patch4: acl-2.2.49-tests.patch
Patch5: acl-2.2.49-setfacl-restore.patch
License: GPLv2+
Group: System Environment/Base
URL: http://oss.sgi.com/projects/xfs/

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n libacl
Summary: Dynamic library for access control list support
License: LGPLv2+
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary: Access control list static libraries and headers
License: LGPLv2+
Group: Development/Libraries
Requires: libacl = %{version}-%{release}, libattr-devel
Requires: nfs-utils-lib, openldap

%description -n libacl-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
autoconf

%build
touch .census
# acl abuses libexecdir
%configure --libdir=/%{_lib} --libexecdir=%{_libdir}
make %{?_smp_mflags} LIBTOOL="libtool --tag=CC"

%check
if ./setfacl/setfacl -m u:`id -u`:rwx .; then
    make tests || exit $?
    if test 0 = `id -u`; then
        make root-tests || exit $?
    fi
else
    echo '*** ACLs are probably not supported by the file system,' \
         'the test-suite will NOT run ***'
fi

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-dev DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

# get rid of libacl.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/libacl.la

# fix links to shared libs and permissions
rm -f $RPM_BUILD_ROOT/%{_libdir}/libacl.so
ln -sf ../../%{_lib}/libacl.so $RPM_BUILD_ROOT/%{_libdir}/libacl.so
chmod 0755 $RPM_BUILD_ROOT/%{_lib}/libacl.so.*.*.*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl
%{_datadir}/doc/acl-%{version}
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man5/acl.5*

%files -n libacl-devel
%defattr(-,root,root)
/%{_lib}/libacl.so
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_libdir}/libacl.*
%{_mandir}/man3/acl_*

%files -n libacl
%defattr(-,root,root)
/%{_lib}/libacl.so.*

%changelog
* Tue May 25 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-4
- let acl depend on the same version of libacl (#595674)

* Wed Mar 24 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-3
- prevent setfacl --restore from SIGSEGV on malformed restore file (#576512)
- run the test-suite if possible

* Wed Mar 10 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-2
- upstream patch for setfacl --restore SUID/SGID bits handling

* Thu Jan 07 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-1
- update to the latest bugfix release
- CVE-2009-4411

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.2.47-5.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 31 2008 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.47-3
- little improvement to params patch
- Resolves: #457244

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.47-2
- rework params patch to apply with fuzz=0
- fix license tag

* Tue Feb 12 2008 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.47-1
- new upstream version

* Mon Jan 28 2008 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.45-3
- Fixed segfault when using only "--" as parameter
- Resolves: #430458

* Wed Nov  7 2007 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.45-2
- Fixed setfacl exitcodes
- Resolves: #368451

* Wed Oct 31 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 2.2.45-1
- New version
- dropped walk patch

* Thu Sep 20 2007 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.39-10
- Rewriten path_max patch to support long UTF8 names
- Resolves #287701, #183181

* Fri Aug 31 2007 Steve Dickson <steved@redhat.com> - 2.2.39-9
- Removed NFS4 ACL patch since it was rejected by upstream.

* Thu Aug 30 2007 Jeremy Katz <katzj@redhat.com> - 2.2.39-8
- disable nfs patch; linking libacl against libs in /usr will lead to breakage

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.2.39-7
- Build Require gawk

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.2.39-6
- Rebuild for selinux ppc32 issue.

* Mon Aug 27 2007 Steve Dickson <steved@redhat.com>  2.2.39-5
- Added NFS v4 ACL support

* Thu Jul 26 2007 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.39-4.1
- Updated man page for getfacl

* Wed Jul 25 2007 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.39-4
- Added support fort short params to getfacl
- Resolves: #204087

* Wed Mar 21 2007 Thomas Woerner <twoerner@redhat.com> 2.2.39-3.1
- new improved walk patch with fixed getfacl exit code (rhbz#232884)

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 2.2.39-3
- fix buildroot
- remove trailing dot from summary
- -devel requires same version of libacl
- escape macro in changelog
- make .so symlink relative

* Thu Feb 22 2007 Steve Grubb <sgrubb@redhat.com> 2.2.39-2
- Apply patch to make order consistent.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.39-1.1
- rebuild

* Wed Jul  5 2006 Thomas Woerner <twoerner@redhat.com> 2.2.39-1
- new version 2.2.39
- fixed usage of long UTF-8 filenames (#183181)
  Thanks to Andrey for the initial patch.

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 2.2.34-2
- rebuild for -devel deps

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.34-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.34-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Thomas Woerner <twoerner@redhat.com> 2.2.34-1
- new version 2.2.34

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Thomas Woerner <twoerner@redhat.com> 2.2.32-2.1
- fixed permissions of libacl

* Tue Dec  6 2005 Thomas Woerner <twoerner@redhat.com> 2.2.32-2
- spec file cleanup
- mark po files as lang specific

* Sun Nov 06 2005 Florian La Roche <laroche@redhat.com>
- 2.2.32

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.2.31-1
- update to 2.2.31

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.2.23-9
- get rid of *.la files
- remove duplicate doc files

* Wed Feb  9 2005 Stephen C. Tweedie <sct@redhat.com> 2.2.23-6
- Rebuild

* Thu Sep 16 2004 Jeremy Katz <katzj@redhat.com> - 2.2.23-5
- make the libs executable so that we find their dependencies (#132696)

* Fri Sep 10 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.23-4
- libacl-devel Requires: libattr-devel for libattr.la

* Fri Sep 10 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.23-3
- Requires libtool >= 1.5 for building

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.2.23-2
- Make libacl.so.* executable.

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.2.23-1
- Update to latest upstream version.

* Sun Aug  8 2004 Alan Cox <alan@redhat.com> 2.2.7-7
- Close bug #125300 (Steve Grubb: build requires libtool,gettext)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 31 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.7-5
- Add missing %%defattr

* Tue Mar 30 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.7-3
- Add /usr/include/acl to files manifest
- Fix location of doc files, add main doc dir to files manifest

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Aug  5 2003 Elliot Lee <sopwith@redhat.com> 2.2.7-2
- Fix libtool invocation

* Tue Jun  3 2003 Stephen C. Tweedie <sct@redhat.com> 2.2.7-1
- Update to acl-2.2.7

* Wed Mar 26 2003 Michael K. Johnson <johnsonm@redhat.com> 2.2.3-2
- include patch from Jay Berkenbilt to print better error messages

* Tue Jan 28 2003 Michael K. Johnson <johnsonm@redhat.com> 2.2.3-1
- udpate/rebuild

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 2.0.11-7
- set execute bits on library so that requires are generated.

* Tue Nov 19 2002 Elliot Lee <sopwith@redhat.com> 2.0.11-5
- Correct patch in previous fix so that shared libraries go in /lib* 
  instead of /usr/lib*

* Tue Nov 19 2002 Elliot Lee <sopwith@redhat.com> 2.0.11-4
- Fix multilibbing

* Wed Sep 11 2002 Than Ngo <than@redhat.com> 2.0.11-3
- Added fix to install libs in correct directory on 64bit machine

* Thu Aug 08 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.11-2
- Made the package only own the one directory that is unique to it:
  /usr/include/acl

* Mon Jun 24 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.11-1
- Initial Red Hat package
  Made as few changes as possible relative to upstream packaging to
  make it easier to maintain long-term.  This means that some of
  the techniques used here are definitely not standard Red Hat
  techniques.  If you are looking for an example package to fit
  into Red Hat Linux transparently, this would not be the one to
  pick.
- acl-devel -> libacl-devel
