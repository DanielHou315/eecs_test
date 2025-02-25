import os
import argparse

from .utils import SF
from .test_config import TestConfigMgr
from .test_case import TestCase

class EECSTest:
    def __init__(self):
        self.correct_counter = 0
        self.incorrect_counter = 0
        self.missing_counter = 0

    def __update_counters(self, c, i, m):
        self.correct_counter += c
        self.incorrect_counter += i
        self.missing_counter += m

    @classmethod
    def __run_cmd(cls, pre_post_fn):
        """Run the pre-command and check success"""
        # Run pre-command (likely a build command)
        if pre_post_fn is None or pre_post_fn == "":
            return
        result = pre_post_fn()
        if result != 0:
            print(f"ERROR! Pre/Post command failed")
            exit(1)

    @classmethod
    def __force_ack(cls, warning):
        """Print an acknowledgement and force user to take it"""
        print(SF.yellow(warning))
        ack = input(SF.yellow("Proceed?")+" [yes|No] >>> ")
        if ack not in ["y","Y", "yes", "Yes", "YES"]:
            print("Not Acknowledged, exiting...")
            exit(0)
        return

    def __dump_summary(self):
        # # For each, print status
        # for test_case in self.test_cases:
        #     test_case.dump_status()
        print("\nTest Summary:")
        c,i,m = self.correct_counter, self.incorrect_counter, self.missing_counter
        tot = c+i+m
        if tot == 0:
            print("No Test Detected!")
            return
        # print correct
        c_rate = (c/tot)*100
        if (c_rate >= 100.0):
            print(f"- Correct: {SF.green(f"{c}/{tot} ({c_rate:.1f}%)")}")
        else:
            print(f"- Correct: {c}/{tot} ({(c/tot)*100:.1f}%)")
        # Print errors
        i_rate = (i/tot)*100
        if (i_rate > 0.0):
            print(f"- Inorrect: {SF.red(f"{i}/{tot} ({i_rate:.1f}%)")}")
        else:
            print(f"- Inorrect: {i}/{tot} ({i_rate:.1f}%)")
        # Print Missing
        m_rate = m/tot*100
        if (m_rate > 0.0):
            print(f"- Missing: {SF.yellow(f"{m}/{tot} ({m_rate:.1f}%)")}")
        else:
            print(f"- Missing: {m}/{tot} ({m_rate:.1f}%)")

    def __call__(self):
        # Parse command-line argument
        parser = argparse.ArgumentParser(description="Run tests for a given test type.")
        parser.add_argument("test", help="Test to run")
        parser.add_argument("--correct", action="store_true",
                            help="Set outputs as correct files")
        # Parse arguments
        args = parser.parse_args()

        # Get config
        cfg = TestConfigMgr.get(args.test)
        # Get correct setting
        if args.correct == True:
            self.__force_ack("Warning: overwriting existing Reference Solutions!")
            cfg.__copy_to_correct__ = True

        # Start testing
        print(SF.magenta(f"\n=== Starting {cfg.name} test ===\n"))
        TestCase.set_cfg(cfg)
        self.__run_cmd(cfg.pre_cmd)

        # For each test dir, run tests
        for test_dir in cfg.test_dirs:
            test_name = os.path.basename(test_dir)
            print(f"\n### Running tests in ``{test_name}`` ###\n")

            # Run tests
            runner = cfg.test_type(test_dir, cfg)
            runner.run_tests()
            
            # Update counters
            c, i, m = runner.get_stats()
            self.__update_counters(c,i,m)

            # Print the per-test result
            runner.dump_test_result()

        self.__dump_summary()
        self.__run_cmd(cfg.post_cmd)

        print("\n=== All tests processed ===")