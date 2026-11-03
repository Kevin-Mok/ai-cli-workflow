#version 120
uniform sampler2D desktop;
uniform sampler2D texture;
varying vec2 uvCoord;
void main() {
    vec3 screen = texture2D(desktop, vec2(uvCoord.x, 1.0 - uvCoord.y)).rgb;
    float selected = texture2D(texture, uvCoord).a;
    gl_FragColor = vec4(screen * mix(0.6, 1.0, selected), 1.0);
}
