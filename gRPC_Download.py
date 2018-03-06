import Commons
import Exceptions
import shutil
import sys


def check_dependencies() -> None:
    """
    Checks that all the gRPC dependencies, listed in configuration file, are installed and available in PATH.
    If one of them is missing, an MissingDependency is raised.
    """
    import configparser
    dependencies_file = configparser.ConfigParser()
    dependencies_file.read('Dependencies.ini')

    for section in dependencies_file.sections():

        program_name: str = dependencies_file[section]['Exe']
        if not shutil.which(program_name):
            raise Exceptions.MissingDependency(f'"{ program_name }" is required.')
        else:
            Commons.print_success(__file__, f'Program { program_name } is present.')


if __name__ == '__main__':

    import time
    start: float = time.time()

    import colorama
    # To get colors in Windows cmd.
    colorama.init(autoreset = True)

    try:
        Commons.print_message(__file__, f'Checking all required dependencies.')
        # First, we want to be sure to have everything.
        check_dependencies()

        # After, we need to make some cleaning.
        import os
        if os.path.isdir(Commons.REPOSITORY_DIRECTORY) and os.listdir(Commons.REPOSITORY_DIRECTORY):
            Commons.print_message(__file__, 'Cleaning the git repository directory first.')
            os.system(f'rmdir /S /q "{ Commons.REPOSITORY_DIRECTORY }"')
            Commons.print_message(__file__, 'Cleaning done.')

        from configparser import ConfigParser
        configuration: ConfigParser = ConfigParser()
        configuration.read('Configuration.ini')

        # The repository to clone can be changed in the settings, to allow building other versions that the last master.
        repository_url: str = configuration['gRPC Repository']['Url']
        version_tag: str = configuration['gRPC Tag'].get('Tag')

        import subprocess

        # Cloning the repository from GitHub.
        tag_message: str = ''
        if version_tag:
            tag_message = f' with tag { colorama.Fore.MAGENTA }{ version_tag }{ colorama.Style.RESET_ALL }'

        Commons.print_message(__file__, f'Cloning git repository from { colorama.Fore.MAGENTA }{ repository_url }{ colorama.Style.RESET_ALL }{ tag_message }.')
        clone_process: subprocess.Popen = None
        if version_tag:
            clone_process = subprocess.Popen(['git', 'clone', '--recursive', '--branch', version_tag, repository_url, '--depth', '1', Commons.REPOSITORY_DIRECTORY], stdout = sys.stdout, stderr = sys.stderr)
        else:
            clone_process = subprocess.Popen(['git', 'clone', repository_url, Commons.REPOSITORY_DIRECTORY], stdout = sys.stdout, stderr = sys.stderr)
        clone_process.communicate()
        Commons.print_message(__file__, f'gRPC successfully cloned into { colorama.Fore.CYAN }{ Commons.REPOSITORY_DIRECTORY }{ colorama.Style.RESET_ALL }.')

        # Gets the source code of gRPC dependencies.
        Commons.print_message(__file__, 'Updating the submodules.')
        update_process: subprocess.Popen = subprocess.Popen(['git', 'submodule', 'update', '--init'], stdout = sys.stdout, stderr = sys.stderr)
        update_process.communicate()
        Commons.print_success(__file__, 'Submodules updated successfully.')

    except Exceptions.MissingDependency as exception:
        Commons.print_failure(__file__, f'A program is missing: { exception }')

    total: float = time.time() - start
    minutes, seconds = divmod(total, 60)
    Commons.print_message(__file__, f'Program executed in {minutes:02.02f} minutes {seconds:02.02f} seconds')