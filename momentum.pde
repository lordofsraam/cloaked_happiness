final int WIN_X = 800;
final int WIN_Y = 600;

final int Friction = 0;

import java.util.Vector;
import java.lang.Math;
import java.util.Random;

class Circle
{
  private float _x;
  private float _y;
  
  private float _radius;
  
  private float _p;
  private float _m;
  private float _v;
  
  private float _d;
  
  public int r;
  public int g;
  public int b;
  
  public Circle(float x, float y)
  {
    r = 255;
    g = 0;
    b = 0;
    
    _x = x;
    _y = y;
    
    _radius = 10;
    this.Update();
  }
  
  public Circle(float x, float y, float radius)
  {
    r = 255;
    g = 0;
    b = 0;
    
    _x = x;
    _y = y;
    
    _radius = radius;
    this.Update();
  }
  
  public float GetRadius()
  {
    return _radius;
  }
  
  private void Update()
  {
    _m = _radius * 5;
    //_p = _m * _v;
  }
  
  public void ResetPos()
  {
    _x = 400;
    _y = 300;
  }
  
  public float Velocity()
  {
    return _p / _m;
  }
  
  public void MoveDirection(double d)
  {
    _y += (this.Velocity())*Math.sin(d);
    _x += (this.Velocity())*Math.cos(d);
  }
  
  private boolean needsBounce = true;
  public void Draw()
  {
    if (_p > 0 && frameCount % 10 == 0)
    {
      this._p -= Friction;
    }
    if (this._y + this._radius < WIN_Y)
    {
      //this.GravDown();
    }
    else if (_p < 0)
    {
      _p = 0;
    }
    if (this._x + this._radius/2 >= WIN_X && needsBounce)
    {
      this._d += (float)(Math.PI - _d*2);
      needsBounce = false;
      this.MoveDirection(_d);
    }
    else if (this._y + this._radius/2 >= WIN_Y && needsBounce)
    {
      this._d = (float)(2*Math.PI) - (_d);
      needsBounce = false;
      this.MoveDirection(_d);
    }
    else if (this._y - this._radius/2 <= 0 && needsBounce)
    {
      this._d = (float)(2*Math.PI) - (_d);
      needsBounce = false;
      this.MoveDirection(_d);
    }
    else if (this._x - this._radius/2 <= 0 && needsBounce)
    {
      this._d += (float)(Math.PI - _d*2);
      needsBounce = false;
      this.MoveDirection(_d);
    }
    else
    {
      this.MoveDirection(_d);
      needsBounce = true;
    }
    fill(r,g,b);
    ellipse(_x,_y,_radius,_radius);
  }
  
  public float GetMomentum()
  {
    return _p;
  }
  
  public void AddMomentum(float p)
  {
    _p += p;
  }
  
  public void MoveFromPoint(float x, float y)
  {
    float new_p = (float)Math.sqrt(Math.pow(Math.abs(x-this.GetXY()[0]),2)+Math.pow(Math.abs(y-this.GetXY()[1]),2))*7;
    
    this.MoveFromPoint(x,y,new_p);
  }
  
  private void GravDown()
  {
    //float new_p = (float)Math.sqrt(Math.pow(Math.abs(x-this.GetXY()[0]),2)+Math.pow(Math.abs(y-this.GetXY()[1]),2))*7;
    
    this.MoveFromPoint(_x,0);
  }
  
  public void MoveFromPoint(float x, float y, float p_offset)
  {
    float new_p = p_offset;
    
    float new_d = (float)Math.atan2(_y-y,_x-x);
    
    float new_py = (float)((new_p)*Math.sin(new_d));
    float new_px = (float)((new_p)*Math.cos(new_d));
    
    float py = (float)((_p)*Math.sin(_d));
    float px = (float)((_p)*Math.cos(_d));
    
    float true_new_d = (float)Math.atan2(new_py+py,new_px+px);
    
    _p = new_p;
    _d = true_new_d;
  }
  
  public float[] GetXY()
  {
    float[] arr = {_x,_y};
    return arr;
  }
}

Vector<Circle> circles = new Vector<Circle>();

//Below this line is code for rendering

void setup()
{
  size(WIN_X,WIN_Y);
  background(0,0,0);
  
  circles.add(new Circle(400,300,50));
  circles.add(new Circle(100,300,40));
  circles.add(new Circle(500,300,60));
}

void draw()
{
  background(0,0,0);
  for (int i = 0; i < circles.size(); i++)
  {
    for (int j = 0; j < circles.size(); j++)
    {
      if (circles.get(i) != circles.get(j))
      {
        float x_diff = Math.abs(circles.get(i).GetXY()[0] - circles.get(j).GetXY()[0]);
        float y_diff = Math.abs(circles.get(i).GetXY()[1] - circles.get(j).GetXY()[1]);
        
        float r_bound = circles.get(i).GetRadius()/2 + circles.get(j).GetRadius()/2;
        if ( x_diff <= r_bound && y_diff <= r_bound)
        {
          println("Touch");
          circles.get(i).MoveFromPoint(circles.get(j).GetXY()[0],circles.get(j).GetXY()[1],circles.get(j).GetMomentum());
          circles.get(j).MoveFromPoint(circles.get(i).GetXY()[0],circles.get(i).GetXY()[1],circles.get(i).GetMomentum());
        }
      }
    }
    circles.get(i).Draw();
  }
}

void mousePressed()
{
  if (mouseButton == LEFT)
  {
    for(Circle c: circles)
    {
      c.MoveFromPoint(mouseX,mouseY);
    }
  }
  else
  {
    for(Circle c: circles)
    {
      c.ResetPos();
    }
  }
}
