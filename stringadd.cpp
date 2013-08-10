#include <iostream>
#include <stdio.h>

std::string AddStringsAsUInts(std::string str1, std::string str2)
{
  std::string tr;
	
  //Make both strings the same size by filling the short one with '0's
	if (str1.size() > str2.size())
	{
		std::string temp;
		temp.append(str1.size()-str2.size(),'0');
		str2 = temp + str2;
	}
	else
	{
		std::string temp;
		temp.append(str2.size()-str1.size(),'0');
		str1 = temp + str1;
	}
	
	std::string res;
	int carry = 0;
	for (int i = (str1.size() > str2.size() ? str2.size() : str1.size()) - 1; i >= 0; i--)
	{
		int t = 0;
    //Do the math with chars minus the ASCII offset
		t = (str1.at(i)-48) + (str2.at(i)-48);
		if (carry != 0) t += carry;
    //Create a carry if the number is greater than 10
		if ((t/10) > 0 )
		{
			 carry = 1;
			 t-= 10;
		}
		else
		{
			carry = 0;
		}
		res.push_back(t+48);
	}
  
  //Add the extra one at the end if the new number has more digits
	if ( carry != 0 ) res.push_back('1');
  
  //Invert the string since we added from right to left
	for (int i = res.size()-1; i >= 0; i--)
	{
		tr.push_back(res.at(i));
	}
  
	return tr;
}

int main()
{
	
}
