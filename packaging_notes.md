I still don't fully understand the behavior of importing modules which are subdirectories of your current directory. You can access scripts that are in the subdirectories if you explicitly name them, but if you name the subdirectory itself, you don't get any access to those scripts.

It's possible that part of the reason why is that the package that is that directory has to be initialized. However, it seeems that this is not the way to make a package in the first place.

# How to make a package

1. Make a folder for the top-level. If these scripts comprise an entire project, then make a folder within your project folder, as running scripts using package notation requires that you run the python interpretor from outside of the top-level directory.
2. For each subpackage or submodule (including the top level package), include all scripts that you want as members of that module. 
3. Within each directory include a file named `__init__.py` (that's two underscores on either side of `init`). This file may be completely empty, but it still has to exist. It tells the python interpreter that these directories represent packages.

Finally, to run a script from the package use the following command:
```bash
python -m pkg_name.subpackage_name.module_name
```

Where you add as many `subpackage_name` as necssary to reach the module from the top level of the package.
