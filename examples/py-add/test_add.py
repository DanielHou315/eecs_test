from eecs_test import TestConfig, TestConfigMgr, EECSTest, MISOTests

class PyAdd(TestConfig):
    name = "add"
    test_dirs = ["./add-tests", "./add-debug-tests"]        # Directories containing in/out/correct subdirectories
    input_ext = ["txt"]              # Input file extensions to process
    output_ext = "out"             # Output file extension
    test_type = MISOTests
    # Command 
    pre_cmd = None
    cmd_template = "python3 add.py {INPUT} {OUTPUT}"
    post_cmd = None
    # Output Configuration
    print_diff_mode = "none"
    print_exec_mode = "file"

class PyAddDebug(TestConfig):
    name = "add-debug"
    test_dirs = ["./add-debug-tests"]        # Directories containing in/out/correct subdirectories
    input_ext = ["txt"]              # Input file extensions to process
    output_ext = "out"             # Output file extension
    test_type = MISOTests
    # Command 
    pre_cmd = None
    cmd_template = "python3 add.py {INPUT} {OUTPUT}"
    post_cmd = None
    # Output Configuration
    print_diff_mode = "none"
    print_exec_mode = "file"
    # Debug
    debug = True

class PyAddWrong(TestConfig):
    name = "add-err"
    test_dirs = ["./add-err-demo"]        # Directories containing in/out/correct subdirectories
    input_ext = ["txt"]              # Input file extensions to process
    output_ext = "out"             # Output file extension
    test_type = MISOTests
    # Command 
    pre_cmd = None
    cmd_template = "python3 add.py {INPUT} {OUTPUT}"
    post_cmd = None
    # Output Configuration
    print_diff_mode = "none"
    print_exec_mode = "none"

# Register configurations
TestConfigMgr.register(PyAdd)
TestConfigMgr.register(PyAddDebug)
TestConfigMgr.register(PyAddWrong)

# Run tests
if __name__ == "__main__":
    runner = EECSTest()
    runner()
    