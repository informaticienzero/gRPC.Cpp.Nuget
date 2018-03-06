# gRPC C++ NuGet #

This project is a collection of Python scripts to **download and build gRPC**, and then **generate a native NuGet** usable in Visual Studio. By default,
the [Google repository](https://github.com/grpc/grpc) provides neither NuGet nor binaries to use gRPC in C++.  

The goal of this project is then to provides, within a collection of Python scripts, a clear way to compile gRPC and generate a NuGet with the parameters
of your choice. It will do the job automatically for you, but still allows you **to choose the repository** to clone and compile (in order to generate a specific
version of gRPC), the **compiler to use** and also the **toolset**. The NuGet is also configurable to fit the best to your needs.

I compile gRPC with [Visual Studio 2017](https://www.visualstudio.com/downloads/), but it should works with other versions of VS and other compilers. However,
I can't certify it. Feel free to open issues and submit pull requests to improve the project.

## Installation ##
### Pre-requisites ###

* **[Python 3.6+](https://www.python.org/downloads/release/python-360/)** (I use type hints, you'll have to delete them to use older version of Python).
* **[git](https://git-scm.com/)** to clone the repository, both this one and the gRPC one.
* **[cmake](https://cmake.org/download/)** (required by gRPC).
* **[go](https://golang.org/dl/)** (required by gRPC).
* **[perl](https://www.activestate.com/activeperl/)** (required by gRPC).

### Configure the project ###

```
git clone https://github.com/informaticienzero/gRPC.Cpp.Nuget
cd gRPC.Cpp.Nuget

# Create a virtual env first. Really, it's better.
pip install -r requirements.txt
```

### Build gRPC ###

```
# Checks dependencies and download the gRPC repository setted in Configuration.ini.
python .\gRPC_Download.py

# Compiles gRPC with the parameters given in Configuration.ini.
python .\gRPC_Build.py
```
