# Put the RPM in the current directory.
%define _rpmdir .
# Don't check stuff, we know exactly what we want.
%undefine __check_files

%global tcollectordir /usr/local/tcollector
%global collectorsdir %{tcollectordir}/collectors
%global rootdir       %{_srcrpmdir}/..
%global eosdir        %{rootdir}/eos
%global srccollectors %{rootdir}/collectors
%global py2_sitelib   /usr/lib/python2.7/site-packages

BuildArch:      noarch
Name:           tcollector
Group:          System/Monitoring
Version:        @PACKAGE_VERSION@
Release:        @RPM_REVISION@
Distribution:   buildhash=@GIT_FULLSHA1@
License:        LGPLv3+
Summary:        Data collection framework for OpenTSDB
URL:            http://opentsdb.net/tcollector.html
Provides:       tcollector = @PACKAGE_VERSION@-@RPM_REVISION@_@GIT_SHORTSHA1@
Requires:       python(abi) = @PYTHON_VERSION@

%description
The tcollector package includes two subpackages.  The base tcollector
package will install the tcollector.py along with

%install
mkdir -p %{buildroot}/%{collectorsdir}/0/
mkdir -p %{buildroot}/etc/init.d/

# Install the init.d
%{__install} -m 0755 -D %{rootdir}/rpm/initd.sh %{buildroot}/etc/init.d/tcollector

# Install Base files
mkdir -p %{buildroot}%{tcollectordir}/collectors/lib/
mkdir -p %{buildroot}%{tcollectordir}/collectors/etc/
%{__install} -m 0755 -D %{srccollectors}/__init__.py %{buildroot}%{tcollectordir}/collectors/
%{__install} -m 0755 -D %{srccollectors}/lib/* %{buildroot}%{tcollectordir}/collectors/lib/
%{__install} -m 0755 -D %{srccollectors}/etc/* %{buildroot}%{tcollectordir}/collectors/etc/
%{__install} -m 0755 -D %{rootdir}/tcollector.py %{buildroot}%{tcollectordir}/

# Install Collectors
%{__install} -m 0755 -D %{srccollectors}/0/* %{buildroot}%{collectorsdir}/0/

# Install EOS files
%{__install} -m 0755 -D %{eosdir}/collectors/agent*.sh %{buildroot}/%{collectorsdir}/0/
%{__install} -m 0755 -D %{eosdir}/collectors/eos.py %{buildroot}/%{collectorsdir}/0/
mkdir -p %{buildroot}/usr/bin/
%{__install} -m 0755 -D %{eosdir}/tcollector %{buildroot}/usr/bin/
mkdir -p %{buildroot}/%{py2_sitelib}/
%{__install} -m 0755 -D %{eosdir}/tcollector_agent.py %{buildroot}/%{py2_sitelib}/


%files
%dir %{tcollectordir}
%attr(755, -, -) /etc/init.d/tcollector
%{tcollectordir}/collectors/__init__.py
%dir %{tcollectordir}/collectors/lib/
%{tcollectordir}/collectors/lib/__init__.py
%{tcollectordir}/collectors/lib/utils.py
%{tcollectordir}/collectors/lib/hadoop_http.py
%dir %{tcollectordir}/collectors/etc/
%{tcollectordir}/collectors/etc/__init__.py
%{tcollectordir}/collectors/etc/config.py
%{tcollectordir}/collectors/etc/flume_conf.py
%{tcollectordir}/collectors/etc/g1gc_conf.py
%{tcollectordir}/collectors/etc/graphite_bridge_conf.py
%{tcollectordir}/collectors/etc/jolokia_conf.py
%{tcollectordir}/collectors/etc/mysqlconf.py
%{tcollectordir}/collectors/etc/postgresqlconf.py
%{tcollectordir}/collectors/etc/udp_bridge_conf.py
%{tcollectordir}/collectors/etc/zabbix_bridge_conf.py
%{tcollectordir}/tcollector.py


%package collectors
Summary: The linux OpenTSDB collectors
Group: System/Monitoring
Requires: tcollector >= 1.2.1
%description collectors


%files collectors
%{tcollectordir}/collectors/0/dfstat.py
%{tcollectordir}/collectors/0/ifstat.py
%{tcollectordir}/collectors/0/iostat.py
%{tcollectordir}/collectors/0/netstat.py
%{tcollectordir}/collectors/0/procnettcp.py
%{tcollectordir}/collectors/0/procstats.py
%{tcollectordir}/collectors/0/smart_stats.py


%package eos
Summary: Linux Collectors and Arista EOS Collectors
Group: System/Monitoring
Requires: tcollector
Requires: EosSdk >= 1.5.1
Obsoletes: tcollectorAgent <= 1.0.2

%description eos
The tcollector-eos subpackage provides files that leverage the EOSSDK to
gather statistics from EOS.  It should be used in conjunction with
the tcollector package and optionally the tcollector-collectors subpackage. If
you run make swix, all three packages will be included.

%files eos
%attr(755, -, -) /usr/bin/tcollector
%{tcollectordir}/collectors/0/agentcpu.sh
%{tcollectordir}/collectors/0/agentmem.sh
%{tcollectordir}/collectors/0/eos.py
%{py2_sitelib}/tcollector_agent.py
