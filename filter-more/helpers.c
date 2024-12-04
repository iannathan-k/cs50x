#include "helpers.h"
#include "math.h"
#include <stdio.h>
#include <stdlib.h>

// Global Constants
int GX[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
int GY[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

// Helpers
void copyImage(int hh, int ww, RGBTRIPLE image1[hh][ww], RGBTRIPLE image2[hh][ww])
{
    for (int ii = 0; ii < hh; ii++)
    {
        for (int jj = 0; jj < ww; jj++)
        {
            image2[ii][jj] = image1[ii][jj];
        }
    }
}

int calcEdgeValue(int gx, int gy)
{
    int ret = round(sqrt(gx * gx + gy * gy));
    return (ret > 255) ? 255 : ret;
}

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // take the avg of R, G, B to determine the shade of grey
    for (int ii = 0; ii < height; ii++)
    {
        for (int jj = 0; jj < width; jj++)
        {
            int red = image[ii][jj].rgbtRed;
            int green = image[ii][jj].rgbtGreen;
            int blue = image[ii][jj].rgbtBlue;
            int gs = round((red + green + blue) / 3.0);
            image[ii][jj].rgbtRed = gs;
            image[ii][jj].rgbtBlue = gs;
            image[ii][jj].rgbtGreen = gs;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Any pixels on the left should end up on the right, vice versa
    for (int ii = 0; ii < height; ii++)
    {
        for (int jj = 0; jj < width / 2; jj++)
        {
            int tmpRed = image[ii][jj].rgbtRed;
            int tmpGreen = image[ii][jj].rgbtGreen;
            int tmpBlue = image[ii][jj].rgbtBlue;

            image[ii][jj].rgbtRed = image[ii][width - 1 - jj].rgbtRed;
            image[ii][jj].rgbtGreen = image[ii][width - 1 - jj].rgbtGreen;
            image[ii][jj].rgbtBlue = image[ii][width - 1 - jj].rgbtBlue;

            image[ii][width - 1 - jj].rgbtRed = tmpRed;
            image[ii][width - 1 - jj].rgbtGreen = tmpGreen;
            image[ii][width - 1 - jj].rgbtBlue = tmpBlue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // First, copy the original to image2
    RGBTRIPLE image2[height][width] = {};
    copyImage(height, width, image, image2);

    // The new value of each pixel would be the avg of the values
    // of all of the pixels that are within 1 row and column of the
    // original pixel (forming a 3x3 box).
    for (int ii = 0; ii < height; ii++)
    {
        // hh1 and hh2 are the vertical boundaries
        int hh1 = (ii == 0) ? ii : ii - 1;
        int hh2 = (ii == (height - 1)) ? ii : ii + 1;

        for (int jj = 0; jj < width; jj++)
        {
            // ww1 and ww2 are the horizontal boundaries
            int ww1 = (jj == 0) ? jj : jj - 1;
            int ww2 = (jj == (width - 1)) ? jj : jj + 1;

            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;
            int countBoxes = 0;
            for (int pp = hh1; pp <= hh2; pp++)
            {
                for (int qq = ww1; qq <= ww2; qq++)
                {
                    sumRed += image2[pp][qq].rgbtRed;
                    sumGreen += image2[pp][qq].rgbtGreen;
                    sumBlue += image2[pp][qq].rgbtBlue;
                    countBoxes++;
                }
            }

            // Modify the original image
            image[ii][jj].rgbtRed = round(sumRed / (double) countBoxes);
            image[ii][jj].rgbtGreen = round(sumGreen / (double) countBoxes);
            image[ii][jj].rgbtBlue = round(sumBlue / (double) countBoxes);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Take 3x3 grid for each pixel, then use Sobel operator

    // Test Data
    // height = 3;
    // width = 3;
    // image[0][0].rgbtRed = 0; image[0][0].rgbtGreen = 10; image[0][0].rgbtBlue = 25;
    // image[0][1].rgbtRed = 0; image[0][1].rgbtGreen = 10; image[0][1].rgbtBlue = 30;
    // image[0][2].rgbtRed = 40; image[0][2].rgbtGreen = 60; image[0][2].rgbtBlue = 80;
    // image[1][0].rgbtRed = 20; image[1][0].rgbtGreen = 30; image[1][0].rgbtBlue = 90;
    // image[1][1].rgbtRed = 30; image[1][1].rgbtGreen = 40; image[1][1].rgbtBlue = 100;
    // image[1][2].rgbtRed = 80; image[1][2].rgbtGreen = 70; image[1][2].rgbtBlue = 90;
    // image[2][0].rgbtRed = 20; image[2][0].rgbtGreen = 20; image[2][0].rgbtBlue = 40;
    // image[2][1].rgbtRed = 30; image[2][1].rgbtGreen = 10; image[2][1].rgbtBlue = 30;
    // image[2][2].rgbtRed = 50; image[2][2].rgbtGreen = 40; image[2][2].rgbtBlue = 10;

    // First, copy the original to image2
    RGBTRIPLE image2[height][width] = {};
    copyImage(height, width, image, image2);

    for (int ii = 0; ii < height; ii++)
    {
        // hh1, hh2 are height-boundaries of an image pixel
        int hh1 = ii - 1;
        int hh2 = ii + 1;
        for (int jj = 0; jj < width; jj++)
        {
            // ww1, ww2 are width-boundaries of an image pixel
            int ww1 = jj - 1;
            int ww2 = jj + 1;

            RGBTRIPLE val[3][3] = {}; // the 3x3 surrounding for each Pixel
            int xx = -1;              // index for "val", 0-2 only
            for (int pp = hh1; pp <= hh2; pp++)
            {
                xx++;
                if (pp < 0 || pp > (height - 1))
                    continue; // out of boundaries, assumes BLACK

                int yy = -1; // index for "val", 0-2 only
                for (int qq = ww1; qq <= ww2; qq++)
                {
                    yy++;
                    if (qq < 0 || qq > (width - 1))
                        continue; // out of boundaries, assumes BLACK

                    // populate the 3x3 with values from the original image
                    val[xx][yy] = image2[pp][qq];
                }
            }

            // Modify the original image
            int gxRed = 0, gyRed = 0;
            int gxGreen = 0, gyGreen = 0;
            int gxBlue = 0, gyBlue = 0;
            for (xx = 0; xx < 3; xx++)
            {
                for (int yy = 0; yy < 3; yy++)
                {
                    gxRed += val[xx][yy].rgbtRed * GX[xx][yy];
                    gyRed += val[xx][yy].rgbtRed * GY[xx][yy];
                    gxGreen += val[xx][yy].rgbtGreen * GX[xx][yy];
                    gyGreen += val[xx][yy].rgbtGreen * GY[xx][yy];
                    gxBlue += val[xx][yy].rgbtBlue * GX[xx][yy];
                    gyBlue += val[xx][yy].rgbtBlue * GY[xx][yy];
                }
            }
            image[ii][jj].rgbtRed = calcEdgeValue(gxRed, gyRed);
            image[ii][jj].rgbtGreen = calcEdgeValue(gxGreen, gyGreen);
            image[ii][jj].rgbtBlue = calcEdgeValue(gxBlue, gyBlue);
        }
    }
    return;
}
