import subprocess
import sys

# String Formatter Class
class SF:
    @staticmethod
    def red(txt):
        return "\033[31m"+txt+"\033[0m"
    
    @staticmethod
    def green(txt):
        return "\033[32m"+txt+"\033[0m"
    
    @staticmethod
    def yellow(txt):
        return "\033[33m"+txt+"\033[0m"
    
    @staticmethod
    def dark_grey(txt):
        return "\033[90m"+txt+"\033[0m"
    
    @staticmethod
    def magenta(txt):
        return "\033[35m"+txt+"\033[0m"
    

# Return function to run arbitrary command
def exec_shell(*args):
    """generates a python function that wraps around shell cmd"""
    def _run_cmds(ag=args):
        for arg in ag:
            # Run the pre-command (likely a build command)
            pre_result = subprocess.run(arg, shell=True, capture_output=True)
            if pre_result.returncode != 0:
                print(f"ERROR! Pre-command failed")
                sys.exit(10)
        return 0
    return _run_cmds