#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

//             {a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p,  q, r, s, t, u, v, w, x, y, z};
int values[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int main(void) {
    string p1 = get_string("Player 1: ");
    string p2 = get_string("Player 2: ");
    int p1Total = 0;
    int p2Total = 0;

    int pLength = strlen(p1);
    for (int i = 0; i < pLength; i++) {
        char c = toupper(p1[i]);
        if (c >= 'A' && c <= 'Z') {
            p1Total += values[c - 'A'];
        }
    }

    pLength = strlen(p2);
    for (int i = 0; i < pLength; i++) {
        char c = toupper(p2[i]);
        if (c >= 'A' && c <= 'Z') {
            p2Total += values[c - 'A'];
        }
    }

    if (p1Total > p2Total) {
        printf("Player 1 wins!\n");
    } else if (p1Total < p2Total) {
        printf("Player 2 wins!\n");
    } else {
        printf("Tie!\n");
    }
}
