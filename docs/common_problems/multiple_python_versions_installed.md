# Multiple Python versions installed on the target

### Error Messages
Multiple different error messages:
> Python package not available

> cannot import name _function_ from _python_package_ 

### Problem
The most common causes of this error message is:

* You have a very recent (development) release of Python installed as an alternative or main Python install

### Solution
To solve this problem:

* define the Python version to use on your host by adding `ansible_python_interpreter=/usr/bin/python3` to your host line in `inventory.ini`. If needed, replace `/usr/bin/python3` with the alternative Python version installed.

### Related issues

* [Issue 299](https://github.com/geerlingguy/internet-pi/issues/299) : Install Docker Compose using Pip not working