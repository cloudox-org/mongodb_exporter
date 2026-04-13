%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name: mongodb_exporter
Version: 0.50.0
Release: 1%{?dist}
Summary: A Prometheus exporter for MongoDB including sharding, replication and storage engines
License: ASL 2.0
URL:     https://github.com/percona/mongodb_exporter

Source0: https://github.com/percona/mongodb_exporter/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description
A Prometheus exporter for MongoDB including sharding, replication and storage engines

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service

%changelog
* Mon Apr 13 2026 Ivan Garcia <igarcia@cloudox.org> - 0.50.0
- Bump version to 0.50.0
* Tue Mar 31 2026 Ivan Garcia <igarcia@cloudox.org> - 0.49.0
- Initial packaging for the 0.49.0 branch
