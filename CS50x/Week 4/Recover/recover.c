#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    unsigned char *holder = malloc(512);
    if (holder == NULL)
    {
        fclose(file);
        return 1;
    }

    char *filename = malloc(8 * sizeof(char));
    if (filename == NULL)
    {
        fclose(file);
        free(holder);
        return 1;
    }

    int image = 0;

    while (fread(holder, sizeof(unsigned char), 512, file) == 512)
    {
        if (holder[0] == 0xff && holder[1] == 0xd8 && holder[2] == 0xff && (holder[3] & 0xf0) == 0xe0)
        {
            sprintf(filename, "%03i.jpg", image);
            FILE *img = fopen(filename, "w");
            fwrite(holder, 1, 512, img);
            fclose(img);
            image++;
        }
        else if (image != 0)
        {
            FILE *img = fopen(filename, "a");
            fwrite(holder, 1, 512, img);
            fclose(img);
        }
    }

    fclose(file);
    free(holder);
    free(filename);

    return 0;
}