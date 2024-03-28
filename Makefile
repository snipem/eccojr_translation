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

patch: deps
	bin/cmdMultiPatch --create Ecco\ Jr.\ \(USA,\ Australia\).Base.md Ecco\ Jr.\ \(USA,\ Australia\).Hack.md eccojr_german.ips

watch:
	ls strings_de.txt| entr make

deps: bin/cmdMultiPatch

bin/cmdMultiPatch:
	mkdir bin || true
	wget http://projects.sappharad.com/multipatch/multipatch20_cmd.zip -O bin/multipatch.zip
	unzip bin/multipatch.zip -d bin
	rm bin/multipatch.zip

