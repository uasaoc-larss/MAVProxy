setlocal
SET PATH=%PATH%;..\mavlink;..\mavlink\pymavlink\examples

mavproxy.py --master=COM18 --baudrate=115200 --mav09
 
pause