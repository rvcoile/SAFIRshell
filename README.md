# SAFIRshell

SAFIRshell is a Python tool to support computations with the finite element solver SAFIR.

## Getting Started

### Prerequisites

[Safir 2016](https://www.uee.uliege.be/cms/c_2383458/en/safir);

[Python 3.6](https://www.anaconda.com/download/) or later; and

The following Python libraries:

```sh
numpy==1.15.0
pandas==0.23.3
scipy==1.1.0
```

### Installation

#### pip

pip is a package management system for installing and updating Python packages. pip comes with Python, so you get pip simply by installing Python. On Ubuntu and Fedora Linux, you can simply use your system package manager to install the `python3-pip` package. [The Hitchhiker's Guide to Python ](https://docs.python-guide.org/starting/installation/) provides some guidance on how to install Python on your system if it isn't already; you can also install Python directly from [python.org](https://www.python.org/getit/). You might want to [upgrade pip](https://pip.pypa.io/en/stable/installing/) before using it to install other programs.

SAFIRshell uses Python3. 

1.	If you are using Windows with Python version 3.3 or higher, use the [Python Launcher for Windows](https://docs.python.org/3/using/windows.html?highlight=shebang#python-launcher-for-windows) to use `pip` with Python version 3:
    ```sh
    pip install safirshell
    ```
2.	If your system has a `python3` command (standard on Unix-like systems), install with:
    ```sh
    python3 -m pip install safirshell
    ```
3.	You can also just use the `python` command directly, but this will use the _current_ version of Python in your environment:
    ```sh
    python -m pip install safirshell
    ```

### Usage

To run a single SAFIR calculation, use the following commands.

```sh
python -m SAFIRshell.shell
```

## Authors

* **Ruben Van Coile** - *ruben.vancoile@gmail.com*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
