import colorama
import Commons
import os


def delete_folder(folder_path: str, print_info = False) -> None:
    """
    Checks if the path is really a directory and then deletes it.
    """
    if os.path.isdir(folder_path) and os.listdir(folder_path):
        if print_info:
            Commons.print_message(__file__, f'Cleaning { colorama.Fore.CYAN }{ folder_path }{ colorama.Style.RESET_ALL } first.')

        os.system(f'rmdir /S /q "{ folder_path }"')

        if print_info:
            Commons.print_message(__file__, f'Cleaning done.')


if __name__ == "__main__":

    import time
    start: float = time.time()

    # To get colors in Windows cmd.
    colorama.init(autoreset = True)

    try:
        from configparser import ConfigParser
        configuration: ConfigParser = ConfigParser()
        configuration.read('Configuration.ini')

        generator: str = configuration['Generator']['Value']
        toolset: str = configuration['Toolset'].get('Value')

        # Cleaning the output directory first.
        delete_folder(Commons.OUTPUT_DIRECTORY, print_info = True)
        
        # Creating output repertories.
        os.makedirs(Commons.OUTPUT_DIRECTORY, exist_ok = True)
        os.mkdir(os.path.join(Commons.OUTPUT_DIRECTORY, r'bin'))
        os.mkdir(os.path.join(Commons.OUTPUT_DIRECTORY, r'lib'))
        os.mkdir(os.path.join(Commons.OUTPUT_DIRECTORY, r'include'))
        os.mkdir(os.path.join(Commons.OUTPUT_DIRECTORY, r'include\google'))
        os.mkdir(os.path.join(Commons.OUTPUT_DIRECTORY, r'include\google\protobuf'))

        # Building gRPC.
        for build_configuration in ['Debug']:

            Commons.print_message(__file__, f'Building gRPC in { colorama.Fore.YELLOW }{ build_configuration }{ colorama.Style.RESET_ALL }.')
            Commons.print_message(__file__, f'Generator is: { colorama.Fore.YELLOW }{ generator }{ colorama.Style.RESET_ALL }.')
            Commons.print_message(__file__, f'Toolset is: { colorama.Fore.YELLOW }{ toolset }{ colorama.Style.RESET_ALL }.')

            # Cmake will output some files in that folder.
            build_folder: str = os.path.join(Commons.REPOSITORY_DIRECTORY, f'.{ build_configuration }')
            delete_folder(build_folder, print_info = True)
            os.makedirs(build_folder, exist_ok = True)

            # Launch the build.
            Commons.print_message(__file__, 'Launching the build.')
            os.chdir(build_folder)

            if toolset:
                os.system(f'cmake "{ Commons.REPOSITORY_DIRECTORY }" -G "{ generator }" -T { toolset } -DCMAKE_BUILD_TYPE={ build_configuration } -DgRPC_BUILD_TESTS=OFF -DgRPC_INSTALL=FALSE')
            else:
                os.system(f'cmake "{ Commons.REPOSITORY_DIRECTORY }" -G "{ generator }" -DCMAKE_BUILD_TYPE={ build_configuration } -DgRPC_BUILD_TESTS=OFF -DgRPC_INSTALL=FALSE')

            os.system(f'cmake --build . --config { build_configuration }')
            Commons.print_success(__file__, 'Build finished successfully.')


    except Exception as exception:
        Commons.print_failure(__file__, f'An error occurred: { exception }.')

    total: float = time.time() - start
    minutes, seconds = divmod(total, 60)
    Commons.print_message(__file__, f'Program executed in {minutes:02.02f} minutes {seconds:02.02f} seconds')