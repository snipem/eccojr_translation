build: read enrich write

diff: read enrich write
	# This is the complete round trip and should work with a plain base rom
	# and a strings_de.txt file that matches an extracted strings_en.txt file
	hexdump -C Ecco\ Jr.\ \(USA,\ Australia\).Base.md > base.txt
	hexdump -C Ecco\ Jr.\ \(USA,\ Australia\).Hack.md > hack.txt
	diff base.txt hack.txt

read:
	python3 read.py

enrich:
	python3 enrich.py

write:
	python3 write.py

watch:
	ls strings_de.txt| entr make
