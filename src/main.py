import sys, secrets, argparse, os, enum

# list constants representing lists of characters.  The ranges are from the ASCII table.
SPECIAL_CHARACTERS = [chr(c) for c in (list(range(32, 48)) + list(range(58, 65)) + list(range(91, 97)) + list(range(123, 127)))]
UC_LETTER_CHARACTERS = [chr(c) for c in list(range(65, 91))]
LC_LETTER_CHARACTERS = [chr(c) for c in list(range(97, 123))]
NUMBER_CHARACTERS = [chr(c) for c in list(range(48, 58))]

#cryptographically random generator using the system hardware per PEP506
r = secrets.SystemRandom()

# char group bitmask.
class CharGroup(enum.Flag):
    BLANK = 0
    UCLETTERS = enum.auto()
    LCLETTERS = enum.auto()
    NUMBERS = enum.auto()
    SPECIALS = enum.auto()
    ALL = (LCLETTERS | UCLETTERS | NUMBERS | SPECIALS)

def random_string(slength: int = 10, types: CharGroup=CharGroup.ALL) -> str:
    characters = []
    if types & CharGroup.LCLETTERS: characters.extend(LC_LETTER_CHARACTERS)
    if types & CharGroup.UCLETTERS: characters.extend(UC_LETTER_CHARACTERS)
    if types & CharGroup.NUMBERS: characters.extend(NUMBER_CHARACTERS)
    if types & CharGroup.SPECIALS: characters.extend(SPECIAL_CHARACTERS)
    return ''.join(r.choices(population=characters, k=slength))

def argparser(argv):
    p = argparse.ArgumentParser(description="Generates a cryptographically random password of a specified length.")
    p.add_argument("length", type=int, help="The length of the password to generate.  Required.")
    p.add_argument("--letters", "-l", help="Use lower case letters", action="store_true")
    p.add_argument("--uppers", "-u", help="Use upper case letters", action="store_true")
    p.add_argument("--specials", "-s", help="Use special characters", action="store_true")
    p.add_argument("--numbers", "-n", help="Use numbers", action="store_true")
    return p.parse_args(argv)

def handle_arguments(argv):
    args = argparser(argv)
    chartypes = CharGroup.BLANK
    if args.letters: chartypes |= CharGroup.LCLETTERS
    if args.uppers: chartypes |= CharGroup.UCLETTERS
    if args.specials: chartypes |= CharGroup.SPECIALS
    if args.numbers: chartypes |= CharGroup.NUMBERS
    if not chartypes: chartypes = CharGroup.ALL
    print(f"Password: {random_string(int(args.length), chartypes)}")

def main(argv):
    handle_arguments(argv[1:])
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))