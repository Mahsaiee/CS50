#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // ask for desired height
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // making right-aligned pyramid
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < (height - i - 1); k++)
        {
            printf(" ");
        }
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("\n"); // move to next line
    }
}