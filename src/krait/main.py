# -*- coding: utf-8 -*-
import logging
import pathlib

import krait.lib.renderers as rndr
import krait.lib.files as kf
import krait.lib.plugins.project_frameworks as kproj
import krait.lib.plugins.test_frameworks as ktest
import krait.lib.plugins.type_checkers as ktype
import krait.lib.plugins.linters as klint
import krait.lib.plugins.automations as kauto


logging.basicConfig(level=logging.INFO)


def create(
    project_name: str,
    author: str,
    email: str,
    linter: klint.BaseLinter,
    type_checker: ktype.BaseTypeChecker,
    automation: kauto.BaseAutomation,
    test_framework: ktest.BaseTestFramework,
    project_framework: kproj.BaseProjectFramework,
    directories: rndr.DirectoryRenderer,
    files: rndr.FileRenderer,
):
    '''
    Create a new python project with the specified options
    '''
    directories.add_directories(
        *map(
            lambda p: pathlib.Path(p),
            [
                'src',
                f'src/{project_name.replace("-","_")}',
                'tests'
            ]
        )
    )

    files.add_files(*map(
        lambda p: kf.File(p),
        [
            'setup.cfg',
            f'src/{project_name.replace("-","_")}/__init__.py',
            'tests/__init__.py'
        ]
    ))

    project_framework.render_file()
    test_framework.render_file()
    automation.render_file()

    readme_file = kf.File('README.md', f'# {project_name}')
    setup_script = kf.SetupScript(
        project_name,
        author,
        email,
        project_framework,
        linter,
        type_checker,
        test_framework
    )
    setup_config = kf.SetupConfig(
        project_framework,
        linter,
        type_checker,
        test_framework,
    )
    manifest_file = kf.File('MANIFEST.in', 'graft src')

    files.add_file(readme_file)
    files.add_file(setup_script)
    files.add_file(setup_config)
    files.add_file(manifest_file)
    directories.create_all()
    files.write_all()
