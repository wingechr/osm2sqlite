# coding: utf-8

import sys
import os
import platform
import importlib.machinery
import subprocess
import setuptools


def build_docs(output_type, package_dir, docs_dir, docs_build_dir):
    import sphinx.apidoc
    import sphinx.cmdline

    args = [None, '-E', '-f', '-s', 'md', '-o', docs_dir, package_dir]
    sphinx.apidoc.main(args)

    kwargs = {
        'html_title': package_name,
        'htmlhelp_basename': package_name,
        'project': package_name,
        'copyright': copyright,
        'version': version
    }
    args = [None, '-q']
    for k_v in kwargs.items():
        args += ['-D', '%s=%s' % k_v]
    args += ['-b', output_type, docs_dir, docs_build_dir]
    sphinx.cmdline.main(args)


def run_tests(test_dir):
    subprocess.check_call([sys.executable, '-m', 'unittest', 'discover', '-s', test_dir])


def build_binaries():
    import cx_Freeze
    packages = setuptools.find_packages(exclude=['tests'])

    executables = []
    for sciptfile in scipt_files:
        print(sciptfile)
        script_path = os.path.join(package_dir, '%s.py' % sciptfile)
        executables.append(cx_Freeze.Executable(
            script=script_path,
            base=None,  # if no GUI
            # targetName=sciptfile + ".exe",
            compress=True,
            copyDependentFiles=True,
            initScript=None,
            targetDir=binary_dir,
            appendScriptToExe=False,
            appendScriptToLibrary=False,
            icon=icon
        ))

    cx_Freeze.setup(
        name=package_name,
        version=version,
        author=author,
        author_email=email,
        description=description,
        license=license_,
        keywords=keywords,
        url=url,
        long_description=readme,
        options={
            'build_exe': {
                "includes": requirements,
                "excludes":  [
                    'tkinter'
                ],
                "packages": packages,
                "path": [],
                'append_script_to_exe': False,
                'build_exe': binary_dir,
                'compressed': True,
                'copy_dependent_files': True,
                'create_shared_zip': True,
                'include_in_shared_zip': True,
                'optimize': 2,
                'include_files': data_dir
            }
        },
        executables=executables
    )


def build():
    packages = setuptools.find_packages(exclude=['tests'])
    setuptools.setup(
        scripts=scipt_files_long,
        install_requires=requires,
        packages=packages,
        package_data={package_name: package_data},
        name=package_name,
        version=version,
        author=author,
        author_email=email,
        description=description,
        license=license,
        keywords=keywords,
        url=url,
        long_description=readme
    )


if __name__ == '__main__':
    # collaect information
    root_dir = os.path.abspath(os.path.dirname(__file__))
    package_name = os.path.basename(root_dir)
    package_dir = os.path.join(root_dir, package_name)
    docs_dir = os.path.join(root_dir, 'docs')
    build_dir = os.path.join(root_dir, 'build')
    docs_build_dir = os.path.join(build_dir, 'docs')
    test_dir = os.path.join(root_dir, 'tests')
    init = os.path.join(package_dir, '__init__.py')
    package = importlib.machinery.SourceFileLoader(package_name, init).load_module()
    bits, op_sys = platform.architecture()
    build_platform = ('%s_%s' % (op_sys, bits)).replace(' ', '_')
    binary_dir = os.path.join(build_dir, 'bin', build_platform)
    icon = os.path.join(docs_dir, '_static', 'favicon.ico')
    icon = icon if os.path.exists(icon) else None
    with open(os.path.join(root_dir, 'README.md')) as f:
        readme = f.read()
    with open(os.path.join(root_dir, 'requirements.txt')) as f:
        requirements = [x.strip() for x in f if x.strip() != '']

    copyright = '%s <%s>' % (package.__author__, package.__email__)
    version = package.__version__
    author = package.__author__
    email = package.__email__
    description = package.__doc__
    license_ = package.__license__
    keywords = package.__keywords__
    url = package.__url__
    requires = package.__requires__
    scipt_files = package.__scripts__
    scipt_files_long = [os.path.join(package_name, '%s.py' % x) for x in scipt_files]
    data_dir = os.path.join(package_name, 'data')
    package_data = [os.path.join(dp, f) for dp, dn, fs in os.walk(data_dir) for f in fs]
    package_data = [x.replace('osm2sqlite\\', '') for x in package_data]
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command in ['doc', 'docs']:
        build_docs(output_type='singlehtml', package_dir=package_dir, docs_dir=docs_dir, docs_build_dir=docs_build_dir)
    elif command in ['test', 'tests']:
        run_tests(test_dir=test_dir)
    elif command in ['bin', 'binary']:
        sys.argv[1] = 'build'
        build_binaries()
    elif command in ['all']:
        sys.argv[1] = 'build'
        run_tests(test_dir=test_dir)
        build_docs(output_type='singlehtml', package_dir=package_dir, docs_dir=docs_dir, docs_build_dir=docs_build_dir)
        build_binaries()
        build()
    else:
        build()
