#version 330 core
in vec4 FragPosLightSpace;

uniform sampler2D shadowMap;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform bool isShadowPass;

out vec4 FragColor;

float ShadowCalculation(vec4 fragPosLightSpace)
{
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    projCoords = projCoords * 0.5 + 0.5;
    float closestDepth = texture(shadowMap, projCoords.xy).r;
    float currentDepth = projCoords.z;
    float shadow = currentDepth > closestDepth + 0.005 ? 1.0 : 0.0;
    return shadow;
}

void main()
{
    if (isShadowPass) {
        FragColor = vec4(1.0);
    } else {
        float shadow = ShadowCalculation(FragPosLightSpace);
        vec3 lighting = mix(vec3(0.3), vec3(1.0), 1.0 - shadow);
        FragColor = vec4(lighting, 1.0);
    }
}
