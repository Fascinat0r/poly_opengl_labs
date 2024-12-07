#version 330 core

layout (location = 0) in vec3 aPos;     
layout (location = 1) in vec2 aTexCoords;

out vec2 TexCoords;  
out vec4 FragPosLightSpace;

uniform mat4 model;
uniform mat4 lightSpaceMatrix;

void main()
{
    TexCoords = aTexCoords;
    FragPosLightSpace = lightSpaceMatrix * model * vec4(aPos, 1.0);
    gl_Position = FragPosLightSpace;
}
