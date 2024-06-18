### Concerns:
# - How to check for repeating decimals within the inversion? At what point do we consider something "repeating"?

import argparse
import decimal

min = 0
max = 100 # TODO: Change to 20,000
decimal_limit = 40

# Terminal foreground colors
red     = "\033[31m"
green   = "\033[32m"
blue    = "\033[34m"
yellow  = "\033[33m"
magenta = "\033[35m"
cyan    = "\033[36m"
white   = "\033[37m"
reset   = "\033[0m"

def get_inversion(num_to_check):
    # Set the precision to a higher value to avoid floating-point precision issues
    decimal.getcontext().prec = decimal_limit + 1  # Additional precision to ensure rounding
    if num_to_check == 0:  # Avoid division by zero error
        return decimal.Decimal(0)

    # Calculate the inversion
    inversion_result = decimal.Decimal(1) / decimal.Decimal(num_to_check)

    # Limit the decimal places
    quantize_format = decimal.Decimal('1.' + '0' * decimal_limit)  # Example: '1.000' for 3 decimal places
    limited_result = inversion_result.quantize(quantize_format, rounding=decimal.ROUND_DOWN)

    return limited_result

def get_decimal_count(num):
    num_str = str(num)
    if '.' not in num_str:
        return 0
    decimal_count = len(num_str.split('.')[1])
    return decimal_count

def is_finite(num):
    if get_decimal_count(num) < decimal_limit:
        result = True
    else:
        result = False
    return result

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('single_check', type=int, nargs='?', help='Check a specific number')
    parser.add_argument('-all', '--show_all', action='store_true', default=False, help='Show all numbers, even if they are not finite')
    parser.add_argument('-l', '--limit', type=int, help='The number of decimal places to check for repeating patterns')
    parser.add_argument('-m', '--min', type=int, help='The minimum number to check')
    parser.add_argument('-M', '--max', type=int, help='The maximum number to check')
    args = parser.parse_args()
    return args

def main():
    args = get_args()

    if args.show_all:
        print(f"Showing {cyan}ALL{reset} numbers between the range of {min:,} and {max:,}\n")
    else:
        print(f"Showing only the {cyan}valid{reset} numbers between the range of {min:,} and {max:,}\n")

    for i in range(min, max+1):
        # TODO: Check for any repeating patterns within the decimal places of the inversion
        inversion_num = get_inversion(i)
        if is_finite(inversion_num):
            print(f"{green}{i:,}: {inversion_num}{reset}")
        else:
            if args.show_all:
                print(f"{red}{i:,}: {inversion_num}{reset}")

if __name__ == '__main__':
    print("\033c") # Quick call to clear terminal screen
    main()