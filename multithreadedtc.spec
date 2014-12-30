%{?_javapackages_macros:%_javapackages_macros}
%global project_name MultithreadedTC
Name:           multithreadedtc
Version:        1.01
Release:        18.1
Summary:        A framework for testing concurrent Java application
Group:          Development/Java
License:        BSD 
URL:            http://www.cs.umd.edu/projects/PL/multithreadedtc
#http://multithreadedtc.googlecode.com/files/MultithreadedTC-1.01-source.zip
Source0:        %{project_name}-%{version}-source.zip
Source1:        %{name}.pom
Patch0:         %{name}-build.patch

BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: ant >= 0:1.6
BuildRequires: ant-junit
BuildRequires: junit

Requires:      java
Requires:      jpackage-utils
Requires:      junit

%description
MultithreadedTC is a framework for testing concurrent applications. 
It features a metronome that is used to provide fine control over
the sequence of activities in multiple threads.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{project_name}-%{version}-source
%patch0 -p0 -b .sav

find . -name "*.class" -print -delete
find . -name "*.jar" -print -delete

sed -i 's/\r//' web/docs/package-list
sed -i 's/\r//' web/docs/stylesheet.css
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' README.txt

%build
ant

%install

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 %{project_name}-%{version}.jar   %{buildroot}%{_javadir}/%{project_name}.jar

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} \
    %{buildroot}%{_mavenpomdir}/JPP-%{project_name}.pom
%add_maven_depmap JPP-%{project_name}.pom %{project_name}.jar -a "edu.umd.cs.mtc:multithreadedtc-jdk14,com.googlecode.multithreadedtc:multithreadedtc"

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr web/docs/* %{buildroot}%{_javadocdir}/%{name}/
rm -rf web/docs

%files -f .mfiles
%doc LICENSE.txt README.txt
%{_javadir}/*
%{_mavenpomdir}/*

# Workaround for rpm bug, remove in F23
%pre javadoc
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Mon Aug 12 2013 gil cattaneo <puntogil@libero.it> - 1.01-15
- fix rhbz#992389
- update to current packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Hui Wang <huwang@redhat.com> 1.01-9
- Revert name in add_to_maven_depmap macro call
- Fix pom's name of %%mavenpomdir dir

* Thu Nov 25 2010 Hui Wang <huwang@redhat.com> 1.01-8
- Fix name in add_to_maven_depmap macro call

* Wed Jun 2 2010 Alexander Kurtakov <akurtako@redhat.com> 1.01-7
- BR ant-junit.

* Wed Jun 2 2010 Alexander Kurtakov <akurtako@redhat.com> 1.01-6
-  BR/R junit.

* Wed Jun 2 2010 Alexander Kurtakov <akurtako@redhat.com> 1.01-5
- Fix build.xml to really compile sources.
- Fix depmap.

* Thu May 27 2010 Hui Wang <huwang@redhat.com> 1.01-4
- Fix LICENSE and txt README.txt encoding
- Delete jar files in pre section

* Thu May 27 2010 Hui Wang <huwang@redhat.com> 1.01-3
- Add multithreadedtc-jdk14 to maven depmap

* Thu May 27 2010 Hui Wang <huwang@redhat.com> 1.01-2
- Using MultithreadedTC-1.01-source.zip as source0
- Add demap.xml
- Add missing requires
- Remove ls-lR
- Fix description line length
- Add LICENSE.txt README.txt in doc section
- Fix javadoc encoding

* Tue May 25 2010 Hui Wang <huwang@redhat.com> 1.01-1
- Initial version of the package
