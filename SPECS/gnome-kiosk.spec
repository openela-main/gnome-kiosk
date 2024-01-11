%global tarball_version %%(echo %{version} | tr '~' '.')
%global major_version %(echo -n %{tarball_version} | sed 's/[.].*//')

%global gettext_version                         0.19.6
%global gnome_desktop_version                   40~rc
%global glib2_version                           2.68.0
%global gtk4_version                            3.24.27
%global mutter_version                          40.0
%global gsettings_desktop_schemas_version       40~rc
%global ibus_version                            1.5.24
%global gnome_settings_daemon_version           40~rc

Name:           gnome-kiosk
Version:        40.0
Release:        5%{?dist}
Summary:        Window management and application launching for GNOME

License:        GPLv2+
URL:            https://gitlab.gnome.org/halfline/gnome-kiosk
Source0:        https://download.gnome.org/sources/%{name}/%{major_version}/%{name}-%{tarball_version}.tar.xz

Provides:       firstboot(windowmanager) = %{name}

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext >= %{gettext_version}
BuildRequires:  git
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-desktop-3.0) >= %{gnome_desktop_version}
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(ibus-1.0) >= %{ibus_version}
BuildRequires:  pkgconfig(libmutter-8) >= %{mutter_version}
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  meson

Requires:       gnome-settings-daemon%{?_isa} >= %{gnome_settings_daemon_version}
Requires:       gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}

Patch10001:     0001-compositor-Support-systemd-user-sessions.patch
Patch10002:     0002-Add-a-script-for-simplifying-kiosk-setup.patch

Patch20001:     0001-compositor-Ignore-some-of-the-builtin-keybindings.patch
Patch20002:     0002-kiosk-script-Make-sure-desktop-file-for-script-is-hi.patch
Patch20003:     0003-kiosk-script-Install-session-file-with-fallback-in-m.patch
Patch20004:     0004-kiosk-script-Give-xsession-and-wayland-session-file-.patch
Patch20005:     0005-kiosk-script-Add-a-hint-about-using-firefox-to-the-k.patch
Patch20006:     0006-kiosk-script-Send-SIGHUP-to-script-at-shutdown-time.patch

Patch30001:     0001-compositor-Be-more-permissive-about-what-s-considere.patch

%description
GNOME Kiosk provides a desktop enviroment suitable for fixed purpose, or
single application deployments like wall displays and point-of-sale systems.

%package search-appliance
Summary:        Example search application application that uses GNOME Kiosk
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}
Requires:       firefox
Requires:       gnome-session
BuildArch:      noarch

%description search-appliance
This package provides a full screen firefox window pointed to google.

%package script-session
Summary:        Basic session used for running kiosk application from shell script
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}
Recommends:     gedit
Requires:       gnome-session
BuildArch:      noarch

%description script-session
This package generates a shell script and the necessary scaffolding to start that shell script within a kiosk session.

%prep
%autosetup -S git -n %{name}-%{tarball_version}

%build
%meson
%meson_build

%install
%meson_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Kiosk.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Kiosk.SearchApp.desktop

%files
%license COPYING
%doc README.md
%{_bindir}/gnome-kiosk
%{_datadir}/applications/org.gnome.Kiosk.desktop
%{_userunitdir}/org.gnome.Kiosk.target
%{_userunitdir}/org.gnome.Kiosk@wayland.service
%{_userunitdir}/org.gnome.Kiosk@x11.service

%files -n gnome-kiosk-script-session
%{_bindir}/gnome-kiosk-script
%{_userunitdir}/gnome-session@gnome-kiosk-script.target.d/session.conf
%{_userunitdir}/org.gnome.Kiosk.Script.service
%{_datadir}/applications/org.gnome.Kiosk.Script.desktop
%{_datadir}/gnome-session/sessions/gnome-kiosk-script.session
%{_datadir}/wayland-sessions/gnome-kiosk-script.desktop
%{_datadir}/xsessions/gnome-kiosk-script.desktop

%files -n gnome-kiosk-search-appliance
%{_datadir}/applications/org.gnome.Kiosk.SearchApp.desktop
%{_datadir}/gnome-session/sessions/org.gnome.Kiosk.SearchApp.session
%{_datadir}/xsessions/org.gnome.Kiosk.SearchApp.Session.desktop
%{_datadir}/wayland-sessions/org.gnome.Kiosk.SearchApp.Session.desktop

%changelog
* Wed Nov 09 2022 Ray Strode <rstrode@redhat.com> - 40.0-5
- Detect anaconda as the kiosk app better
  Resolves: #1999060

* Wed Aug 11 2021 Ray Strode <rstrode@redhat.com> - 40.0-4
- Fix crash when hitting alt-f2
- Various fixes to the script-session
  Related: #1965338

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 40.0-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Aug 06 2021 Ray Strode <rstrode@redhat.com> - 40.0-2
- Support systemd --user sessions
- Add script-session subpackage
  Related: #1965338

* Mon May 17 2021 Ray Strode <rstrode@redhat.com> - 40.0-1
- Update to 40.0
  Related: #1950042

* Tue Apr 27 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-7
- Fix desktop file
  Resolves: #1954285

* Fri Apr 23 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-6
- Add vprovides so initial-setup can use this

* Wed Apr 21 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-5
- Fix keyboard layouts getting out of sync in anaconda

* Tue Apr 20 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-4
- Fix infinite loop

* Mon Apr 19 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-3
- Fix crash

* Sun Apr 18 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-2
- Work with 3rd party keyboard layout selectors
- Be less aggressive about fullscreening windows

* Mon Apr 12 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-1
- Initial import

