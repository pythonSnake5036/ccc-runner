from os import listdir
from os.path import join
import re
import asyncio
import sys
import time

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    NC = '\033[0m'

test_regex = re.compile(r"^(.*)\.in$")

def find_test_cases(test_data_path):
    matches = [test_regex.match(f) for f in listdir(test_data_path)]
    test_cases = [(match[1], join(test_data_path, match[0]), join(test_data_path, match[1]+".out")) for match in matches if match is not None]
    return test_cases

async def run_test_case(program_cmd, test_case):
    with open(test_case[2]) as f:
        expected_out = f.read()

    with open(test_case[1]) as f:
        proc = await asyncio.create_subprocess_shell(program_cmd, shell=True, stdin=f, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)

        stdout, _ = await proc.communicate()

    output = stdout.decode()

    return (expected_out == output, output, expected_out)

async def run_problems(test_data_path, program_cmd):
    test_cases = find_test_cases(test_data_path)

    for test_case in test_cases:
        start_time = time.perf_counter()
        success, out, expected = await run_test_case(program_cmd, test_case)
        end_time = time.perf_counter()
        elapsed = end_time - start_time

        yield test_case, success, elapsed, out, expected

async def main():
    test_data = sys.argv[1]
    program_cmd = " ".join(sys.argv[2:])
    async for test_case, success, elapsed, out, expected in run_problems(test_data, program_cmd):
        if success:
            print(f"{Colors.GREEN}{test_case[0]}: Pass ({elapsed:.2f}s){Colors.NC}")
        else:
            print(f"{Colors.RED}{test_case[0]}: Fail ({elapsed:.2f}s)\nOutput:\n{out}\nExpected Output:\n{expected}\n{Colors.NC}")

if __name__ == "__main__":
    asyncio.run(main())

