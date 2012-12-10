%global project_name MultithreadedTC
Name:           multithreadedtc
Version:        1.01
Release:        12
Summary:        A framework for testing concurrent Java application

Group:          Development/Java
License:        BSD 
URL:            http://www.cs.umd.edu/projects/PL/multithreadedtc
#http://multithreadedtc.googlecode.com/files/MultithreadedTC-1.01-source.zip
Source0:        %{project_name}-%{version}-source.zip
Source1:        %{name}.pom
Patch0:        %{name}-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: jpackage-utils
BuildRequires: ant >= 0:1.6
BuildRequires: ant-junit
BuildRequires: junit

Requires:      java
Requires:       jpackage-utils
Requires:      junit

Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

%description
MultithreadedTC is a framework for testing concurrent applications. 
It features a metronome that is used to provide fine control over
the sequence of activities in multiple threads.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils 

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{project_name}-%{version}-source
%patch0 -p0 -b .sav

rm -f *.jar

sed -i 's/\r//' web/docs/package-list
sed -i 's/\r//' web/docs/stylesheet.css
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' README.txt

%build
ant

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 %{project_name}-%{version}.jar   %{buildroot}%{_javadir}/%{project_name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap edu.umd.cs.mtc multithreadedtc %{version} JPP %{project_name}
%add_to_maven_depmap edu.umd.cs.mtc multithreadedtc-jdk14 %{version} JPP %{project_name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} \
    %{buildroot}%{_mavenpomdir}/JPP-%{project_name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr web/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf web/docs

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}



%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 1.01-12
+ Revision: 734182
- rebuild
- imported package multithreadedtc

