#/bin/sh

fetch="./fetch_weather.py"
data="/tmp/weather.data"
notify="/tmp/weather_updata_notify"
is_parse="/tmp/weather_is_parse"

if [ ! -f $fetch ]; then
	exit 0
fi
if [ -f $notify ]; then
	rm -f $notify
fi
while [ 1 -eq 1 ]
do
	if [ -f $is_parse ]; then
		continue
	fi
	$fetch > $data
	touch $notify
	sleep 60
done

exit 0
