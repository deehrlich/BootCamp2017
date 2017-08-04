#include <iostream>
#include <stdio.h>
#include <math.h>
#include <complex>

int main()
{
	using namespace std;
	complex<float> a;
	complex<float> b;
	complex<float> c;
	cout << "Enter a number";
	cin >> a;
	cout << "Enter a number";
	cin >> b;
	cout << "Enter a number";
	cin >> c;
	complex<float> root1;
	complex<float> root2;
	//float 2;
	//float 4;
	root1 = (-b + sqrt(b*b-float(4)*a*c))/(float(2)*a);
	root2 = (-b - sqrt(b*b-float(4)*a*c))/(float(2)*a);
	cout << "Rout 1 =  " << root1 << endl; 
	cout << "Rout 2 =  " << root2 << endl;
	return 0;

}
