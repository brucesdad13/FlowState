uniform sampler2D bgl_RenderedTexture;
vec2 texcoord = vec2(gl_TexCoord[0]).st;
float sat = 0.6;

vec4 gradient(vec4 coo)
{
	vec4 stripes = coo;
    float sat = 0.9;
    float brt = -0.0;
    float l = (stripes.r+stripes.g+stripes.b)*0.733+brt;
	stripes.r =  pow((l*(1-sat))+((stripes.r)*sat)*1.05,sat);
	stripes.g = pow((l*(1-sat))+((stripes.g)*sat),sat);
	stripes.b = pow((l*(1-sat))+((stripes.b)*sat)*1.075,sat);
	stripes.a = 1.0;
	return stripes;
}

void main (void) 
{ 		
	vec4 value = texture2D(bgl_RenderedTexture, texcoord);
		

// 	gl_FragColor = gradient(vec4(clamp(gl_TexCoord[3].s,0.0,1.0)));
	gl_FragColor.rgb = gradient(value).rgb;
	gl_FragColor.a = 1.0;	
} 
