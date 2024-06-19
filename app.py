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
    # - How many of the same last digits in a row should be required to consider it "repeating"?
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

    decimals = str(num).split(".")[1]
    digits_so_far = ""
    # For the 0.3333-like cases:
    is_repeating_single_digit = True
    repeating_count = 0
    repeats_required = 5 # Seems large enough to be very unlikely a false positive, but not so large that its position extends beyond the tail end of our limited window of digits.
    # For the 0.123123-like cases:
    keep_checking_for_repeating_patterns = True
    #repeating_pattern_count = 0
    #current_pattern_length = 0
    quit_at_iteration = (len(decimals) - 1) / 2 # This is half of the decimal length (-1 due to the loop's 0-indexing)

    print("decimals:", decimals) # TEMP

    # Loop backwards through the decimal digits (split)
    for i in range(len(decimals) - 1, 0, -1):
        print(f"i: {i}")
        next_digit = decimals[i - 1]

        ### Firstly, check for the 0.3333-like case:
        if is_repeating_single_digit:
            # Check if the current digit is the same as the next digit
            is_repeating_single_digit = decimals[i] == next_digit
            repeating_count += 1
            if repeating_count >= repeats_required:
                return True # Exit the loop early since we found what seems to be a valid pattern

        ### Secondly, check for the 0.123123-like case:
        if keep_checking_for_repeating_patterns:
            if len(digits_so_far) > 1:
                # Do the next several digits match the last pattern window's contents?
                next_potential_pattern_match = decimals[i - len(digits_so_far) + 1:i + 1] # NOTE: This was tricky since I was going backwards. Thanks for the help, ChatGPT. :)
                another_match_found = digits_so_far == next_potential_pattern_match

                pattern_repeats_required = get_pattern_repeats_required(len(decimals), len(digits_so_far))

                # TEMP
                print(f"another_match_found: {another_match_found} - next poential pattern match: {next_potential_pattern_match}")

                if another_match_found:
                    required_matches_found = False
                    # Instead of looping again, since we've found a pair of matching patterns already, just check the next N digits and compare again.
                    # Loop through the number of pattern_repeats_required and see if that many matches are found (minus the pair we already have). (remember we're going backwards)
                    # Check if the next X chars (length of current pattern) also match. Do this for as many times as needed based on the pattern_repeats_required value.
                    for j in range(i - len(digits_so_far), i - (len(digits_so_far) * pattern_repeats_required), -len(digits_so_far)):
                        # Check if the next X chars (length of current pattern) also match.
                        next_potential_pattern_match = decimals[j - len(digits_so_far) + 1:j + 1]
                        another_match_found = digits_so_far == next_potential_pattern_match
                        if not another_match_found:
                            break
                    return True

            #TEMP
            print(f"digits_so_far: {digits_so_far} -- next {len(digits_so_far)}")

            digits_so_far = str(decimals[i]) + digits_so_far # Remember we're going backwards, which is why we're appending it in reverse
            print(f"Updated digits so far:  {digits_so_far}")

        # Check if the next iteration count is no longer required
        if i + 1 <= quit_at_iteration:
            break

        print() # TEMP

    return False

def test_check_for_repeating_decimals():
    nums = {
        decimal.Decimal('0.333333333'): True,
        decimal.Decimal('0.123123'): True,
        decimal.Decimal('0.123456789'): False,
        decimal.Decimal('3.141592653'): False,
        decimal.Decimal('0.666666667'): False,
        decimal.Decimal('0.142857142857'): True,
        decimal.Decimal('0.101010101'): True,
        decimal.Decimal('0.987654321'): False,
        decimal.Decimal('0.27182818284'): False,
        decimal.Decimal('1.414213562'): False,
        decimal.Decimal('0.8532323232323'): True,
        decimal.Decimal('0.012344444'): True,
        decimal.Decimal('0.0123444445'): False,
        decimal.Decimal('2.718281828'): True,
        decimal.Decimal('1.618033988'): False,
        decimal.Decimal('0.99998888777766665555444433332222111100001'): False,
        decimal.Decimal('0.123456789987654321123456789987654321'): True,
    }

    num_passed = 0
    num_failed = 0

    for num, expected in nums.items():
        repeats = check_for_repeating_decimals(num)
        if repeats == expected:
            num_passed += 1
            print(f"{green}PASS{reset}: {num} repeats: {repeats}{reset}")
        else:
            num_failed += 1
            print(f"{red}FAIL{reset}: {num} repeats: {repeats} {red}(expected {expected}){reset}")

    print(f"\nTest Results: {green}{num_passed} passed{reset}, {red}{num_failed} failed{reset}")

# How many digits are there? We should use that alongside the number of current pattern chars to calculate how many patterns we should require
def get_pattern_repeats_required(decimal_length, current_pattern_length):
    #print(f"decimal_length: {decimal_length}, current_pattern_length: {current_pattern_length}")

    #########################################
    # TODO: Implement this function's logic #
    #########################################

    TEMP_PLACEHOLDER = 2

    return TEMP_PLACEHOLDER

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
        num_to_check = decimal.Decimal(args.single_check)
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