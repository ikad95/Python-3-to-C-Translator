#include <iostream>
#include <vector>
#include <algorithm>
#define True 1
#define False 0

using namespace std;

int main()
{
	double F_dou;
	double C_dou;


	printf("Enter temperature in degree Celcius : \n");
	scanf("%f",&C_dou);
	printf("In degree Farenheit : \n");
	F_dou=(9*C_dou/5)+32;
	printf("%f",F_dou);
	if(C_dou>40)
	{
		printf("You're in Durgapur!");

	}
	return 0;
}
