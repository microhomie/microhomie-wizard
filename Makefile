export PATH := $(PWD)/esp-open-sdk/xtensa-lx106-elf/bin:$(PWD)/micropython/tools:$(PWD)/micropython/ports/unix:$(HOME)/go/bin:$(PATH)

VERSION := 0.1.0-alpha
MICROPYVERSION := 1.9.4
PORT := /dev/ttyUSB0


all: clean bin2res templates copy firmware

requirements:
	micropython -m upip install -p micropython/ports/esp8266/modules -r requirements.txt
	cp lib/* micropython/ports/esp8266/modules

bin2res: style
	cd wizard; mpy_bin2res.py static/style.min.css > R.py

copy: clear-templates
	cp -rf wizard micropython/ports/esp8266/modules
	cp inisetup.py micropython/ports/esp8266/modules

firmware:
	cd micropython/ports/esp8266; make

copy-firmware:
	cp micropython/ports/esp8266/build/firmware-combined.bin ./microhomie-wizard-v$(VERSION).bin

release: requirements clean bin2res templates copy firmware copy-firmware

clean:
	cd micropython/ports/esp8266; make clean
	-rm -rf micropython/ports/esp8266/modules/wizard

deploy: erase flash

erase:
	esptool.py --port $(PORT) --baud 460800 erase_flash

flash:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0 micropython/ports/esp8266/build/firmware-combined.bin

style:
	cd wizard/static; minify -o style.min.css style.css

templates: clear-templates
	MICROPYPATH=lib micropython -c 'import wizard.app; wizard.app.preload_templates()'

clear-templates:
	-rm wizard/templates/*.py

go-minify:
	go get github.com/tdewolff/minify/cmd/minify

espopensdk:
	git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
	cd esp-open-sdk; make

micropython:
	git clone --recursive https://github.com/micropython/micropython.git
	cd micropython; git checkout -b $(MICROPYVERSION)
	cd micropython; make -C mpy-cross
	cd micropython/ports/unix; make axtls; make
	cd micropython; git apply ../micropython.patch

bootstrap: espopensdk micropython go-minify requirements
