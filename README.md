# SubDomainTrack
简单的子域名查找工具.
支持爆破和https证书查找.

## Usage

```
Usage: Track.py [option] domain.com

Options:
  -h, --help            show this help message and exit
  -t THREADS, --threads=THREADS
                        Num of Scan Threads, Default 150
  -f FILE, --file=FILE  Scan list of Domain, Please put file in dict floder
                        below, Default wordlist.txt
  -c, --crt             Through the Https certificate
  -o OUTFILE, --outfile=OUTFILE
                        Output a file
```

## 参考

[subDomianBrute](https://github.com/lijiejie/subDomainsBrute)
