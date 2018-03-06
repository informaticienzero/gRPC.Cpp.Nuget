import colorama
import Commons
import os
import shutil

from typing import List, Tuple


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


def copy_folder_recursively(source: str, destination: str) -> None:
    """
    Copies a folder recursively, with all the sub-folders and files in it.
    Found here: https://stackoverflow.com/a/1994840/6060256
    """
    import errno

    try:
        shutil.copytree(source, destination)
    except OSError as exception:
        if exception.errno == errno.ENOTDIR:
            shutil.copy(source, destination)
        else:
            raise


def create_and_copy(source: str, destination: str) -> None:
    """
    Creates the destination folder if doesn't exist, or clean it first if already present.
    """
    delete_folder(destination, print_info = True)
    copy_folder_recursively(source, destination)


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

            toolset_option: str = ''
            if toolset:
                toolset_option = f'-T { toolset }'

            os.system(f'cmake "{ Commons.REPOSITORY_DIRECTORY }" -G "{ generator }" { toolset_option } -DCMAKE_BUILD_TYPE={ build_configuration } -DgRPC_BUILD_TESTS=OFF -DgRPC_INSTALL=FALSE')
            os.system(f'cmake --build . --config { build_configuration }')

            Commons.print_success(__file__, f'{ build_configuration } build finished successfully.')

            # Copying include folder.
            Commons.print_message(__file__, 'Copying #include folders.')

            protobuf_directory: str = os.path.join(Commons.REPOSITORY_DIRECTORY, r'third_party\protobuf\src\google\protobuf')
            output_protobuf_directory: str = os.path.join(Commons.OUTPUT_DIRECTORY, r'include\google\protobuf')

            create_and_copy(os.path.join(Commons.REPOSITORY_DIRECTORY, r'include'), os.path.join(Commons.OUTPUT_DIRECTORY, r'include'))
            create_and_copy(os.path.join(protobuf_directory, r'stubs'), os.path.join(output_protobuf_directory, r'stubs'))
            create_and_copy(os.path.join(protobuf_directory, r'io'), os.path.join(output_protobuf_directory, r'io'))

            # Now we need to copy all files at root of the protobuf directory.
            for file in os.listdir(protobuf_directory):
                if file.endswith('.h') or file.endswith('.cc'):
                    shutil.copy2(os.path.join(protobuf_directory, file), output_protobuf_directory)

            Commons.print_success(__file__, 'All #include folders successfully copied.')

            # Copying binaries.
            Commons.print_message(__file__, 'Copying binaries.')
            
            bin_output_directory: str = os.path.join(Commons.OUTPUT_DIRECTORY, f'bin\{ build_configuration }\google')
            os.makedirs(bin_output_directory)

            shutil.copy2(os.path.join(build_folder, f'third_party\protobuf\{ build_configuration }\protoc.exe'), bin_output_directory)
            shutil.copy2(os.path.join(build_folder, f'{ build_configuration }\grpc_cpp_plugin.exe'), bin_output_directory)

            Commons.print_success(__file__, 'Successfully copied binaries.')

            # Copying static libraries.
            Commons.print_message(__file__, 'Copying static libraries.')

            output_libraries_directory: str = os.path.join(Commons.OUTPUT_DIRECTORY, f'lib\{ build_configuration }\google')
            os.makedirs(output_libraries_directory)

            # We need to rename some libs because they have 'd' inside them in Debug.
            if build_configuration == 'Debug':
                shutil.copyfile(os.path.join(build_folder, r'third_party\protobuf\Debug\libprotobufd.lib'), os.path.join(output_libraries_directory, r'libprotobuf.lib'))
                shutil.copyfile(os.path.join(build_folder, r'third_party\protobuf\Debug\libprotocd.lib'), os.path.join(output_libraries_directory, r'libprotoc.lib'))
                shutil.copyfile(os.path.join(build_folder, r'third_party\zlib\Debug\zlibd.lib'), os.path.join(output_libraries_directory, r'zlib.lib'))
                shutil.copyfile(os.path.join(build_folder, r'third_party\zlib\Debug\zlibstaticd.lib'), os.path.join(output_libraries_directory, r'zlibstatic.lib'))
            else:
                shutil.copy2(os.path.join(build_folder, r'third_party\protobuf\Release\libprotobuf.lib'), output_libraries_directory)
                shutil.copy2(os.path.join(build_folder, r'third_party\protobuf\Release\libprotoc.lib'), output_libraries_directory)
                shutil.copy2(os.path.join(build_folder, r'third_party\zlib\Release\zlib.lib'), output_libraries_directory)
                shutil.copy2(os.path.join(build_folder, r'third_party\zlib\Release\zlibstatic.lib'), output_libraries_directory)

            shutil.copy2(os.path.join(build_folder, r'third_party\boringssl\crypto\{}\crypto.lib'.format(build_configuration)), output_libraries_directory)
            shutil.copy2(os.path.join(build_folder, r'third_party\boringssl\ssl\{}\ssl.lib'.format(build_configuration)), output_libraries_directory)
            shutil.copy2(os.path.join(build_folder, f'{ build_configuration }\gpr.lib'), output_libraries_directory)
            shutil.copy2(os.path.join(build_folder, f'{ build_configuration }\grpc.lib'), output_libraries_directory)
            shutil.copy2(os.path.join(build_folder, f'{ build_configuration }\grpc++.lib'), output_libraries_directory)
            shutil.copy2(os.path.join(build_folder, f'{ build_configuration }\grpc++_error_details.lib'), output_libraries_directory)
            shutil.copy2(os.path.join(build_folder, f'{ build_configuration }\grpc++_reflection.lib'), output_libraries_directory)
            # TEMP: to investigate in order to know what is the problem with those two.
            #shutil.copy2(os.path.join(build_folder, f'{ build_configuration }\grpc_unsecure.lib'), output_libraries_directory)
            #shutil.copy2(os.path.join(build_folder, f'{ build_configuration }\grpc++_unsecure.lib'), output_libraries_directory)

            Commons.print_success(__file__, 'Static libraries successfully copied.')

    except OSError as exception:
        Commons.print_failure(__file__, f'Got an I/O error: { exception }.')
    except Exception as exception:
        Commons.print_failure(__file__, f'An error occurred: { exception }.')

    total: float = time.time() - start
    minutes, seconds = divmod(total, 60)
    Commons.print_message(__file__, f'Program executed in {minutes:02.02f} minutes {seconds:02.02f} seconds')