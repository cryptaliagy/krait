# Changelog


## 0.6.2

### New

* Installed templates in config directory. BREAKING CHANGE. Must re-configure krait on upgrade. [Natalia Maximo]

### Changes

* Added config clean step to CI. [Natalia Maximo]

* Added debug prompt. [Natalia Maximo]

### Fix

* Resolved issue with update time on windows. [Natalia Maximo]

* Patched tests that used wrong install directory. [Natalia Maximo]

* Updated test to use proper directory. [Natalia Maximo]

* Converted path to string in template loader. [Natalia Maximo]

* Py3.6/3.7 compatibility with pathish type. [Natalia Maximo]


## 0.6.1 (2020-12-17)

### New

* Added azure pipelines to krait generations. [Natalia Maximo]


## 0.6 (2020-12-17)

### New

* Added 'krait reset' command. [Natalia Maximo]

* Added vcs support for git (#5) [Natalia Maximo]

  * new: added vcs support for git, resolves #1

  * chg: added gitpython to setup requirements
  * new: integrated .gitignore rendering, resolves #2

### Changes

* Removed finished tasks from readme file. [Natalia Maximo]

* Better error messaging and default name/email selection. [Natalia Maximo]

* Added codeowner file. [Natalia Maximo]

* Reverted variable name. [Fernando Nogueira]

* Refactored imports. [SeoFernando25]

* Fixed undeclared variable. [SeoFernando25]

* Explicitly disabled autoescape. [SeoFernando25]

* Added .vscode to .gitignore. [SeoFernando25]

* Renamed repeated variable at L57 and L458. [SeoFernando25]

* Reordered imports. [SeoFernando25]

* Refactoring. [SeoFernando25]

* Reordered imports to comply with PEP 8. [Fernando Nogueira]

* Simplified bool comparisons. [Fernando Nogueira]

* Added release gha status badge. [Natalia Maximo]

### Fix

* Resolved issue with the set-output command in gha. [Natalia Maximo]

* Added pattern to codeowners file. [Natalia Maximo]

### Other

* Revert "chg: Added .vscode to .gitignore" [Fernando Nogueira]

  This reverts commit d9a7894e482f29621cfe1e0873974a8327fb4070.

* Revert "chg: refactoring" [SeoFernando25]

  This reverts commit 3c58b13a636fe567a2ece12eeb8779f33e90c9dc.


## 0.5 (2020-12-12)

### Changes

* Added more tests to release process. [Natalia Maximo]

* Added new pytests and automated test steps. [Natalia Maximo]

* Reworked how library projects are created. [Natalia Maximo]

### Fix

* Corrected error in workflow file. [Natalia Maximo]

* Corrected release issues for windows. [Natalia Maximo]

* Corrected lib_test logic with pytest fixture. [Natalia Maximo]

* Changed main to lib on pytest-library-lib_test.py. [Natalia Maximo]

* Missing pytest mark on generated lib_test.py. [Natalia Maximo]

* Spacing issues and runner issue. [Natalia Maximo]

* Only setup entry points if its a cli app. [Natalia Maximo]

* Used correct krait command in CI tests. [Natalia Maximo]

* Fixed exclude directory for pycache on flake8 configs. [Natalia Maximo]

### Other

* Dev: possible fix for gha release. [Natalia Maximo]

* Dev: debugging release. [Natalia Maximo]

* Doc: updated readme. [Natalia Maximo]


## 0.4 (2020-12-11)

### New

* Added update cooldown configs and support for using 'python -m krait' [Natalia Maximo]

* Added configuration system. [Natalia Maximo]

* Added 'krait update' command. [Natalia Maximo]

### Changes

* Reworked 'cli framework' to 'project type' [Natalia Maximo]

* Bumped up version because of the number of changes. [Natalia Maximo]

* Dev status is now beta. [Natalia Maximo]

* Added downloads badge. [Natalia Maximo]

### Fix

* Use float for timestamp instead of int. [Natalia Maximo]

* Use timestamp instead of iso format for py3.6 compatibility. [Natalia Maximo]

* Added pydeepmerge to requirements. [Natalia Maximo]

* Changed release name to appropriate project name. [Natalia Maximo]


## 0.3.4 (2020-12-09)

### New

* Changelog generation. [Natalia Maximo]

### Fix

* Bump version for release. [Natalia Maximo]

* Updated release process for new github env variable system. [Natalia Maximo]

* Bump version for release. [Natalia Maximo]

* Fixed wrong changelog version. [Natalia Maximo]


## 0.3.1 (2020-12-08)

### New

* Added license badge to redme file. [Natalia Maximo]

* Added license info to setup.py. [Natalia Maximo]

* Added license. [Natalia Maximo]

* Added more interactive output and silencing option. [Natalia Maximo]

* Automatic update checking. [Natalia Maximo]

* Readme updates. [Natalia Maximo]

* Added help link plugins. [Natalia Maximo]

* Github actions support. [Natalia Maximo]

* Added linter and type checker configs. [Natalia Maximo]

* Can prompt for user input, suppress prompt, and render basic cli and cli_test. [Natalia Maximo]

* Render basic main.py, readme and setup script. [Natalia Maximo]

* Create empty common files. [Natalia Maximo]

* Krait plugin system. [Natalia Maximo]

* Set-default and help commands. [Natalia Maximo]

### Changes

* Upped version for release. [Natalia Maximo]

* Project metadata update. [Natalia Maximo]

* Disabled set-default command. [Natalia Maximo]

* Flattened structure slightly, will expand when necessary. [Natalia Maximo]

* Made 'krait' be a command group instead of a single command according to design doc. [Natalia Maximo]

* Added basic description to package. [Natalia Maximo]

* Used install_requires with no version info. [Natalia Maximo]

### Fix

* Version bump for release. [Natalia Maximo]

* Ensure 'none' appears as last item in options. [Natalia Maximo]

* Python <3.8 compatibility. removed walrus operator. [Natalia Maximo]

* Using dashes in project name no longer causes errors. [Natalia Maximo]

* Fixed up some testing issues. [Natalia Maximo]

* Test framework rendering file in incorrect location. [Natalia Maximo]

* Fixed test and added missing file. [Natalia Maximo]

* Type annotation on setupscript class. [Natalia Maximo]

* Added manifest file and included package data in setup script. [Natalia Maximo]

* Added jinja2 to dependency for project. [Natalia Maximo]

* Made click default and fixed template error. [Natalia Maximo]

* Wrong name on github actions. [Natalia Maximo]

* Setup.cfg fix. [Natalia Maximo]

### Other

* Dev: setup of project repository. [Natalia Maximo]

* Initial commit. [Natalia Maximo]
