/*
 * ns_euler.h
 *
 *  Created on: Oct 3, 2011
 *      Author: Piero
 */

#include <iostream>
#include <stdio.h>
#include <math.h>
#include <functional>
#include <algorithm>
#include <sstream>

#ifndef NS_EULER_H_
#define NS_EULER_H_



namespace Euler
{
  class Number
  {
  public:
    double Value;
    Number(int v)
    {
      Value = v;
    }
    Number(double v)
    {
      Value = v;
    }

    /**
     * Overload operators to make it more int-like.
     */
    Number operator = (int v)
    {
      Value = v;
    }
    Number operator += (int v)
    {
      Value += v;
    }
    Number operator -= (int v)
    {
      Value -= v;
    }
    Number operator ++ ()
    {
      ++Value;
    }
    Number operator -- ()
    {
      --Value;
    }
    Number operator ++ (int)
    {
      Value++;
    }
    Number operator -- (int)
    {
      Value--;
    }
    int operator + (int i)
    {
      return (Value + i);
    }
    int operator - (int i)
    {
      return (Value - i);
    }
    Number operator + (Number n)
    {
      return (Value + n.Value);
    }
    Number operator - (Number n)
    {
      return (Value - n.Value);
    }
    /**
     * Casting operator overloads make it simple to turn a Number into convenient types
     */
    operator std::string() const
    {
      std::stringstream out;
      out << Value;
      return out.str();
    }
    operator int()
    {
      return Value;
    }
    operator double()
    {
      return Value;
    }

    bool IsDivisibleBy(int divisor)
    {
      if ( fmod(Value,divisor) == 0)
      {
  return true;
      }
      else
      {
	return false;
      }
    }

    bool IsEven()
    {
      if(IsDivisibleBy(Value,2))
      {
	return true;
      }
      else
      {
	return false;
      }
    }

    bool IsPrime()
    {
      for (int i = 2; i < Value; i++)
      {
	if( (i != Value) && (fmod(Value,i) == 0) )
	{
	  return false;
	}
	else
	{
	  return true;
	}
      }
    }

    bool HasFactor(int f)
    {
      if(fmod(Value,f) == 0)
      {
	return true;
      }
      else
      {
	return false;
      }
    }

    bool HasFactor(double f)
    {
      if(fmod(Value,f) == 0)
      {
	return true;
      }
      else
      {
	return false;
      }
    }

    bool IsPalindrome()
    {
      std::string testf;
      std::string testb = "";
      std::stringstream out;
      out << Value;
      testf = out.str();

      for (int i = (testf.size()-1);  i >= 0 ; i--)
      {
	testb =+ testf.at(i);
      }

      if (testb == testf)
      {
	return true;
      }
      else
      {
	return false;
      }
    }

    /** Made static overloads of methods incase you don't want to instatiate the class
     * just to use them.
     */
    static bool IsDivisibleBy(int subject, int divisor)
    {
      if ( subject % divisor == 0)
      {
	return true;
      }
      else
      {
	return false;
      }
    }

    static bool IsEven(int subject)
    {
      if(IsDivisibleBy(subject,2))
      {
	return true;
      }
      else
      {
	return false;
      }
    }
  };


  class FibonacciIterator
  {
    /**
     * How to use:
     * Inherit the class (you might want to send your class' constructor to this one).
     * Override the ForEach(int) method.
     * Put whatever code you want to work on the Fibonacci sequence in the ForEach() method.
     * (The ForEach() method will be handed each number in the Fibonacci sequence up to
     * the MaxValue.)
     */
  private:
    int MaxValue;
  public:
    FibonacciIterator(int maxFibValue)
    {
      MaxValue = maxFibValue;
    }
    virtual int ForEach(int) = 0;
    void run()
    {
      for(int last = 0, prev = 1, current = 1, temp = 0; current < MaxValue; temp = current + prev , last = prev , prev = current , current = temp)
      {
	ForEach(current);
      }
    }
  };



}

#endif /* NS_EULER_H_ */
