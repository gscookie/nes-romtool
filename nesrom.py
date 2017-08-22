import ctypes
c_uint8 = ctypes.c_uint8
c_uint32 = ctypes.c_uint32

STRUCT_NES_HEADER = [
				("platform", c_uint32, 32),
				("prgpages", c_uint8, 8),
				("chrpages", c_uint8, 8),
				("mapperlow", c_uint8, 4),
				("fourscreenmode", c_uint8, 1),
				("trainerpresent", c_uint8, 1),
				("srambatterybacked", c_uint8, 1),
				("mirroring", c_uint8, 1),
				("mappermid", c_uint8, 4),
				("headerversion", c_uint8, 2),
				("playchoice10", c_uint8, 1),
				("vsunisystem", c_uint8, 1),
				("mapperhigh", c_uint8, 4),
				("submapper", c_uint8, 4),
				("chrpageshigh", c_uint8, 4),
				("prgpageshigh", c_uint8, 4),
				("prgrambatterysize", c_uint8, 4),
				("prgramnotbatterysize", c_uint8, 4),
				("chrrambatterysize", c_uint8, 4),
				("chrramnotbatterysize", c_uint8, 4),
				("reserved_0", c_uint8, 6),
				("dendypalmode", c_uint8, 1),
				("ntsc", c_uint8, 1),
				("vshardware", c_uint8, 8),
				("reserved_1", c_uint8, 8),
				("reserved_2", c_uint8, 8)
			]



def structSize(struct):
	size = 0;
	for field in struct:
		size += field[2]
	return size

class NESHeaderStruct(ctypes.LittleEndianStructure):
		_fields_ = STRUCT_NES_HEADER

class NESHeader(ctypes.Union):
		_fields_ = [("b", NESHeaderStruct), ("asbytes", c_uint8 * int(structSize(STRUCT_NES_HEADER)/8))]
	

class NESRom:
	
	def __init__(self):
		self.header = NESHeader()
		self.prgpages = list()
		self.chrpages = list()

	def load_from_file(self, filename):
		with open(filename, "rb") as f:
			self.header.asbytes = (ctypes.c_ubyte*0x10)(*(f.read(0x10)))
			for bank in range(0, self.header.b.prgpages):
				self.prgpages.append(f.read(0x4000))
			for bank in range(0, self.header.b.chrpages):
				self.chrpages.append(f.read(0x4000))

	def __str__(self):
		string = "Headers:\n"
		for b in STRUCT_NES_HEADER:
			string += "  %s: %02X\n" % (b[0], getattr(self.header.b, b[0]))

		string += "PRG Pages: %d\n" % len(self.prgpages)
		return string
