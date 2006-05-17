%define cvs_version     %(echo %{version} | tr . _)
Summary:	Java imaging toolkit
Summary(pl):	Biblioteka do obrazków w Javie
Name:		jimi
Version:	1.0
Release:	0.1
License:	Sun Binary Code License
Group:		Development/Languages/Java
Source0:	%{name}%{cvs_version}.zip
# NoSource0-md5:	9cf0b3422b4cbd88e57ee159bc29973f
NoSource:	0
URL:		http://java.sun.com/products/jimi/
BuildRequires:	perl-base
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JIMI Software Development Kit is a class library for managing images.
Its primary function is image I/O. Jimi was formerly a product of
Activated Intelligence. Sun is making it available for developers who
have code with dependencies on Jimi or for those who need image I/O
functionality in applications running under 1.1.x versions of the
Java(TM) Platform. Jimi's range of supported formats includes GIF,
JPEG, TIFF, PNG, PICT, Photoshop, BMP, Targa, ICO, CUR, Sunraster,
XBM, XPM, and PCX, although some of these formats do not have complete
support for all features.

%description -l pl
JIMI SDK to biblioteka klas do zarz±dzania obrazkami. G³ówn± jej
funkcj± s± operacje we/wy na obrazkach. Poprzednio by³ to produkt
firmy Activated Intelligence. Sun udostêpnia bibliotekê dla
programistów posiadaj±cych kod zale¿±cy od biblioteki Jimi oraz dla
tych, którzy potrzebuj± funkcjonalno¶ci we/wy dla obrazków w
aplikacjach dzia³aj±cych pod kontrol± wersji 1.1.x platformy Java(TM).
Jimi obs³uguje formaty graficzne GIF, JPEG, TIFF, PNG, PICT,
Photoshop, BMP, Targa, ICO, CUR, Sunraster, XBM, XPM i PCX, choæ
niektóre z tych formatów nie maj± pe³nej obs³ugi niektórych
w³a¶ciwo¶ci.

%package manual
Summary:	Manual for %{name}
Summary(pl):	Podrêcznik dla pakietu %{name}
Group:		Development/Languages/Java

%description manual
Documentation for %{name}.

%description manual -l pl
Dokumentacja dla pakietu %{name}.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl
Dokumentacja javadoc dla pakietu %{name}.

%package demo
Summary:	Demo for %{name}
Summary(pl):	Programy demonstracyjne dla pakietu %{name}
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%description demo -l pl
Programy demonstracyjne i przyk³adowe dla pakietu %{name}.

%prep
%setup -q -n Jimi

# use jar archive
unzip -q JimiProClasses.zip
jar cf %{name}.jar com
# correct examples
find examples -name "*.bat" -exec rm -f {} ';'
for file in `find examples -name *.html`; do
	%{__perl} -pi -e 's/JimiProClasses\.jar/jimi.jar/' $file
done
for file in `find examples -name *.sh`; do
	%{__perl} -pi -e 's|\$CLASSPATH:[./:]*JimiProClasses\.zip[./:]*|\$CLASSPATH:%{_javadir}/jimi.jar:.|' $file
done

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cd $RPM_BUILD_ROOT%{_javadir}
ln -sf %{name}-%{version}.jar %{name}.zip
for jar in *-%{version}.jar; do
	ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
done
cd -

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
