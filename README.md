# CVL Benchmarking Module 🍸

All python scripts needed for benchmarking Document Analysis algorithms
are contained in this repository.

## Building

### Requirements

[Python 3.4.4] (https://www.python.org/downloads/) or newer

### Build Steps

- Install required modules:

```bat
pip install pyyaml
```

- Open this directory (containing the ``setup.py``) in a command line and type

```bat
python setup.py install
```

## Database

Database contains scripts to crawl your hard disk and reduce the number of
specific file types. See:

```bat
lib\database\cdb.py --help
```

Example:

```bat
lib\database\cdb.py --outfile C:/temp/db.txt --copyto C:/temp/reduced C:/temp 5
```

This command locates all images in ``C:/temp``, reduces the set to 5 images and
copies these images to ``C:/temp/reduced``. Then, ``C:/temp/db.txt`` is
created which contains the paths to the original images of the reduced set.

Call this function from python using:

```python
import database
rf = database.cdb.index_and_reduce_database("C:/temp", 13)
print("\n".join(rf))
```

Another script `split.py` splits a folder into train, evaluation and test set with user set proportions:

```bat
lib\database\split.py C:/temp C:/temp/split --train 0.2 --eval 0.1
```

This command copies 20% of the images contained in `C:/temp` into `C:/temp/split/train`, 10% into `C:/temp/split/eval` and all other images into `C:/temp/split/test`. You can set --eval 0 if you don't need an evaluation set.

## Writer

Writer contains scripts to analyze XML files in the mets format. It extracts the
and his corresponding pages out of the XML files and copies it to a new directory

First you have to create a database with all the xml files using the database crawler:

```bat
lib\database\cdb.py --outfile c:\tmp\db.txt --ext xml c:\tmp\myDatabase 1000000
```

From these xml files the writers are than extracted using

```bat
lib\writer\analyze.py --infile c:\tmp\db.txt --outfile c:\tmp\writers.txt --dumpfile c:\tmp\writer.pkl

```

and then the dataset is created using

``` bat
lib\writer\create.py --infile c:\tmp\writer.pkl --outdir c:\tmp\writer-database \\
--minnum 0 --maxnum -1 --mapfile c:\tmp\writer-database\authorName-to-id-mapping.txt
```

`minnum` is the minimal number of pages, and `maxnum` is the maximal number of pages
(if -1 than all pages are taken from this writer)

## Links

- [CVL](http://www.caa.tuwien.ac.at/cvl/)
