%{!?version: %global version 0.0.0}
%global debug_package %{nil}
%global selinuxtype targeted
%global selinux_modulename rhc_advisor_collector
%global selinux_policy_version 42.1.8

Name:           rhc-advisor-collector
Version:        %{version}
Release:        1%{?dist}
Summary:        Advisor collector for rhc

License:        Apache-2.0
URL:            https://github.com/RedHatInsights/rhc-advisor-collector
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  selinux-policy-devel
BuildRequires:  insights-core-selinux

Requires:       rhc
Requires:       insights-core
Requires:       ((%{name}-selinux = %{version}-%{release}) if selinux-policy-%{selinuxtype})
%{?systemd_requires}

%description
Advisor collector executed by rhc-collector. The collection engine stays in
insights-core; this package provides the rhc_advisor_collector.rhc adapter
that bridges rhc-collector's executable contract to it. It also installs the
com.redhat.advisor entrypoint, its configuration, and the systemd units. The
timer is not enabled.

%package selinux
Summary:        SELinux policy for rhc-advisor-collector
License:        Apache-2.0
BuildArch:      noarch
Requires:       insights-core-selinux
Requires:       selinux-policy >= %{selinux_policy_version}
Requires:       selinux-policy-%{selinuxtype} >= %{selinux_policy_version}
Requires(post): libselinux-utils
Requires(post): policycoreutils
Requires(post): selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-base >= %{selinux_policy_version}
Requires(postun): libselinux-utils
Requires(postun): policycoreutils

%description selinux
SELinux policy that transitions com.redhat.advisor from rhc_collector_t into
the existing insights_core_t domain. Collection permissions stay in the
insights_core module shipped by insights-core-selinux.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
# Policy sources live in-tree (selinux/), same as rhc.spec's own rhc-selinux
# subpackage -- no second Source, no separate repository to keep in lockstep.
make -C selinux -f %{_datadir}/selinux/devel/Makefile %{selinux_modulename}.pp
bzip2 -9 selinux/%{selinux_modulename}.pp

%install
install -D -p -m 0755 collectors/com.redhat.advisor %{buildroot}%{_libexecdir}/rhc/collectors/com.redhat.advisor
install -D -p -m 0644 rhc_advisor_collector/__init__.py %{buildroot}%{python3_sitelib}/rhc_advisor_collector/__init__.py
install -D -p -m 0644 rhc_advisor_collector/rhc.py %{buildroot}%{python3_sitelib}/rhc_advisor_collector/rhc.py
install -D -p -m 0644 config/com.redhat.advisor.toml %{buildroot}%{_prefix}/lib/rhc/collectors/com.redhat.advisor.toml
install -D -p -m 0644 systemd/rhc-collector-com.redhat.advisor.service %{buildroot}%{_unitdir}/rhc-collector-com.redhat.advisor.service
install -D -p -m 0644 systemd/rhc-collector-com.redhat.advisor.timer %{buildroot}%{_unitdir}/rhc-collector-com.redhat.advisor.timer
install -D -p -m 0644 selinux/%{selinux_modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{selinux_modulename}.pp.bz2
install -D -p -m 0644 selinux/%{selinux_modulename}.if %{buildroot}%{_datadir}/selinux/devel/include/distributed/%{selinux_modulename}.if

%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post
%systemd_post rhc-collector-com.redhat.advisor.service
%systemd_post rhc-collector-com.redhat.advisor.timer
if [ -x /usr/sbin/restorecon ]; then
    /usr/sbin/restorecon /usr/libexec/rhc/collectors/com.redhat.advisor || :
fi

%preun
%systemd_preun rhc-collector-com.redhat.advisor.service
%systemd_preun rhc-collector-com.redhat.advisor.timer

%postun
%systemd_postun rhc-collector-com.redhat.advisor.service
%systemd_postun rhc-collector-com.redhat.advisor.timer

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{selinux_modulename}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{selinux_modulename}
    %selinux_relabel_post -s %{selinuxtype}
fi

%files
%license LICENSE
%{_libexecdir}/rhc/collectors/com.redhat.advisor
%{python3_sitelib}/rhc_advisor_collector/
%{_prefix}/lib/rhc/collectors/com.redhat.advisor.toml
%{_unitdir}/rhc-collector-com.redhat.advisor.service
%{_unitdir}/rhc-collector-com.redhat.advisor.timer

%files selinux
%license LICENSE
%{_datadir}/selinux/packages/%{selinuxtype}/%{selinux_modulename}.pp.*
%{_datadir}/selinux/devel/include/distributed/%{selinux_modulename}.if
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{selinux_modulename}

%changelog
* Fri Nov 13 2026 Ping Qin <30404410+qinpingli@users.noreply.github.com> - 0.0.1-1
- Initial package for the Advisor collector and its SELinux transition.
