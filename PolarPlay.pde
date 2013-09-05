final int WIN_X = 800;
final int WIN_Y = 600; 

final int P_AMNT = 20000;

import java.util.Vector;
import java.lang.Math;

boolean mouseDown = false;

class Point
{
  private float _x;
  private float _y;
  private float _r;
  private float _r_bak;
  
  public int r;
  public int g;
  public int b;
  
  public Point(float x, float y)
  {
    _x = x;
    _y = y;
    _r = 1+(float)Math.random()*0.10;
    _r_bak = _r;
    
    r = 255;
    g = 0;
    b = 0;
  }
  
  public void Draw()
  {
    stroke(r,g,b);
    point(_x%WIN_X,_y%WIN_Y);
  }
  
  public void SetXY(float x, float y)
  {
    _x = x;
    _y = y;
  }
  
  public float[] GetXY()
  {
    float[] arr = {_x,_y};
    return arr;
  }
  
  public void IncrementXY(float x, float y)
  {
    _x += x;
    _y += y;
  }
  
  public void MoveDirection(double d)
  {
    _y += (_r)*Math.sin(d);
    _x += (_r)*Math.cos(d);
  }
  
  public void SetPolarRadius(float r)
  {
    _r = r;
  }
  
  public void IncrementPolarRadius(float r)
  {
    _r += r;
    if (_r < 0) _r = 0; 
  }
  
  public void MoveToPoint(int x, int y)
  {
    this.MoveDirection(Math.atan2(y-_y,x-_x));
  }
  
  public void MoveFromPoint(int x, int y)
  {
    this.MoveDirection(Math.atan2(_y-y,_x-x));
  }
  
  public void MovePerpendicularToPoint(int x, int y)
  {
    this.MoveDirection(Math.atan2(y-_y,x-_x)-(HALF_PI));
  }
  
  public void MovePerpendicularToPoint(int x, int y, float o)
  {
    this.MoveDirection(Math.atan2(y-_y,x-_x)-(HALF_PI+o));
  }
  
  public void ResetPolarRadius()
  {
    _r = _r_bak;
  }
}

Vector<Point> p_vec = new Vector<Point>();

void setup()
{
  size(WIN_X,WIN_Y);
  noSmooth();
  background(0,0,0);
  for (int i = 0; i < P_AMNT; i++)
  {
    p_vec.add(new Point((WIN_X/2)+(float)(i*Math.random()*0.01), (WIN_Y/2)-(float)(i*Math.random()*0.01)));
  }
  for (int i = 0; i < p_vec.size(); i++)
  {
    p_vec.get(i).r -= i*0.02;
    p_vec.get(i).g += i*0.02;
  }
}

void mousePressed()
{ 
  /*
  for(Point pp: p_vec)
  {
    pp.IncrementPolarRadius((float)((float)Math.random()*1+(Math.hypot(Math.abs(pp.GetXY()[0]-mouseX)*1.5,Math.abs(pp.GetXY()[1]-mouseY)*1.5)*0.005)));
  }
  */
  mouseDown = true;
}

void mouseReleased()
{
  for(Point p: p_vec)
  {
    p.ResetPolarRadius();
  }
  mouseDown = false;
}

void keyReleased()
{
  for(Point p: p_vec)
  {
    p.ResetPolarRadius();
  }
}

void draw()
{
  background(0,0,0);
  for(Point p: p_vec)
  {
    p.Draw();
    if (keyPressed && key == 'c')
    {
      if (key == 'c')
      {
        p.MoveToPoint(WIN_X/2,WIN_Y/2);
      }
      /*
      else if ()
      {
        p.MovePerpendicularToPoint(WIN_X/2,WIN_Y/2);
      }
      */
    }
    if (mouseDown)
    {
      if ( mouseButton == LEFT )
      {
        p.MoveToPoint(mouseX,mouseY);
      }
      else
      {
        p.MoveFromPoint(mouseX,mouseY);
      }
    }
    else
    {
      if (keyPressed)
      {
        if (key == 'o')
        {
          p.MovePerpendicularToPoint(WIN_X/2,WIN_Y/2);
        }
        else if (key == 'g')
        {
          p.MovePerpendicularToPoint(WIN_X/2,WIN_Y/2,-0.1);
        }
        else if (key == 'r')
        {
          p.MovePerpendicularToPoint(WIN_X/2,WIN_Y/2,0.1);
        }
      }
      else
      {
        p.MoveDirection(Math.toRadians(frameCount));
      }
      if (frameCount % 150 == 0) p.IncrementPolarRadius((float)Math.random()*0.5);
    }
  }
}
