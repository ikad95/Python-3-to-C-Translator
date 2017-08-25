#include <iostream>
#include <vector>
#include <algorithm>
#define True 1
#define False 0

using namespace std;

int main()
{
	double C_dou;
	double F_dou;
	long long i_lon;


	printf("Enter temperature in degree Celcius : \n");
	scanf("%lf",&C_dou);
	printf("In degree Farenheit : \n");
	F_dou=(9*C_dou/5)+32;
	printf("%lf",F_dou);
	if(C_dou>40)
	{
		printf("You're in Durgapur!");
	
	}
	for(i_lon=0;i_lon<10000;i_lon++)
	{
		printf("hello world");

	}
	return 0;
}
