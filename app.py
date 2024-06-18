### Concerns:
# - How to check for repeating decimals within the inversion? At what point do we consider something "repeating"?

import argparse
import decimal

min = 0
max = 100 # TODO: Change to 20_000
decimal_limit = 20

# Terminal foreground colors
red     = "\033[31m"
green   = "\033[32m"
blue    = "\033[34m"
yellow  = "\033[33m"
magenta = "\033[35m"
cyan    = "\033[36m"
white   = "\033[37m"
reset   = "\033[0m"

def check_for_repeating_decimals(num):
    # TODO: Loop through each digit, and check if it repeats. If it does, return True. If it doesn't, return False.
    # If all digits are checked and no repeats are found, return False.
    # NOTE: Split this into two processes: one for 0.3333 and the other for 0.123123
    # NOTE: ACTUALLY, NO! Combine both to prevent re-checking through the same digits twice.
    # Hold onto two booleans: is_repeating and is_repeating_pattern.
    # Hold onto two more booleans: is_repeating_found and is_repeating_pattern_found.
    # Hold onto the ongoing chain of digits (up to the current iteration) to be used specifically to check the is_repeating_pattern boolean.
    # Hold onto the number of repeating patterns so far (per iteration)?

    # NOTE: Start backwards! We can just could how many of the "same" last digits there are (to be used for the 0.3333 case).

    # RULES:
    # - How many of the same last digits in a row should be reuqired to consider it "repeating"?
    #   Answer: 5?
    # - How many repeating sequences should be required to consider it "repeating" (FROM THE TAIL)?
    #   Answer: 2? Nah, it should depend on how many characters there are in the pattern (if there's a lot, maybe 2 will be enough),
    #   but if it's a short pattern, maybe something more like 5 or 6 would be required.
    #   Should it be a fraction such as 1/3 of the pattern length?

    # 0. Convert to string, capturing only the decimal digits (split by ".")
    # 1. Start at first decimal digit
    # 2. Check if the next digit is the same as the first decimal digit.
    # 3. If it is, set is_repeating to True and check if the next digit is the same as the second decimal digit. If it's not, set is_repeating to False
    # 4. If it is, set is_repeating_pattern to True and continue checking the pattern repeating these steps.

    # Loop backwards through the decimal digits (split)
    pass

def test_check_for_repeating_decimals():
    nums = {
        0.333333333: True,
        0.123123:    True,
        0.123456789: False,
        3.141592653: False,
    }
    for num, expected in nums.items():
        repeats = check_for_repeating_decimals(num)
        if repeats == expected:
            print(f"{green}PASS{reset}: {num} repeats: {repeats}")
        else:
            print(f"{red}FAIL{reset}: {num} repeats: {repeats} (expected {expected})")

def get_inversion(num_to_check):
    global decimal_limit
    # Set the precision to a higher value to avoid floating-point precision issues
    decimal.getcontext().prec = decimal_limit + 1  # Additional precision to ensure rounding
    if num_to_check == 0:  # Avoid division by zero error
        return decimal.Decimal('0.0')

    # Calculate the inversion
    inversion_result = decimal.Decimal(1) / decimal.Decimal(num_to_check)

    # Convert the result to a string
    result_str = str(inversion_result)

    # Find the decimal point
    if '.' in result_str:
        integer_part, decimal_part = result_str.split('.')
        # Trim the decimal part to the desired length
        trimmed_decimal_part = decimal_part[:decimal_limit]
        # Combine the integer part and the trimmed decimal part
        trimmed_result = integer_part + '.' + trimmed_decimal_part
    else:
        # If there's no decimal part, return the integer part as is
        trimmed_result = result_str

    return decimal.Decimal(trimmed_result)

def get_decimal_count(num):
    num_str = str(num)
    if '.' not in num_str:
        return 0
    decimal_count = len(num_str.split('.')[1])
    return decimal_count

def is_finite(num):
    global decimal_limit
    if get_decimal_count(num) < decimal_limit:
        result = True
    else:
        result = False
    return result

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('single_check', type=int, nargs='?', help='Check a specific number')
    parser.add_argument('-a', '--all', action='store_true', default=False, help='Show all numbers, even if they are not finite')
    parser.add_argument('-l', '--limit', type=int, help='The number of decimal places to check for repeating patterns')
    parser.add_argument('-m', '--min', type=int, help='The minimum number to check')
    parser.add_argument('-M', '--max', type=int, help='The maximum number to check')
    parser.add_argument('-t', '--test', action='store_true', default=False, help='Run validation test against check_for_repeating_decimals()')
    args = parser.parse_args()
    return args

def main():
    global min, max, decimal_limit

    args = get_args()

    if args.test:
        test_check_for_repeating_decimals()
        return

    if args.single_check:
        print("Checking single entry...")
        num_to_check = args.single_check
        inversion_num = get_inversion(num_to_check)
        if is_finite(inversion_num):
            print(f"{green}{num_to_check:,}: {inversion_num}{reset}")
        else:
            print(f"{red}{num_to_check:,}: {inversion_num}{reset}")
        return

    if args.min:
        min = args.min
    if args.max:
        max = args.max

    print(f"Decimal limit set to {cyan}{decimal_limit}{reset} decimal places.\n")
    if args.all:
        print(f"Showing {cyan}ALL{reset} numbers between the range of {min:,} and {max:,}\n")
    else:
        print(f"Showing only the {cyan}valid{reset} numbers between the range of {min:,} and {max:,}\n")

    for i in range(min, max+1):
        # TODO: Check for any repeating patterns within the decimal places of the inversion
        inversion_num = get_inversion(i)
        if is_finite(inversion_num):
            print(f"{green}{i:,}: {inversion_num}{reset}")
        else:
            if args.all:
                print(f"{red}{i:,}: {inversion_num}{reset}")

if __name__ == '__main__':
    print("\033c") # Quick call to clear terminal screen
    main()