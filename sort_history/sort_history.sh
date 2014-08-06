history | awk '{a[$2]++;} END {for (i in a) printf "%5s %s\n", a[i],i;}' | awk '{a[$0]=$1} END {l=asorti(a,b); for (i=l; i > 0; --i) print b[i];}'
