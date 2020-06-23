# Release: 0.1.0
## Optichiver

Python script for splitting image files into separate directories according to specified disc size and hashes files.

### Dependencies:

- Python 3.6+

- Unix/Linux 

### Python3 Dependencies

```
sudo pip3 install exifread toml
```

### Usage:

```
chmod +x optichiver.py
./optichiver --input /inputpath --output /outputpath --size DVD --hash --checksum sha256 --format NONE 
```

Run using default settings as listed above

```
./optichiver --input /inputpath --output /outputpath
```

### Optichiver cli:
```
Optichiver: Script for backing up to optical discs

usage: optichiver.py [-h] [--input INPUT] [--output OUTPUT] [--skipcheck]
                     [--size SIZE] [--custom CUSTOM] [--label LABEL]
                     [--format FORMAT] [--hash] [--checksum CHECKSUM]
                     [--hashfile HASHFILE] [--verbose]

Optichiver cli

optional arguments:
  -h, --help           show this help message and exit
  --input INPUT        Input path
  --output OUTPUT      Output path
  --skipcheck          Skip system file check
  --size SIZE          Disc size:
                       	DVD	4.7GB(default)
                       	DVD-DL	9.4GB
                       	BL	25GB
                       	BL-DL	50GB
                       	BL-QL	100GB
  --custom CUSTOM      Custom size:
                       	(int)B
  --label LABEL        Set disc label prefix
  --format FORMAT      Output file format
                       	YMD		/label/year/month/dir/image.jpg
                       	YM		/label/year/month/image.jpg
                       	Y		/label/year/image.jpg
                       	NONE(default)	/label/image.jpg
  --hash               Enable hashing
  --checksum CHECKSUM  Checksum algorithm:
                       	blake2
                       	md5
                       	sha1
                       	sha224
                       	sha256(default)
                       	sha384
                       	sha512
  --hashfile HASHFILE  Input hash file
  --verbose            Increase output verbosity
```
