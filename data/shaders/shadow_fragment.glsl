#version 330 core
in vec4 FragPosLightSpace;
uniform sampler2D shadowMap;

void main()
{
    float shadow = texture(shadowMap, FragPosLightSpace.xy).r;
    gl_FragColor = vec4(vec3(shadow), 1.0);
}
