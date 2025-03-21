import os
import subprocess
import shutil

from .utils import SF, log_debug
from .test_case import TestCase

class TestRunner:
    DEBUG_ID = "Test Runner"
    def __init__(self, test_dir, cfg):
        self.test_dir = os.path.abspath(test_dir)
        self.cfg = cfg
        # Resset
        self.__reset()
        self.__preprocess_testdir()

    def is_empty_dir(self):
        return (not os.path.isdir(self.input_dir))

    def __reset(self):
        self.correct_counter = 0
        self.incorrect_counter = 0
        self.missing_counter = 0
        self.test_cases = []

    def __preprocess_testdir(self):
        """Preprocess the directories, make them if needed"""
        # Build directory paths
        self.input_dir = os.path.join(self.test_dir, "in")
        self.output_dir = os.path.join(self.test_dir, "out")
        self.correct_dir = os.path.join(self.test_dir, "correct")

        # Create output directory if needed
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run_tests(self):
        # Finally, run all the commands
        for test_id, test_case in enumerate(self.test_cases):
            cmd_result = subprocess.run(test_case.cmd, shell=True, capture_output=True, text=True)
            
            # If later used, overwrite
            diff_output = None
            cmd_output = cmd_result.stdout

            if self.cfg.__copy_to_correct__ == True:
                status_msg = self.__copy_to_correct(test_case.output_path, test_case.correct_path)
                diff_output = ""
            else:
                status_msg, diff_output = self.check_result(test_case.output_path, test_case.correct_path)
            status = status_msg.format(i=(test_id+1), filename=test_case.test_name)
            test_case.store_status(status, cmd_output, diff_output)

    def check_result(self, output_path, correct_path):
        # Determine test status
        status = "No.{i} {filename}: "+SF.red("Execution Raised Error")
        diff_output = None

        # If output file is generated
        if os.path.exists(output_path):
            if os.path.exists(correct_path):
                status, diff_output = self.__compare_to_correct(output_path, correct_path)
            else:
                status = "No.{i} {filename}: "+SF.yellow(f"Missing Output Reference {correct_path}")
                self.missing_counter += 1
        return status, diff_output

    def __compare_to_correct(self, output_path, correct_path):
        diff_output = ""
        # Compare with reference file
        diff_result = subprocess.run(
            ["diff", output_path, correct_path],
            capture_output=True,
            text=True
        )
        if diff_result.returncode == 0:
            status = "No.{i} {filename}: "+SF.green("Output Correct")
            self.correct_counter += 1
        else:
            status = "No.{i} {filename}: "+SF.red("Output Incorrect")
            self.incorrect_counter += 1
            diff_output = diff_result.stdout
        return status, diff_output

    @classmethod
    def __copy_to_correct(cls, output_path, correct_path):
        """
        Copies the file at output_path to correct_path.
        
        If a file already exists at correct_path, it is overwritten and
        the function returns status "overwrite". If no file exists at
        correct_path, the file is added and the function returns status "add".
        """
        # Determine the status based on whether the correct file exists.
        if os.path.exists(correct_path):
            status = "No.{i} "+SF.red("Overwritten")+" {filename}"
        else:
            status = "No.{i} "+SF.green("Added")+" {filename}"

        # Ensure the destination directory exists.
        dest_dir = os.path.dirname(correct_path)
        os.makedirs(dest_dir, exist_ok=True)
        
        # Copy the file from output_path to correct_path.
        shutil.copy2(output_path, correct_path)
        return status

    def dump_test_result(self):
        # For each, print status
        for test_case in self.test_cases:
            test_case.dump_status()

    def get_stats(self):
        return (self.correct_counter, self.incorrect_counter, self.missing_counter)
  

class SISOTests(TestRunner):
    DEBUG_ID = "SISO Runner"
    def __init__(self, test_dir, cfg):
        super().__init__(test_dir, cfg)
        self.__generate_test_cases()

    def __generate_test_cases(self):
        files = [f for f in os.listdir(self.input_dir) 
                if (os.path.isfile(os.path.join(self.input_dir, f))
                    and os.path.splitext(f)[1][1:] in self.cfg.input_ext)
                ]
        # Assemble commands as normal
        for i, file in enumerate(files):
            # Process filename, skip if none
            (input_path, output_path, correct_path) = \
                self.__process_fname(file)
            if output_path is None:
                continue

            # Build a TestCase instance
            test_name = os.path.splitext(os.path.basename(input_path))[0]
            # print(test_name, "from", input_path)
            cmd = self.cfg.cmd_template.format(INPUT=input_path, OUTPUT=output_path)
            if self.cfg.debug:
                log_debug(self.DEBUG_ID, f"Built command\n- <<{cmd}>>\nfor {test_name}")
            test_case = TestCase(self.test_dir, test_name, cmd, output_path, correct_path)
            # Add command
            self.test_cases.append(test_case)

    def __process_fname(self, filename):
        """process given input file name"""
        input_path = os.path.join(self.input_dir, filename)
        base, _ = os.path.splitext(filename)

        # Prepare file paths
        output_filename = f"{base}.{self.cfg.output_ext}"
        output_path = os.path.join(self.output_dir, output_filename)
        correct_path = os.path.join(self.correct_dir, f"{output_filename}.correct")
        if self.cfg.debug:
            log_debug(self.DEBUG_ID, f"Test file {filename} corresponds to\n- OUT: {output_filename}\n- CORRECT: {correct_path}")
        return (input_path, output_path, correct_path)

class MISOTests(TestRunner):
    DEBUG_ID = "MISO Runner"
    def __init__(self, test_dir, cfg):
        super().__init__(test_dir, cfg)
        self.test_dir = test_dir
        self.__generate_test_cases()

    def __generate_test_cases(self):
        dirs = [
            os.path.join(self.input_dir, d) for d in os.listdir(self.input_dir) 
            if (os.path.isdir(os.path.join(self.input_dir, d)))
        ]
        files = []
        for dir in dirs:
            f_in_dir = [
                os.path.join(dir, f) for f in os.listdir(dir) 
                if (os.path.isfile(os.path.join(dir, f))
                and os.path.splitext(f)[1][1:] in self.cfg.input_ext)
            ]
            f_in_dir.sort()
            files.append(f_in_dir)
        # Assemble commands in subdir manner
        for i, file in enumerate(files):
            # Process filename, skip if none
            (input_path, output_path, correct_path) = \
                self.__process_fname(file)
            if output_path is None:
                continue

            # Build a TestCase instance
            test_name = os.path.splitext(os.path.basename(output_path))[0]
            cmd = self.cfg.cmd_template.format(INPUT=" ".join(input_path), OUTPUT=output_path)
            if self.cfg.debug:
                log_debug(self.DEBUG_ID, f"Built {test_name} command\n\t``{cmd}``")
            test_case = TestCase(self.test_dir, test_name, cmd, output_path, correct_path)
            # Add command
            self.test_cases.append(test_case)

    def __process_fname(self, files):
        """process given input file name"""
        assert isinstance(files, list)
        if len(files) == 0:
            return None, None, None
        input_path = files
        base = files[0].split('/')[-2]

        # Prepare file paths
        output_filename = f"{base}.{self.cfg.output_ext}"
        output_path = os.path.join(self.output_dir, output_filename)
        correct_path = os.path.join(self.correct_dir, f"{output_filename}.correct")
        if self.cfg.debug:
            log_debug(self.DEBUG_ID, f"Test folder ``{base}`` corresponds to\n\t- OUT: {output_filename}\n\t- CORRECT: {correct_path}")
        return (input_path, output_path, correct_path)
