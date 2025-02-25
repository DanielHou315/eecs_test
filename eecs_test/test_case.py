import os
import subprocess

from .utils import SF

class TestCase:
    cfg = None
    def __init__(self, root_dir, test_name, cmd, output_path, correct_path):
        self.root_dir = root_dir
        self.test_name = test_name
        self.cmd = cmd
        self.output_path = output_path
        self.correct_path = correct_path
        self.exec_log_file = os.path.join(root_dir, "logs", test_name+".exec.out")
        self.diff_log_file = os.path.join(root_dir, "logs", test_name+".diff.out")

    @classmethod
    def set_cfg(cls, cfg):
        cls.cfg = cfg
        correct_modes = ["print", "file", "none"]
        for mode in [cfg.print_exec_mode, cfg.print_diff_mode]:
            if mode not in correct_modes:
                print(SF.red(f"** ERROR: Mode {mode} is invalid!"))
                print(f"** Valid modes are {correct_modes}")
                exit(1)
        # Show warning messages
        if cfg.print_exec_mode == "file":
            print(SF.yellow("[Warning] Execution output -> file output"))
        elif cfg.print_exec_mode == "None":
            print(SF.yellow("[Warning] Execution output omitted"))
        # Show warning messages
        if cfg.print_diff_mode == "file":
            print(SF.yellow("[Warning] diff output -> file output"))
        elif cfg.print_diff_mode == "None":
            print(SF.yellow("[Warning] diff output omitted"))

    def run(self):
        cmd_result = subprocess.run(self.cmd, shell=True, capture_output=True, text=True)
        
        # If later used, overwrite
        diff_output = None
        cmd_output = cmd_result.stdout

        return cmd_result, diff_output, cmd_output

    def store_status(self, status, stdout, diffout):
        self.status = status
        self.stdout = stdout
        self.diffout = diffout
    
    @staticmethod
    def __write_to_file(filename, content):
        base_dir = os.path.dirname(filename)
        os.makedirs(base_dir, exist_ok=True)
        with open(filename, "w") as f:
            f.write(content)
            f.close()

    def __dump_output(self, content, opcode, filename, dump_mode):
        if content is None or content == "":
            return
        if dump_mode == "print":
            content = f"{opcode} produced: \n```\n"+SF.dark_grey(content)+"\n```"
            print(content)
        elif dump_mode == "file":
            content = f"{opcode} produced: \n```\n"+content+"\n```"
            self.__write_to_file(filename, content)

    def dump_status(self):
        print(self.status)
        self.__dump_output(self.stdout, 
                        "Execution",
                        self.exec_log_file, 
                        self.cfg.print_exec_mode
                    )
        self.__dump_output(self.diffout, 
                        "Diff",
                        self.diff_log_file, 
                        self.cfg.print_diff_mode
                    )
        print("-----")