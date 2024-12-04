#include "bmp.h"

// Helper
void copyImage(int hh, int ww, RGBTRIPLE table1[hh][ww], RGBTRIPLE table2[hh][ww]);
int calcEdgeValue(int gx, int gy);  // helper function

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width]);

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width]);

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width]);

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width]);
