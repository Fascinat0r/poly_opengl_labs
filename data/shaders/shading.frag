#version 330 core

in VS_OUT {
    vec3 FragPos;
    vec3 Normal;
    vec2 TexCoords;
    vec4 FragPosLightSpace;
} fs_in;

uniform vec3 viewPos;

struct DirLight {
    vec3 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform DirLight dirLight;

uniform sampler2D diffuseTexture;
uniform sampler2D shadowMap;

uniform vec4 particleColor;
uniform bool useParticleColor;

float ShadowCalculation(vec4 fragPosLightSpace)
{
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    projCoords = projCoords * 0.5 + 0.5;

    vec4 texColor = texture(diffuseTexture, fs_in.TexCoords);
    if (texColor.a < 0.1)
    return 0.0;

    float closestDepth = texture(shadowMap, projCoords.xy).r;
    float currentDepth = projCoords.z;

    float shadow = currentDepth > closestDepth + 0.005 ? 1.0 : 0.0;

    if (projCoords.z > 1.0)
    shadow = 0.0;

    return shadow;
}



out vec4 FragColor;

vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir, vec3 diffuseColor)
{
    vec3 lightDir = normalize(-light.direction);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = light.diffuse * diff * diffuseColor;
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = light.specular * spec;
    return (light.ambient + diffuse + specular);
}

void main()
{
    if (useParticleColor) {
        FragColor = particleColor;
        return;
    }

    vec3 norm = normalize(fs_in.Normal);
    vec3 viewDir = normalize(viewPos - fs_in.FragPos);


    vec4 texColor = texture(diffuseTexture, fs_in.TexCoords);


    if (texColor.a < 0.1)
    discard;

   
    vec3 lighting = CalcDirLight(dirLight, norm, viewDir, texColor.rgb);
    float shadow = ShadowCalculation(fs_in.FragPosLightSpace);
    lighting = (1.0 - shadow) * lighting;

   
    FragColor = vec4(lighting, texColor.a);
}
