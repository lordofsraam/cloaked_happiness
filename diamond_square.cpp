#include <math.h>
#include <stdio.h>
#include <iostream>
#include <vector>

void Print2DArray(std::vector< std::vector<int> > arr)
{
  for (unsigned i = 0; i < arr.size(); i++)
	{
		for (unsigned j = 0; j < arr[i].size(); j++)
		{
			std::cout << arr[i][j] << ' ';
		}
		std::cout << std::endl;
	}
}

void Expand2DArray(std::vector< std::vector<int> > &arr)
{
    for (unsigned i = 0; i < arr.size(); i++)
	{
        unsigned j = 0;
        while (true)
		{
			std::vector<int>::iterator it = arr[i].begin();
            arr[i].insert(it+j+1,(int)floor((arr[i][j]+arr[i][j+1])/2.0));
            j += 2;
            if (j >= (arr[i].size()-1)) break;
		}
	}
    unsigned i = 0;
    while (true)
	{
        std::vector<int> temprow;
        for (unsigned j = 0; j < arr[i].size(); j++)
		{
			std::vector<int>::iterator it = temprow.begin();
			temprow.insert(it+j,(int)floor((arr[i][j]+arr[i+1][j])/2.0));
		}
		std::vector< std::vector<int> >::iterator it = arr.begin();
        arr.insert(it+i+1,temprow);
        i += 2;
        if (i >= (arr.size()-1)) break;
	}
}

int main()
{
	std::vector< std::vector<int> > matrix;
	
	int ta[] = {10,20};
	std::vector<int> r (ta,ta + sizeof(ta)/sizeof(int));
	int ta2[] = {30,40};
	std::vector<int> rr (ta2,ta2 + sizeof(ta2)/sizeof(int));
	
	matrix.push_back(r);
	matrix.push_back(rr);
	
	Print2DArray(matrix);
	
	Expand2DArray(matrix);
	
	Print2DArray(matrix);
}
