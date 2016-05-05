#include <iostream>
#include <vector>
#define True 1
#define False 0

using namespace std;

int main()
{
	double num_dou;


			scanf("%f",&num_dou);
	if(num_dou>=0)
	{
		if(num_dou==0)
		{
			printf("Zero");
	
		}
		else
		{
			printf("Positive number");
	
		}
	
	}
	else
	{
		printf("Negative number");

	}
	return 0;
}
