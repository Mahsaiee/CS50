#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gray = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = gray;
            image[i][j].rgbtGreen = gray;
            image[i][j].rgbtBlue = gray;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaR = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            if (sepiaR > 255)
            {
                sepiaR = 255;
            }
            int sepiaG = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            if (sepiaG > 255)
            {
                sepiaG = 255;
            }
            int sepiaB = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);
            if (sepiaB > 255)
            {
                sepiaB = 255;
            }

            image[i][j].rgbtRed = sepiaR;
            image[i][j].rgbtGreen = sepiaG;
            image[i][j].rgbtBlue = sepiaB;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int start = 0;
        int end = width - 1;

        while (start < end)
        {
            RGBTRIPLE holder = image[i][start];
            image[i][start] = image[i][end];
            image[i][end] = holder;

            start++;
            end--;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sumR = 0;
            float sumG = 0;
            float sumB = 0;
            int count = 0;

            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    int newI = i + k;
                    int newJ = j + l;

                    if (newI >= 0 && newI < height && newJ >= 0 && newJ < width)
                    {
                        sumR += copy[newI][newJ].rgbtRed;
                        sumG += copy[newI][newJ].rgbtGreen;
                        sumB += copy[newI][newJ].rgbtBlue;
                        count++;
                    }
                    else
                    {
                        continue;
                    }
                }
            }
            image[i][j].rgbtRed = round((float) sumR / count);
            image[i][j].rgbtGreen = round((float) sumG / count);
            image[i][j].rgbtBlue = round((float) sumB / count);
        }
    }
}
