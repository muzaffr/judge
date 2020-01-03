from subprocess import run, check_output, TimeoutExpired, CompletedProcess
from sys import argv
from os.path import split, splitext, join, abspath, isfile
from getpass import getpass
from hashlib import sha256
from time import sleep, strftime, localtime
from shlex import split as lexsplit
import pickle

LANGUAGES = {
    ".c": ("C99", "gcc {} -o {} --std=c99 -lm"),
    ".cpp": ("C++17", "g++ {} -o {} --std=c++17"),
}


class Test:
    verdict_map = {
        0: ("PENDING_JUDGEMENT", 1, 46, 30),
        1: ("ACCEPTED", 1, 42, 30),
        2: ("WRONG_ANSWER", 1, 41, 30),
        3: ("TIME_LIMIT_EXCEEDED", 1, 45, 30),
        4: ("RUNTIME_ERROR", 1, 43, 30),
    }

    def __init__(self, uid, inp, max_score, is_gen):
        self.uid = uid
        self.inp = inp  # stores input filename initially, stores first few characters of input after judging
        self.is_gen = is_gen  # true if the file pointed by inp is a generator, false if it is plain text
        self.max_score = max_score
        self.score = 0
        self.verdict = 0
        path, base = split(self.inp)
        stem, ext = splitext(base)
        self.out = join(path, "out_" + stem + ".txt")
        self.log = ""


def ansi_color(text, *attributes):
    """
    Formats/highlights text to be printed on the console as per the ANSI
    coloring scheme.
    """
    return "\033[{}m{}\033[0m".format(";".join(map(str, attributes)), text)


def verify_pass(pw, action):

    with open(join(base_path, "data/hashes", action), 'r') as content_file:
        content = content_file.read()
        if sha256(pw.encode("utf-8")).hexdigest() != content:
            print(ansi_color("Invalid password.", 1, 31))
            return False
    return True


def print_result(test):
    """
    Prints the formatted result of a test.
    """
    print("| {:>2} | {:<33} | {:>14} | {}".format(
            str(test.uid),
            ansi_color(*Test.verdict_map[test.verdict]),
            ansi_color("{}/{}".format(test.score, test.max_score), 31 + (test.verdict == 1)),
            test.log
        ),
        end="\r\n"[bool(test.verdict)]
    )


def check(test):
    """
    Runs checker on test result.
    """
    if not test.verdict:
        if test.is_gen:
            checker_input = check_output([join(base_path, test.inp)])
        else:
            with open(join(base_path, test.inp), 'rb') as content_file:
                checker_input = content_file.read()
        with open(join(base_path, test.out), 'rb') as content_file:
            checker_input += content_file.read()
        p = run(join(base_path, "data/checker"), input=checker_input, capture_output=True)
        test.verdict = p.returncode
        if test.verdict == 1:
            test.score = test.max_score
        test.log = p.stdout.decode()
    print_result(test)


def reveal(param):
    """
    Reveal most information about a test case.
    """
    try:
        test_id = int(param)
        if test_id < 1:
            raise IndexError
        with open("judge_data.pkl", 'rb') as content_file:
            data = pickle.load(content_file)
            tests = data["results"]
        test = sorted(tests, key=lambda x: x.uid)[test_id-1]
    except ValueError:
        print("Usage: ./judge reveal #testcase")
        return
    except IndexError:
        print("Invalid case ID. (1-{})".format(len(tests)))
        return
    except FileNotFoundError:
        print("Judge at least once before using reveal.")
        return
    if not verify_pass(getpass(), "reveal"):
        return

    run("clear")
    print(ansi_color("Test #{}".format(test.uid), 1, 4), end="\n\n")
    print(ansi_color("Source file name:", 1))
    print(data["name"], end="\n\n")
    print(ansi_color("Judged at:", 1))
    print(data["time"], end="\n\n")
    print(ansi_color("Input:", 1))
    print(test.inp, end="\n\n")
    print(ansi_color("Your output:", 1))
    print(test.out, end="\n\n")
    print(ansi_color("Verdict:", 1))
    print(Test.verdict_map[test.verdict][0], end="\n\n")
    if test.log:
        print(ansi_color("Checker log:", 1))
        print(test.log, end="\n\n")


def clean():
    """
    Cleans generated data.
    """
    print("Clean will delete the judge and all judge generated data.")
    res = input("Proceed? [Y/N] ").upper()
    if res != 'Y':
        return
    if not isfile("judge_data.pkl"):
        print("Nothing to clean!")
        return
    print("Deleting judge generated data...")
    run(["rm", "judge_data.pkl"])
    print("Deleting judge...")
    run(["rm", "judge"])
    print("Clean!")
    return


def main():

    global base_path
    try:
        base_path = sys._MEIPASS
    except NameError:
        base_path = abspath(".")

    if len(argv) == 3 and argv[1] == "reveal":
        reveal(argv[2])
        return
    elif len(argv) == 2 and argv[1] == "clean":
        clean()
        return
    elif len(argv) != 2:
        print("Usage: ./judge filename")
        return

    if not verify_pass(getpass(), "judge"):
        return

    with open(join(base_path, "data", "metadata.pkl"), 'rb') as data_file:
        metadata = pickle.load(data_file)
    time_limit = metadata["time_limit"]
    allowed_languages = metadata["allowed_languages"]
    tests = metadata["tests"]

    filename = argv[1]
    run("clear")
    print("Judging {}...".format(ansi_color(filename, 36)))
    stem, ext = splitext(filename)
    if ext not in allowed_languages:
        print("Invalid file extension.\nAllowed files are:")
        for allowed_ext in allowed_languages:
            print(allowed_ext, "({})".format(LANGUAGES[allowed_ext][0]))
        return
    print()
    command = LANGUAGES[ext][1].format(filename, stem)
    p = run(lexsplit(command))

    if p.returncode:
        print(ansi_color("\nVerdict:", 1, 37), ansi_color("COMPILATION_ERROR", 1, 41, 30))
        return

    print("\n| {:>10} | {:<27} | {:>5} | {}".format(
            ansi_color("#", 1),
            ansi_color("Verdict", 1),
            ansi_color("Score", 1),
            ansi_color("Checker log", 1),
        )
    )
    print('-'*80)
    results = []
    passed_cases = total = max_total = 0
    total_cases = len(tests)

    for test in tests:
        print_result(test)  # pending judgement
        sleep(0.3166227766)
        if test.is_gen:
            input_content = check_output([join(base_path, test.inp)])
        else:
            with open(join(base_path, test.inp), 'rb') as content_file:
                input_content = content_file.read()
        try:
            p = run(join(".", stem), input=input_content, capture_output=True, timeout=time_limit/1000)
            if p.returncode:
                test.log = "exit code is {}".format(p.returncode)
                test.verdict = 4
        except TimeoutExpired:
            p = CompletedProcess("", 0)
            p.stdout = b""
            test.verdict = 3
            test.log = "running time exceeded {}ms".format(time_limit)

        with open(join(base_path, test.out), 'wb') as the_file:
            the_file.write(p.stdout)

        check(test)  # check if output was correct
        passed_cases += (test.verdict == 1)
        total += test.score
        max_total += test.max_score

        trail = ("", "...")
        test.inp = input_content.decode()
        test.inp = test.inp[:255] + trail[len(test.inp) > 255]
        test.out = p.stdout.decode()
        test.out = test.out[:255] + trail[len(test.out) > 255]
        if not test.out:
            test.out = "<no output>"

        results.append(test)

    print("\nCases passed: {}/{}".format(passed_cases, total_cases))
    print(ansi_color("Total score:  {}/{}\n".format(total, max_total), 1))
    if total == max_total:
        print("Well done!")
    if total == 0:
        print("Better luck next time.")

    # store the tests with their verdicts into a file
    with open("judge_data.pkl", 'wb') as the_file:
        pickle.dump(
            {
                "results": results,
                "name": filename,
                "time": strftime('%I:%M:%S %p, %d-%b-%Y', localtime()),
            },
            the_file, -1,
        )

    run(["rm", stem])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nQuitting judge...\n")
