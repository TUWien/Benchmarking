# CVL Benchmarking Module 🍸
All python scripts needed for benchmarking Document Analysis algorithms
are contained in this repository.

## Building

#### Requirements
Python 3.4.4 or newer (see https://www.python.org/downloads/)

#### Build Steps
- Install required modules:
```
pip install pyyaml
```

- Open this directory (containing the ``setup.py``) in a command line and type
```
python setup.py install
```

### Database
Database contains scripts to crawl your hard disk and reduce the number of
specific file types. See:
```
lib\database\cdb.py --help
```

Example:
```
lib\database\cdb.py --outfile C:/temp/db.txt --copyto C:/temp/reduced C:/temp 5
```
This command locates all images in ``C:/temp``, reduces the set to 5 images and
copies these images to ``C:/temp/reduced``. Then, ``C:/temp/db.txt`` is
created which contains the paths to the original images of the reduced set.

Call this function from python using:

```
import database
rf = database.cdb.index_and_reduce_database("C:/temp", 13)
print("\n".join(rf))
```

### Writer ###
Writer contains scripts to analyze XML files in the mets format. It extracts the
and his corresponding pages out of the XML files and copies it to a new directory

First you have to create a database with all the xml files using the database crawler:
```
lib\database\cdb.py --outfile c:\tmp\db.txt --ext xml c:\tmp\myDatabase 1000000
```
From these xml files the writers are than extracted using
```
lib\writer\analyze.py --infile c:\tmp\db.txt --outfile c:\tmp\writers.txt --dumpfile c:\tmp\writer.pkl
```
and then the dataset is created using
```
lib\writer\create.py --infile c:\tmp\writer.pkl --outdir c:\tmp\writer-database --minnum 0 --maxnum -1 --mapfile c:\tmp\writer-database\authorName-to-id-mapping.txt
```

### Links
- CVL http://www.caa.tuwien.ac.at/cvl/
