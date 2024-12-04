#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int BLOCK_SIZE = 512;
const char *OUTPUT_EXT = "jpg";

void generateFileName(int count, char *buffer)
{
    sprintf(buffer, "%03d.%s", count, OUTPUT_EXT);
}

bool isJpg(uint8_t buffer[BLOCK_SIZE])
{
    return (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            ((buffer[3] >> 4) == 0xe));
}

int main(int argc, char *argv[])
{
    int fileCount = 0;

    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Can't open file %s", argv[1]);
        return 1;
    }

    FILE *output = NULL;
    char res[7];

    // Create a buffer for a block of data
    uint8_t buffer[BLOCK_SIZE];

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        if (isJpg(buffer))
        {
            // Found a new JPG, close previous file (if any)
            if (output != NULL)
                fclose(output);

            // Create JPEGs from the data
            generateFileName(fileCount++, res);

            output = fopen(res, "w");
            if (output == NULL)
            {
                printf("Failed to create image file %s, exiting..\n", res);
                fclose(card);
                return 1;
            }
        }

        // If JPG was previously found, continue writing data to the file
        if (output != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, output);
        }
    }

    fclose(output);
    fclose(card);
}
