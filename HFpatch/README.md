`Those patches are needed to correct the bugs in HistFitter official package or make is suitable for our case`

## PrintFitResult.py:

* fixed the bug that the `-o` (output) is not working

## Significance.cxx:

* set minimum p-value = 0.0001

## SysTable.py:

* add more print out to make bugging easier
* add a block to prepare txt file for systematic plot

## SysTableTex.py：

* set different font and format to make it suitable for our case

## Utils.cxx:

* add a function for `GetPropagatedErrorNoStat`
* aiming to get correct errors before/after fit

## YieldsTable.py:

* change into correct functions to get correct errors before/after fit
* setup output or few options to make it suitable for our case

## YieldsTableTex.py:

* change font and format to suitable for our case
* add a function `getStatErr` to get correct statistical uncertainty to be read directly by the workspace created by HistFitter

## contourPlotter.py:

* add more output to help with debugging

## harvestToContours.py:

* add more output to help with debugging

## multiplexContours.py:

* to add expected 1-d band in the output files which will make the plots correct

## pull_maker.py:

* fixed the bug in drawing pull plots which will cause the displaced bins in the plot

## sample.py:

* fixed the bug on the treatment of the systematics going to one direction while symmeterizing
