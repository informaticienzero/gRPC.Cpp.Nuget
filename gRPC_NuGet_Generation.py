import Commons
import os
import shutil
import subprocess
import sys
import time


if __name__ == '__main__':

    start: float = time.time()
    Commons.print_message(__file__, 'Launching the NuGet generation script.')

    shutil.copy('gRPC.autopkg', Commons.OUTPUT_DIRECTORY)
    
    os.chdir(Commons.OUTPUT_DIRECTORY)
    process = subprocess.Popen(['powershell.exe', 'Write-NuGetPackage', 'gRPC.autopkg'], stdout = sys.stdout)
    process.communicate()

    total: float = time.time() - start
    minutes, seconds = divmod(total, 60)
    Commons.print_success(__file__, f'NuGet package successfully generated.')
    Commons.print_message(__file__, f'Program executed in {minutes:02.02f} minutes {seconds:02.02f} seconds')