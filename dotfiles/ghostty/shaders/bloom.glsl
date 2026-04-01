// Subtle bloom shader for Ghostty
// Soft light bleed around bright text — refined, not flashy.

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec4 col = texture(iChannel0, uv);

    // Accumulate nearby bright pixels with a 2-pass box blur
    float radius = 2.0;
    vec4 bloom = vec4(0.0);
    float samples = 0.0;

    for (float x = -radius; x <= radius; x += 1.0) {
        for (float y = -radius; y <= radius; y += 1.0) {
            vec2 offset = vec2(x, y) / iResolution.xy;
            vec4 s = texture(iChannel0, uv + offset);
            // Only bloom bright fragments (text, cursor)
            float luminance = dot(s.rgb, vec3(0.2126, 0.7152, 0.0722));
            float weight = smoothstep(0.5, 1.0, luminance);
            bloom += s * weight;
            samples += 1.0;
        }
    }

    bloom /= samples;

    // Blend: original + subtle glow
    float intensity = 0.15;
    fragColor = col + bloom * intensity;
    fragColor.a = col.a;
}
