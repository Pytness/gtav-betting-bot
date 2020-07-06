#!/usr/bin/env bash

cd training-data
count=`ls *.png | wc -l`



for i in $(seq 0 $(expr $count - 1)); do
	tesseract -l eng eng.pricedown.exp$i.png eng.pricedown.exp$i.box nobatch box.train
	# break
done

echo "pricedown 0 0 0 0 0" > font_properties
unicharset_extractor eng.pricedown.exp*.box
mftraining -F font_properties -U unicharset -O eng.unicharset eng.pricedown.exp*.tr
cntraining eng.pricedown.exp*.tr

mv inttemp pricedown.inttemp
mv normproto pricedown.normproto
mv pffmtable pricedown.pffmtable
mv shapetable pricedown.shapetable

combine_tessdata pricedown.
