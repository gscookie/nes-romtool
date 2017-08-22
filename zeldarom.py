import nesrom
import ctypes, struct
c_uint8 = ctypes.c_uint8
c_uint32 = ctypes.c_uint32


CharMapNPC = {	
	'00': '0',
	'01': '1',
	'02': '2',
	'03': '3',
	'04': '4',
	'05': '5',
	'06': '6',
	'07': '7',
	'08': '8',
	'09': '9',
	'0A': 'a',
	'0B': 'b',
	'0C': 'c',
	'0D': 'd',
	'0E': 'e',
	'0F': 'f',
	'10': 'g',
	'11': 'h',
	'12': 'i',
	'13': 'j',
	'14': 'k',
	'15': 'l',
	'16': 'm',
	'17': 'n',
	'18': 'o',
	'19': 'p',
	'1A': 'q',
	'1B': 'r',
	'1C': 's',
	'1D': 't',
	'1E': 'u',
	'1F': 'v',
	'20': 'w',
	'21': 'x',
	'22': 'y',
	'23': 'z',
	'24': ' ',
	'25': '~',
	'28': ',',
	'29': '!',
	'2A': "'",
	'2B': '&', #rainbow
	'2C': '.',
	'2D': '"', #doubleheart
	'2E': '?',
	'2F': '-', #smiley
	'30': '+', #TM
	'31': '#', #Hashtag
	'32': '@',
	'40': "\n",
	'80': "\n",
	'C0': "\n\n"
	}

def rom_address_to_bank_offset(address):
	if address < 0x1C000:
		return address - 0x8000
	else:
		return address - 0xC000

class ZString():

	def __init__(self, address=0, bank=False, string=False, zmap=CharMapNPC):
		self.address = address
		self.zmap = zmap
		if bank:
			bankOffset = rom_address_to_bank_offset(address)
			self.read_ztext(bank, bankOffset)
		elif string:
			self.read_string(string)


	def read_ztext(self, bank, offset):
		self.ztext = list()
		EOF = False
		current_offset = offset
		while not EOF and (current_offset - offset) < 0x100:
			byte = bank[offset]
			self.ztext.append(byte)
			if (byte & 0xC0) == 0xC0:
				EOF = True
			offset += 1

	def read_string(self, string):
		pass

	def __str__(self):
		text = "$%04X: " % self.address
		count = 0
		size = 0
		for c in self.ztext:
			zchar = c & 0x3F
			if "%02X" % zchar in self.zmap:
				text += self.zmap["%02X" % zchar]
			else:
				text += "`%02X`" % zchar
			
			flags = c & 0xC0

			if flags:
				text += "\n"

			if flags == 0xC0:
				break
		return text


class TextTable():
	tableBank = 0
	tableOffset = 0x0

	def __init__(self):
		self.strings = list()

	def load_from_rom(self, size, bank, offset):
		self.tableBank = bank
		self.tableOffset = offset

		for pointer in struct.iter_unpack("<H", bank[offset : offset + (struct.calcsize("<H")*size)]):
			self.strings.append(ZString(address=pointer[0], bank=bank))

	
	def __str__(self):
		string = "Text Table @%0X:\n" % self.tableOffset
		for s in self.strings:
			string += "  %s" % str(s).replace("\n", "\n  ")
		return string


class ZeldaRom(nesrom.NESRom):
	def __init__(self):
		super().__init__()
		self.textTable = TextTable()

	def load_from_rom(self):
		self.textTable.load_from_rom(25, self.prgpages[1], 0)

	def __str__(self):
		string = super().__str__()
		string += str(self.textTable)
		return string