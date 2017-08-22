import sys, zeldarom, nesrom

rom = zeldarom.ZeldaRom()
rom.load_from_file(sys.argv[1])
rom.load_from_rom()

print(rom)
