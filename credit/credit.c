#include <stdio.h>
#include <cs50.h>

string isValid(int length, int start, int checkSum) {

    if (checkSum % 10 != 0) {
        return "INVALID\n";
    }

    if (start == 34 || start == 37) {
        if (length == 15) {
            return "AMEX\n";
        }
    }

    if (start >= 51 && start <= 55) {
        if (length == 16) {
            return "MASTERCARD\n";
        }
    }

    if (start / 10 == 4) {
        if (length == 16 || length == 13) {
            return "VISA\n";
        }
    }

    return "INVALID\n";

}

int main(void) {

    long num = get_long("Number: ");

    int counter = 0;
    int total = 0;
    int digit, temp, dig1, dig2;
    while (num != 0) {
        digit = num % 10;
        num = num / 10;

        dig2 = dig1;
        dig1 = digit;

        if (counter % 2 == 0) {
            total += digit;
        } else {
            temp = 2 * digit;
            while (temp != 0) {
                total += temp % 10;
                temp = temp / 10;
            }
        }
        counter++;
    }

    printf("%s", isValid(counter, dig1 * 10 + dig2, total));
}
