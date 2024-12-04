#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void) {

    string text = get_string("Text: ");

    int length = strlen(text);
    int i = 0;
    int wordCounter = 0;
    int senCounter = 0;
    int letCounter = 0;

    while (i < length) {
        if (length == i) {
            break;
        }

        if (text[i] == ' ') {
            wordCounter++;
        } else if (text[i] == '.' || text[i] == '!' || text[i] == '?') {
            senCounter++;
        } else if (toupper(text[i]) >= 'A' && toupper(text[i]) <= 'Z') {
            letCounter++;
        }

        i++;
    }

    wordCounter++;

    float aveLetter = 100 * ((float) letCounter / (float) wordCounter);
    float aveSent = 100 * ((float) senCounter / (float) wordCounter);

    int grade = round(0.0588 * aveLetter - 0.296 * aveSent - 15.8);
    if (grade < 1) {
        printf("Before Grade 1\n");
    } else if (grade >= 16) {
        printf("Grade 16+\n");
    } else {
        printf("Grade %i\n", grade);
    }

}
