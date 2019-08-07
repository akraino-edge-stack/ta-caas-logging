# Copyright 2019 Nokia

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

Name:           caas-logging
Version:        %{_version}
Release:        1%{?dist}
Summary:        CaaS Logging restful API and CLI plugins
License:        %{_platform_license}

Vendor:         %{_platform_vendor}
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python-flask, python2-flask-restful, python2-configparser
BuildRequires:  python python-setuptools

%description
This RPM contains CaaS Logging components (restful API and CLI plugins) for Akraino REC

%prep
%autosetup

%install
mkdir -p %{buildroot}%{_python_site_packages_path}/caas_logging

mkdir -p %{buildroot}%{_python_site_packages_path}/yarf/handlers/caas_logging
rsync -ra src/caas_logging/rest-plugin/* %{buildroot}/%{_python_site_packages_path}/yarf/handlers/caas_logging

mkdir -p %{buildroot}/opt/cmframework/activators/
rsync -ra src/caas_logging/activator/* %{buildroot}/opt/cmframework/activators

cd src && python setup.py install --root %{buildroot} --no-compile --install-purelib %{_python_site_packages_path} --install-scripts %{_platform_bin_path} && cd -

%files
%defattr(0755,root,root)
%{_python_site_packages_path}/caas_logging*
%{_python_site_packages_path}/yarf/handlers/caas_logging*
/opt/cmframework/activators/caasactivator.py*

%pre

%post

%preun

%postun

%clean
rm -rf %{buildroot}
