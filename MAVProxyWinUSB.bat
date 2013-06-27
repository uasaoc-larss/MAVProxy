setlocal
SET PATH=%PATH%;..\mavlink;..\mavlink\pymavlink\examples

mavproxy.py --master=COM13 --baudrate=57600 --target-system=17

pause