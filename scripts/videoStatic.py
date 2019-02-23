uniform sampler2D bgl_RenderedTexture;
uniform float timer;
uniform float rfNoise;
float frameScrolling = 1.38;
float frameShifting = 0.5;
float colorBurstNoise = 1.19;
float rf = clamp(rfNoise*.01,0.0,1.0);
float pi = 3.14159265;
float rand(vec2 co)
{
    float a = 12.9898;
    float b = 78.233;
    float c = 43758.5453;
    float dt= dot(co.xy ,vec2(a,b));
    float sn= mod(dt,3.14);
    return fract(sin(sn) * c);
}

void main()
{

    vec2 texcoord = vec2(gl_TexCoord[0]).st;
    float a = (rand(timer*texcoord)*2)-1;
    float b = (rand(timer*texcoord+1)*2)-1;
    float c = (rand(timer*texcoord+2)*2)-1;
    float e = (rand(timer*texcoord+3));
    float d = a+b+c;
    float cb = (sin((timer*100)+(((texcoord.y*12)+a)+(e*0.1))))*((rand(timer*vec2(0,texcoord.y))*2)-1)*rf*2;
    float vc = (rand(timer*vec2(1,1)))*rf*.6;
    vec4 image = vec4(0);
    int j;
    int i;
    float redShift = pow(sin((cb)+90),3)*cb;
    float greenShift = pow(sin((cb)),3)*cb;
    float blueShift = pow(sin((cb)+45),3)*cb;
    vec4 colorShift = vec4(redShift*rf, greenShift*rf, blueShift*rf, 1);
    image = clamp(pow(cb*colorBurstNoise,3)+(colorShift*2),0.0,1.0)+texture2D(bgl_RenderedTexture, texcoord + vec2(pow(cb*frameShifting,3), pow(vc*frameScrolling,3))); 
    
    float cm = 0.5;
    float lm = 0.7;
    vec4 asdf = vec4((d*lm)+(a*cm), (d*lm)+(b*cm), (d*lm)+(c*cm), 1);
    //vec4 asdf = dot(bgl_RenderedTexture.rgba,vec4(a, a, a,1));
    //vec4 asdf = bgl_RenderedTexture;
    float rssi = clamp(pow(rf,1.2),0.0,1.0);
    gl_FragColor = (asdf*rssi)+((image)*(1-rssi));
    //gl_FragColor = rf*((texture2D(bgl_RenderedTexture, texcoord)));
}