REM dir to current directory
cd %~dp0

REM bohisto
lib\database\cdb.py --outfile F:\competition\cmp-250 --copyto F:\competition\cmp-250 --log --flat --batch F:\ftp-ibk\ 250

REM train/test for baseline competition
lib\database\cdb.py --outfile "D:\read\baseline-competition\bc-train\Track A" --copyto "D:\read\baseline-competition\bc-train\Track A"  --batch "D:\read\baseline-competition\bc-test\Track A" --log --deletesource --ext ".jp(e)?g$|.tif(f)?$|.png$|.bmp$|.xml$" 30

REM test
REM Track A images
lib\database\cdb.py --outfile "D:\read\baseline-competition\baseline-test-train\bc-test-img" --copyto "D:\read\baseline-competition\baseline-test-train\train\Track A"  --batch "D:\read\baseline-competition\baseline-test-train\bc-test-img\Track A" --log --deletesource --ext ".jp(e)?g$|.tif(f)?$|.png$|.bmp$|.xml$" 30

REM Track A XMLs
lib\database\cdb.py --outfile "D:\read\baseline-competition\baseline-test-train\bc-test-xml" --copyto "D:\read\baseline-competition\baseline-test-train\train\Track A"  --batch "D:\read\baseline-competition\baseline-test-train\bc-test-xml\Track A" --log --deletesource --ext ".jp(e)?g$|.tif(f)?$|.png$|.bmp$|.xml$" 30

REM Track B images
lib\database\cdb.py --outfile "D:\read\baseline-competition\baseline-test-train\bc-test-img" --copyto "D:\read\baseline-competition\baseline-test-train\train\Track B"  --batch "D:\read\baseline-competition\baseline-test-train\bc-test-img\Track B" --log --deletesource --ext ".jp(e)?g$|.tif(f)?$|.png$|.bmp$|.xml$" 30

REM Track B XMLs
lib\database\cdb.py --outfile "D:\read\baseline-competition\baseline-test-train\bc-test-xml" --copyto "D:\read\baseline-competition\baseline-test-train\train\Track B"  --batch "D:\read\baseline-competition\baseline-test-train\bc-test-xml\Track B" --log --deletesource --ext ".jp(e)?g$|.tif(f)?$|.png$|.bmp$|.xml$" 30
