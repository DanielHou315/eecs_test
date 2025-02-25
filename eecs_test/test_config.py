from .test_runner import SISOTests, MISOTests

from .utils import exec_shell

class TestConfigNotExistError(Exception):
    def __init__(self):
        pass

class TestConfigExistError(Exception):
    def __init__(self):
        pass

class TestConfig:
    name = "BaseTestConfig"
    # Directory Configuration
    test_dirs = ["./tests"]        # Directories containing in/out/correct subdirectories
    input_ext = ["as",]              # Input file extensions to process
    output_ext = "mc"             # Output file extension
    # Type of tests
    test_type = SISOTests
    # Computing Configuration
    pre_cmd = None
    cmd_template = "./assembler {INPUT} {OUTPUT}"
    post_cmd = exec_shell("make clean")
    # Output Configuration
    print_diff_mode = "print"        # or "file" or "none"
    print_exec_mode = "print"      # or "file" or "none"

    # Hidden Properties
    __copy_to_correct__ = False

class TestConfigMgr:
    cfg_dict = {}
    default_test = None

    @classmethod
    def register(cls, cfg:TestConfig):
        name = cfg.name
        if name in cls.cfg_dict.keys():
            raise TestConfigExistError()
        cls.cfg_dict[name] = cfg

    @classmethod
    def exists(cls, key):
        return (key in cls.cfg_dict.keys())

    @classmethod
    def get(cls, key):
        if key not in cls.cfg_dict.keys():
            raise TestConfigNotExistError()
        return cls.cfg_dict[key]

    @classmethod
    def set_default(cls, key):
        if not cls.exists(key):
            raise TestConfigNotExistError()
        cls.default_test = key