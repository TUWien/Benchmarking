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
python lib\database\cdb.py --help
```

Example:
```
python lib\database\cdb.py --outfile C:/temp/db.txt --copyto C:/temp/reduced C:/temp 5
```
This command locates all images in ``C:/temp``, reduces the set to 5 images and
copies these images to ``C:/temp/reduced``. Then, ``C:/temp/db.txt`` is
created which contains the paths to the original images of the reduced set.

Call this function from python using:

```
import database
rf = database.cdb.create_database("C:/temp", 13)
print("\n".join(rf))
```
### Links
- CVL http://www.caa.tuwien.ac.at/cvl/
