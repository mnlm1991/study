#/bin/sh

base_dir=$(cd "$(dirname "$0")"; pwd)
fetch=$base_dir/"fetch_weather.py"
data="/tmp/weather.data"
notify="/tmp/weather_updata_notify"
is_parse="/tmp/weather_is_parse"

echo $base_dir
echo $fetch
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
	sleep 5
done

exit 0
