set encoding iso_8859_1
#set terminal postscript eps enhanced
set palette defined ( 0 0 0 0, 1 1 1 1 )
set xrange [1:80000]
set yrange [0:10000]
set xlabel "Frequency"
set ylabel "Number of patterns"
set key right top
set style data histogram
set style fill solid border
set style line 1 lc rgb "black"
set style line 2 lc rgb "blue"
set style line 3 lc rgb "green"
set style line 4 lc rgb "yellow"
set title "D100K5S2T6I"
plot \
  'D100K5S2T6I_10000.num' using 1:3 :($1-0.00):($1+2*600.00) title "without constraint" with boxes fill pattern fill solid 0.8 ls 1, \
  '7_D100K5S2T6I_10000.num' using 1:3 :($1+2*600.00):($1+4*600.00) title "with M=7" with boxes fill solid 0.5 ls 1, \
  '4_D100K5S2T6I_10000.num' using 1:3 :($1+4*600.00):($1+6*600.00) title "with M=4" with boxes fill solid 0.2 ls 1
set term postscript portrait
set output "D100K5S2T6I_freq.eps"
#set size 0.9, 0.525
#set size 1, 0.4
replot
