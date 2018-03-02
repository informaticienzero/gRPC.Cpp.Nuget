import Commons
import Exceptions
import git
import shutil


class GitCloneProgress(git.RemoteProgress):
    """
    Used to show in real-time progress of the git clone.
    """
    def line_dropped(self, line: str):
        print(line)

    def update(self, *args):
        print(self._cur_line)


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
            os.rmdir(Commons.REPOSITORY_DIRECTORY)


        from configparser import ConfigParser
        configuration: ConfigParser = ConfigParser()
        configuration.read('Configuration.ini')

        # The repository to clone can be changed in the settings, to allow building other versions that the last master.
        repository_url: str = configuration['gRPC Repository']['Url']

        # Cloning the repository from GitHub.
        Commons.print_message(__file__, f'Cloning git repository from { colorama.Fore.MAGENTA }{ repository_url }{ colorama.Style.RESET_ALL }.')
        repository: git.Repo = git.Repo.clone_from(repository_url, Commons.REPOSITORY_DIRECTORY, progress = GitCloneProgress())
        Commons.print_message(__file__, f'gRPC successfully cloned into { colorama.Fore.CYAN }{ Commons.REPOSITORY_DIRECTORY }{ colorama.Style.RESET_ALL }.')

        # git update submodules --init
        Commons.print_message(__file__, 'Updating the submodules.')
        print(repository.git.submodule('update', '--init'))
        Commons.print_success(__file__, 'Submodules updated successfully.')

    except Exceptions.MissingDependency as exception:
        Commons.print_failure(__file__, f'A program is missing: { exception }')

    total: float = time.time() - start
    minutes, seconds = divmod(total, 60)
    Commons.print_message(__file__, f'Program executed in {minutes:02.02f} minutes {seconds:02.02f} seconds')