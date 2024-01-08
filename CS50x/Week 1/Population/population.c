#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int initialPopulation;
    do
    {
        initialPopulation = get_int("Start Size: ");
    }
    while (initialPopulation < 9);

    // TODO: Prompt for end size
    int finalPopulation;
    do
    {
        finalPopulation = get_int("End Size: ");
    }
    while (finalPopulation < initialPopulation);

    // TODO: Calculate number of years until we reach threshold
    int years = 0;
    while (initialPopulation < finalPopulation)
    {
        int newLlamas = initialPopulation / 3;
        int llamasPassedAway = initialPopulation / 4;
        initialPopulation = initialPopulation + newLlamas - llamasPassedAway;
        years++;
    }
    // TODO: Print number of years
    printf("Years: %i\n", years);
}
