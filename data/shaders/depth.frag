#version 330 core

in vec2 TexCoords;                
uniform sampler2D diffuseTexture; 

void main()
{
    vec4 texColor = texture(diffuseTexture, TexCoords);

   
    if (texColor.a < 0.1)
        discard;

   
    gl_FragDepth = gl_FragCoord.z;
}
