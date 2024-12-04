#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

bool validKey(string key) {
    int checkVal = 2015;

    if (strlen(key) != 26) return false;

    for (int i = 0; i < 26; i++) {
        if (toupper(key[i]) < 'A' || toupper(key[i]) > 'Z') return false;
        checkVal -= toupper(key[i]);
    }

    if (checkVal != 0) return false;

    for (int i = 0; i < 26; i++) {
        for (int j = i + 1; j < 26; j++) {
            if (key[j] == key[i]) return false;
        }
    }

    return true;
}

int main(int argc, char* argv[]) {
    string key = argv[1];
    if (argc != 2 || !validKey(key)) {
        printf("Usage ./substitution key\n");
        return 1;
    }

    string text = get_string("plaintext: ");
    char replace;

    printf("ciphertext: ");

    int length = strlen(text);
    for (int i = 0; i < length; i++) {
        if (text[i] >= 'a' && text[i] <= 'z') {
            printf("%c", tolower(key[text[i] - 'a']));
        } else if (text[i] >= 'A' && text[i] <= 'Z') {
            printf("%c", toupper(key[text[i] - 'A']));
        } else {
            printf("%c", text[i]);
        }
    }

    printf("\n");

    return 0;
}
