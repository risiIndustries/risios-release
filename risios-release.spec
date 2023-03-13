%global release_name 	The Cure
%global dist_version 	38

Summary:	risiOS release files
Name:		risios-release
Version:	%{dist_version}
Release:	2%{?dist}
License:	MIT
Group:		System Environment/Base
Source0:	LICENSE
Source1:	README.developers
Source2:	README.risiOS-Release-Notes
Source3:	README.license

Source6:	85-display-manager.preset
Source7:	90-default.preset
Source8:	99-default-disable.preset
Source9:	90-default-user.preset

BuildArch: 	noarch

Provides: 	risios-release
Provides: 	risios-release-variant
Provides: 	risios-release-identity

# We need to Provides: and Conflicts: system release here and in each
# of the generic-release-$VARIANT subpackages to ensure that only one
# may be installed on the system at a time.
Conflicts: 	system-release
Provides: 	system-release
Provides: 	system-release(%{dist_version})
Conflicts:	fedora-release
Conflicts:	fedora-release.identity
Requires: 	risios-release-common = %{version}-%{release}

%description
risiOS release files such as yum configs and various /etc/ files that
define the release. This package explicitly is a replacement for the 
trademarked release package, if you are unable for any reason to abide by the 
trademark restrictions on that release package.


%package common
Summary: risiOS release files

Requires:   risios-release-variant
Suggests:   risios-release

Requires:   fedora-repos(%{dist_version})
Conflicts:  fedora-release-common

%description common
Release files common to all Editions and Spins


%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes

%description notes
risiOS release notes package. This package explicitly is a replacement
for the trademarked release-notes package, if you are unable for any reason
to abide by the trademark restrictions on that release-notes
package. Please note that there is no actual useful content here.

%prep

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "risiOS release %{version} (%{release_name})" > %{buildroot}%{_prefix}/lib/fedora-release
echo "cpe:/o:risi:risios:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Symlink the -release files
install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/fedora-release %{buildroot}%{_sysconfdir}/fedora-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s fedora-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s fedora-release %{buildroot}%{_sysconfdir}/system-release

# Create the common os-release file
install -d $RPM_BUILD_ROOT/usr/lib/os.release.d/
cat << EOF >>%{buildroot}%{_prefix}/lib/os-release
NAME=risiOS
VERSION="%{dist_version} (%{release_name})"
ID=risios
ID_LIKE=fedora
VERSION_ID=%{dist_version}
PRETTY_NAME="risiOS %{dist_version} (%{release_name})"
ANSI_COLOR="0;94"
CPE_NAME="cpe:/o:risi:risios:%{dist_version}"
HOME_URL="https://risi.io/"
SUPPORT_URL="https://risi.io/"
BUG_REPORT_URL="https://risi.io/"
REDHAT_BUGZILLA_PRODUCT="risiOS"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="risiOS"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
PRIVACY_POLICY_URL="https://risi.io/"
EOF

# Create the common /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create os-release and issue files for the different editions here
# There are no separate editions for risios-release

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release $RPM_BUILD_ROOT/etc/os-release

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora		%{dist_version}
%%dist			%%{?distprefix}.fc%{dist_version}%%{?with_bootstrap:~bootstrap}
%%fc%{dist_version}	1
EOF

# Install readme
mkdir -p readme
install -pm 0644 %{SOURCE3} readme/README.risiOS-Release-Notes

# Install licenses
mkdir -p licenses
install -pm 0644 %{SOURCE0} licenses/LICENSE
install -pm 0644 %{SOURCE2} licenses/README.license

# Add presets
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/user-preset/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

# Default system wide
install -Dm0644 %{SOURCE6} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE7} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE8} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE9} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/user-preset/


%files common
%license licenses/LICENSE licenses/README.license
%{_prefix}/lib/fedora-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/fedora-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset


%files
%{_prefix}/lib/os-release


%files notes
%doc readme/README.risiOS-Release-Notes


%changelog
* Sat Oct 01 2022 PizzaLovingNerd
- risiOS 37

* Wed Aug 11 2021 PizzaLovingNerd
- Setup for risiOS

* Mon Nov 05 2018 Stephen Gallagher <sgallagh@redhat.com> - 30-0.1
- Update to 30
- Drop variants from generic-release
- Rework significantly to be more like fedora-release
- Sync systemd presets from fedora-release

* Mon Jul 09 2018 Adam Williamson <awilliam@redhat.com> - 29-0.2
- Server: don't require rolekit (not installable, soon to be retired)

* Mon Apr 16 2018 Tom Callaway <spot@fedoraproject.org> 29-0.1
- add ID_LIKE=fedora to os-release
- update to 29

* Wed Nov 15 2017 Tom Callaway <spot@fedoraproject.org> 28-0.3
- rework significantly to match fedora-release

* Mon Sep 25 2017 Matthew Miller <mattdm@fedoraproject.org> 28-0.2
- use dist-tag -- and define it if previously undefined

* Wed Aug 23 2017 Mohan Boddu <mboddu@redhat.com> 28-0.1
- Rawhide is now 28

* Fri Mar  3 2017 Tom Callaway <spot@fedoraproject.org> 27-0.1
- Rawhide is now 27

* Thu Aug 04 2016 Bruno Wolff III <bruno@wolff.to> - 26-0.1
- Rawhide is now 26

* Sat Mar 05 2016 Bruno Wolff III <bruno@wolff.to> - 25-0.1
- Rawhide is now 25

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 24-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Tom Callaway <spot@fedoraproject.org> - 24-0.3
- spec file cleanups

* Sat Aug 22 2015 Bruno Wolff III <bruno@wolff.to> - 24-0.2
- Fix typo in obsoletes

* Wed Jul 15 2015 Bruno Wolff III <bruno@wolff.to> - 24-0.1
- Rawhide is now f24

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Dennis Gilmore <dennis@ausil.us> - 23-0.5
- add system preset files
- drop product sub-packages

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.4
- Fix up change log

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.3
- Rawhide is now 23

* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.3
- add versioned provide for system-release(VERSION)

* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.2
- add productization (it is the foooooture)

* Thu Aug 07 2014 Dennis Gilmore <dennis@ausil.us> - 22-0.1
- Require fedora-repos and no longer ship repo files

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Tom Callaway <spot@fedoraproject.org> - 21-4
- license changes and clarification doc

* Sun Mar 09 2014 Bruno Wolff III <bruno@wolff.to> - 21-3
- Install dist macro into the correct directory

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-2
- Work around incorrect prefix in the upstream tarball

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-1
- Bump version to match current rawhide

* Sat Dec 21 2013 Bruno Wolff III <bruno@wolff.to> - 21-0.3
- Update version to 21 (which should have happened when f20 was branched)
- Changed to work with recent yum change (bug 1040607)

* Mon Dec  9 2013 Tom Callaway <spot@fedoraproject.org> - 20-1
- final release (disable rawhide dep)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 20-0.1
- sync

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 19-2
- sync to release

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 19-0.3
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Tom Callaway <spot@fedoraproject.org> - 19-0.1
- sync to 19-0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Tom Callaway <spot@fedoraproject.org> - 18-0.2
- sync with fedora-release model

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Tom Callaway <spot@fedoraproject.org> - 17-0.2
- initial 17

* Fri Jul 22 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.2
- require -rawhide subpackage if we're built for rawhide

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.1
- initial 16

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 15-1
- sync to f15 final

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 15-0.3
- sync to rawhide

* Wed Feb 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.2
- fix broken requires

* Wed Feb 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.1
- update to sync with fedora-release

* Mon Nov 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 12-1
- Update for F12 final

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11.90-1
- Build for F12 collection

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11-1
- resync with fedora-release package

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-2
- drop Requires: system-release-notes

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-1
- 10.90

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10-1
- Bump to 10, update repos

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-2
- add Conflicts
- further sanitize descriptions

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-1
- initial package for generic-release and generic-release-notes
