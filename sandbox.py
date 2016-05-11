from multiprocessing import Pool


def f(p):

    print("p: %s -" % p)


# test routine
def test():
    import database
    from database import indexer
    from database import utils

    fn = "C:/temp/db.txt"
    paths = database.utils.read(fn)

    print(paths)

    p = Pool(5)
    p.map(indexer.dir_to_info, paths)
    # indexer.dirs_to_info(paths)
    print('done')


if __name__ == '__main__':
    import os

    p = "C:/temp"
    t = os.walk('.')
    print(t)
    # test()
