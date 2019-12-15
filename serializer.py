from os.path import join
from judge import Test
import pickle

tests_dir = "data/tests"

tests = [
    Test(1, join(tests_dir, "t01.txt"), 1, 0),
    Test(2, join(tests_dir, "t02.txt"), 1, 0),
    Test(3, join(tests_dir, "t03.txt"), 2, 0),
    Test(4, join(tests_dir, "t04.txt"), 2, 0),
    Test(5, join(tests_dir, "t05.txt"), 1, 0),
    Test(6, join(tests_dir, "t06.txt"), 1, 0),
    Test(7, join(tests_dir, "t07.txt"), 2, 0),
    Test(8, join(tests_dir, "t08.txt"), 2, 0),
    Test(9, join(tests_dir, "t09.txt"), 1, 0),
    Test(10, join(tests_dir, "t10.txt"), 1, 0),

    Test(11, join(tests_dir, "t11.out"), 2, 1),
    Test(12, join(tests_dir, "t12.out"), 3, 1),
    Test(13, join(tests_dir, "t13.out"), 2, 1),
    Test(14, join(tests_dir, "t14.out"), 1, 1),
    Test(15, join(tests_dir, "t15.out"), 2, 1),
]

with open(join(tests_dir, "dat.pkl"), 'wb') as the_file:
    pickle.dump(tests, the_file, -1)