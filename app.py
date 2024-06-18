### Concerns:
# - How to check for repeating decimals within the inversion? At what point do we consider something "repeating"?

import decimal

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

def get_inversion(num_to_check):
    # NOTE: I'm adding one because we also want to see if there's more digits beyond our limit
    decimal.getcontext().prec = decimal_limit + 1 # To avoid float's 16-digit limit (of precision)
    if num_to_check == 0: # Avoid division by zero error
        return decimal.Decimal(0)
    return decimal.Decimal(1 / num_to_check)

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

def main():
    min = 0
    max = 100 # TODO: Change to 20,000
    for i in range(min, max+1):
        # TODO: Check for any repeating patterns within the decimal places of the inversion
        inversion_num = get_inversion(i)
        if is_finite(inversion_num):
            print(f"{green}{i}: {inversion_num}{reset}")
        else:
            print(f"{red}{i}: {inversion_num}{reset}")

if __name__ == '__main__':
    main()