#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrix;

out vec4 FragPosLightSpace;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    FragPosLightSpace = lightSpaceMatrix * model * vec4(aPos, 1.0);
}
