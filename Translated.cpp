#include <iostream>
#include <vector>
#include <algorithm>
#define True 1
#define False 0

using namespace std;

int main()
{
	long long n_lon;
	long long i_lon;
	vector<long long> a_vec;


	
	n_lon=50;
	for(i_lon=0;i_lon<n_lon;i_lon++)
	{
		a_vec.push_back(100-n_lon);
	
	}
	sort(a_vec.end(),a_vec.begin());
	return 0;
}
