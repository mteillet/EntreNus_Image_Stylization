float lerp(float x, float y, float a)
{
    float ox = (1 - a) * x + a * y;
    return ox;
}

inline float smallest(float inArr[], int arrlen)
{
    float smt = 1.0e5f;
    for (unsigned int i = 0; i < arrlen; ++i)
    {
        smt = min(smt, inArr[i]);
    }

    return smt;
}

inline float largest(float inArr[], int arrlen)
{
    float lrg = 0.0f;
    for (unsigned int i = 0; i < arrlen; ++i)
    {
        lrg = max(lrg, inArr[i]);
    }

    return lrg;
}

inline float4 hsv(const float4& inRGB)
{
    float rgbArr[3] = {inRGB.x, inRGB.y, inRGB.z};
    float mx = largest(rgbArr, 3);
    float mn = smallest(rgbArr, 3);
    float diff = mx - mn;
    float h = 0.f;
    float s = 0.f;
    if (mx == mn)
    {
        h = 0.f;
    }
    else if (mx == inRGB.x)
    {
        h = fmod((60.f * ((inRGB.y - inRGB.z) / diff) + 360.f), 360.f);
    }
    else if (mx == inRGB.y)
    {
        h = fmod((60.f * ((inRGB.z - inRGB.x) / diff) + 120.f), 360.f);
    }
    else if (mx == inRGB.z)
    {
        h = fmod((60.f * ((inRGB.x - inRGB.y) / diff) + 240.f), 360.f);
    }

    if (mx == 0.f)
    {
        s = 0.f;
    }
    else
    {
        s = (diff/mx);
    }

    float v = mx;
    return float4(h, s, v, inRGB.w);
}

inline bool OutOfBounds(const int2& pos, const int2& res)
{
  return !(pos.x < res.x && pos.x > 0 && pos.y < res.y && pos.y > 0);
}

kernel SaturationKernel : ImageComputationKernel<ePixelWise>
{
  Image<eRead, eAccessPoint, eEdgeClamped> noiseInput; // the input image
  Image<eRead, eAccessRandom, eEdgeClamped> brushPattern;
  Image<eWrite, eAccessRandom> dst; // the output image

  param:
    int2 Resolution;
    int2 BrushRes;
    float a;
    float valueMin;
    float brushValueMin;
    int brushHalfSize;


  // In define(), parameters can be given labels and default values.
  void define() 
  {
    defineParam(Resolution, "Resolution", int2(1998,1920));
    defineParam(BrushRes, "BrushRes", int2(1024,1024));
    defineParam(a, "angle", 0.f);
    defineParam(valueMin, "Min_Value", 1.e-2f);
    defineParam(brushValueMin, "Brush_min_val", 1.e-3f);
    defineParam(brushHalfSize, "Brush_half_size", 16);
  }

  // The init() function is run before any calls to process().
  // Local variables can be initialized here.
  void init() 
  {

  }

  void process(int2 pos) 
  {
      const float4 noisePt = noiseInput();
      // Converting the noise input to HSV values - easier to use for luminance
      float4 _hsv = hsv(noisePt);

      // Beginning the drawing process only if the pixel underneath the position's luminance is detected as lighter than the current Brush
      // Meaning the lighter brushes will overlay on top of the darker ones
      if (_hsv.z > valueMin)
      {
        const int2 CurrentPos = pos;
        int2 orig = int2(pos.x - (brushHalfSize/2), pos.y - (brushHalfSize/2));
        //int2 upperbound = int2(pos.x + brushHalfSize, pos.y + brushHalfSize);
        int dist = brushHalfSize * 2;

        int2 brPos = int2(0, 0);
        while (brPos.x < dist)
        {
          brPos.y = 0;
          while (brPos.y < dist)
          {
            float posX = float(brPos.x);
            float posY = float(brPos.y);
            float _dist = float(dist);
            float x = (posX / _dist) * BrushRes.x;
            float y = (posY / _dist) * BrushRes.y;

            float4 brushColor = bilinear(brushPattern, x, y);
            brushColor *= noisePt;
            int2 writePos;
            int2 rpos = int2((brPos.x + orig.x) - pos.x, (brPos.y + orig.y) - pos.y);
            const float angle = lerp(-a, a, _hsv.z);
            writePos.x = orig.x + (rpos.x * cos(angle) - rpos.y * sin(angle));
            writePos.y = orig.y + (rpos.x * sin(angle) + rpos.y * cos(angle));
            //int2 writePos = orig + brPos;
            float4 brushHsv = hsv(brushColor);
            if (!OutOfBounds(writePos, Resolution) && brushHsv.z >= brushValueMin)
            {
              int2 pos[5] = {int2(1,0),int2(-1,0),int2(0,1),int2(0,-1),int2(0,0)};
              for (unsigned int idx=0; idx < 5; ++idx)
              {
                const int2 cvld = pos[idx];
                float4 test = dst(writePos.x + cvld.x, writePos.y + cvld.y);
                if (hsv(test).z < brushHsv.z)
                {
                  dst(writePos.x+cvld.x, writePos.y+cvld.y) = brushColor;//float4(posX / _dist, posY / _dist, 0.f, 1.f);
                }
              }
            }
            brPos.y++;
          }
          brPos.x++;
        }
      }
  }
};
