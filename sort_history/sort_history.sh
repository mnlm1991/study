history | awk '{a[$2]++;} END {for (i in a) printf "%5s %s\n", a[i],i;}' | sort -rn
