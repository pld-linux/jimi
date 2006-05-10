%define cvs_version     %(echo %{version} | tr . _)
Summary:	Java imaging toolkit
Name:		jimi
Version:	1.0
Release:	0.1
License:	Sun Binary Code License
Group:		Development/Languages/Java
URL:		http://java.sun.com/products/jimi/
Source0:	%{name}%{cvs_version}.zip
# NoSource0-md5:	9cf0b3422b4cbd88e57ee159bc29973f
NoSource:	0
BuildRequires:	/usr/bin/perl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JIMI Software Development Kit Jimi is a class library for managing
images. Its primary function is image I/O. Jimi was formerly a product
of Activated Intelligence. Sun is making it available for developers
who have code with dependencies on Jimi or for those who need image
I/O functionality in applications running under 1.1.x versions of the
JavaTM Platform. Jimi's range of supported formats includes GIF, JPEG,
TIFF, PNG, PICT, Photoshop, BMP, Targa, ICO, CUR, Sunraster, XBM, XPM,
and PCX, although some of these formats do not have complete support
for all features.

%package manual
Summary:	Manual for %{name}
Group:		Development/Languages/Java

%description manual
Documentation for %{name}.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%package demo
Summary:	Demo for %{name}
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n Jimi

# use jar archive
unzip -q JimiProClasses.zip
jar cf %{name}.jar com
# correct examples
find examples -name "*.bat" -exec rm -f {} ';'
for file in `find examples -name *.html`; do
  perl -pi -e 's/JimiProClasses\.jar/jimi.jar/' $file
done
for file in `find examples -name *.sh`; do
	perl -pi -e 's|\$CLASSPATH:[./:]*JimiProClasses\.zip[./:]*|\$CLASSPATH:%{_javadir}/jimi.jar:.|' $file
done

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && ln -sf %{name}-%{version}.jar %{name}.zip)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/html/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf docs/html/api

# data
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr examples $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc License Readme
%{_javadir}/*

%files manual
%defattr(644,root,root,755)
%doc docs/html/*

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}

%files demo
%defattr(644,root,root,755)
%{_datadir}/%{name}
