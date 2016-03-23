
ASM_PATH=../../util/rgbds

all:
	$(ASM_PATH)/rgbasm -o simple.obj simple.asm
	$(ASM_PATH)/rgblink -m simple.map -n simple.sym -o simple.gb simple.obj
	$(ASM_PATH)/rgbfix -p0 -v simple.gb
