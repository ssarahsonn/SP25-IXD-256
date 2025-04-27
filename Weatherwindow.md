# Weather Window 
## Introduction
Weather Window is an interactive physical prototype that brings real-time weather information into your daily environment in a way that’s both functional and ambient. Instead of displaying simple numbers or icons, the Weather Window uses light, movement, and tactile controls to create an intuitive, sensory experience of the weather—right inside your home or office. Designed for those who want to spend less time checking their phones, it offers a calming, glanceable alternative to digital screens.

## Context & Use Case
Weather Window is intended for use in personal or shared indoor spaces—like bedrooms, living rooms, kitchens, or offices—where people often begin their day. The device provides a quick, ambient weather update as soon as someone approaches, eliminating the need to pick up a phone or ask a smart speaker. Beyond basic utility, it gently transforms the atmosphere of the room to reflect the current weather, creating a seamless transition between indoor and outdoor worlds.

## Intended Audience
This project is ideal for anyone who finds themselves habitually reaching for their phone for simple updates like the weather. Whether you’re looking to develop healthier digital habits or simply want to start your day in a more mindful way, Weather Window offers a more intentional, ambient approach to checking the weather.

## Implementation
Enclosure & Mechanical Design
The physical “window” is made from several acrylic panels, each hand-sandblasted to create a frosted effect. The panels are precisely glued together for a seamless, sturdy finish. At the top edge, a slot holds an RGB LED strip, which creates the ambient lighting effects that visually represent the current weather conditions.

## Hardware (Electronics)
RGB LED strip: Provides dynamic, color-based feedback for weather states.

Proximity (IR) sensor: Detects when someone approaches, automatically activating the display and lighting.

Angle unit (potentiometer): Allows users to cycle through weather forecasts (today, tomorrow, previous days) with a turn.

All components are integrated along the edge of the window for easy interaction.

## Software & Visuals
p5.js: Used to create dynamic weather animations—foggy, rainy, sunny, and snowy—which are projected onto the frosted panel.

Figma: For data visualization assets (temperature, icons) used in the prototype.

ProtoPie: For integrating p5.js visuals and Figma assets into a single interactive prototype, allowing for real-time updates and media mixing.

Below are code snippets for the weather animations:


**Sunny**
javascript
Copy
Edit
let layers = 10;
let maxRadius;
function setup() {
  createCanvas(800, 800);
  noStroke();
  colorMode(HSB, 360, 100, 100);
  maxRadius = min(width, height) * 0.55;
}
function draw() {
  background(0);
  translate(width / 2, height / 2);
  scale(0.6);
  let time = millis() * 0.002;
  let pulse = sin(time * 2.5) * 60;
  for (let i = layers; i > 0; i--) {
    let layerRatio = i / layers;
    let r = map(i, 1, layers, 100, maxRadius) + pulse * layerRatio;
    let alpha = map(i, 1, layers, 0.5, 3);
    let hue = map(i, 1, layers, 50, 15);
    fill(hue, 90, 100, alpha);
    beginShape();
    let wavyOffset = time * 1.2;
    let waveAmp = map(i, 1, layers, 10, 50);
    let waveFreq = map(i, 1, layers, 2, 12);
    for (let angle = 0; angle < TWO_PI; angle += 0.07) {
      let wave = sin(angle * waveFreq + i * 0.7 + wavyOffset) * waveAmp;
      let x = (r + wave) * cos(angle);
      let y = (r + wave) * sin(angle);
      vertex(x, y);
    }
    endShape(CLOSE);
  }
}

**Rainy**
javascript
Copy
Edit
let layers = [];
let t = 0;
let lightningTimer = 0;
let flashAlpha = 100;
let lightningFlash = true;
let boltPath = [];
function setup() {
  createCanvas(600, 600);
  noStroke();
  colorMode(HSB, 360, 100, 100);
  for (let i = 0; i < 10; i++) {
    layers.push(createGraphics(width, height));
    layers[i].colorMode(HSB, 360, 100, 100);
    layers[i].noStroke();
  }
  generateBoltPath();
  lightningTimer = millis() + random(1500, 4000);
}
function draw() {
  background(0);
  clearLayers();
  if (millis() > lightningTimer && !lightningFlash) {
    lightningFlash = true;
    flashAlpha = 100;
    generateBoltPath();
    lightningTimer = millis() + random(1500, 4000);
  }
  for (let i = 0; i < layers.length; i++) {
    drawRain(layers[i], t + i * 0.05, i);
    tint(255, 20 + i * 20);
    image(layers[i], 0, 0);
  }
  if (lightningFlash) {
    flashAlpha -= 2.5;
    if (flashAlpha <= 0) {
      lightningFlash = false;
      flashAlpha = 0;
    }
  }
  t += 0.01;
}
function generateBoltPath() {
  boltPath = [];
  let x = int(random(width * 0.3, width * 0.7));
  for (let y = 0; y < height; y += 20) {
    x += int(random(-20, 20));
    boltPath.push({ x: round(x / 10) * 10, y });
  }
}
function drawRain(pg, offset, layerIndex) {
  pg.clear();
  for (let x = 0; x < width; x += 10) {
    for (let y = 0; y < height; y += 20) {
      let noiseVal = noise(x * 0.01, y * 0.01, offset);
      if (noiseVal > 0.55) {
        let alpha = map(noiseVal, 0.55, 1, 10, 40);
        let fallSpeed = map(layerIndex, 0, layers.length, 0.5, 2);
        let yOffset = (t * 100 * fallSpeed + y) % height;
        let w = 2;
        let h = 20;
        let hue = 210;
        let sat = 5;
        let bright = 60;
        if (
          lightningFlash &&
          boltPath.some(p => abs(x - p.x) < 5 && abs(y - p.y) < 5)
        ) {
          bright = 100;
          sat = 0;
          alpha = flashAlpha;
          w = 3;
          h = 30;
        }
        pg.fill(hue, sat, bright, alpha);
        pg.ellipse(x, yOffset, w, h);
      }
    }
  }
}
function clearLayers() {
  for (let pg of layers) {
    pg.clear();
  }
}

**Snowy**
javascript
Copy
Edit
let layers = [];
let snowflakes = [];
let t = 0;
function setup() {
  createCanvas(600, 600);
  noStroke();
  for (let i = 0; i < 8; i++) {
    layers.push(createGraphics(width, height));
  }
  for (let i = 0; i < 80; i++) {
    snowflakes.push({
      x: random(width),
      y: random(-height, height),
      radius: random(1, 4),
      speed: random(0.5, 1.5),
      drift: random(-0.5, 0.5),
    });
  }
}
function draw() {
  background(0);
  for (let i = 0; i < layers.length; i++) {
    drawCloud(layers[i], t + i * 0.15);
    tint(255, 20 + i * 25);
    image(layers[i], 0, 0);
  }
  drawSnow();
  t += 0.01;
}
function drawCloud(pg, offset) {
  pg.clear();
  pg.noStroke();
  for (let x = 0; x < width; x += 10) {
    for (let y = 0; y < height; y += 10) {
      let n = noise(x * 0.01, y * 0.01, offset);
      if (n > 0.5) {
        let alpha = map(n, 0.5, 1, 5, 50);
        pg.fill(255, alpha);
        pg.ellipse(x, y, 30, 30);
      }
    }
  }
}
function drawSnow() {
  fill(255, 240);
  for (let flake of snowflakes) {
    let wind = map(noise(flake.y * 0.005, t), 0, 1, -0.5, 0.5);
    ellipse(flake.x, flake.y, flake.radius * 2);
    flake.y += flake.speed;
    flake.x += wind + flake.drift;
    if (flake.y > height) {
      flake.y = random(-50, 0);
      flake.x = random(width);
    }
  }
}

**Foggy**
javascript
Copy
Edit
let layers = [];
let t = 0;
function setup() {
  createCanvas(600, 600);
  noStroke();
  for (let i = 0; i < 10; i++) {
    layers.push(createGraphics(width, height));
  }
}
function draw() {
  background(30);
  clearLayers();
  for (let i = 0; i < layers.length; i++) {
    drawCloud(layers[i], t + i * 0.1);
    tint(255, 30 + i * 20);
    image(layers[i], 0, 0);
  }
  t += 0.01;
}
function drawCloud(pg, offset) {
  pg.clear();
  pg.noStroke();
  for (let x = 0; x < width; x += 10) {
    for (let y = 0; y < height; y += 10) {
      let noiseVal = noise(x * 0.01, y * 0.01, offset);
      if (noiseVal > 0.5) {
        let alpha = map(noiseVal, 0.5, 1, 10, 80);
        pg.fill(255, alpha);
        pg.ellipse(x, y, 30, 30);
      }
    }
  }
}
function clearLayers() {
  for (let pg of layers) {
    pg.clear();
  }
}

## Firmware (MicroPython)
The microcontroller is programmed using MicroPython (via Thonny).
Key responsibilities include:

Reading input from the proximity sensor and angle unit.

Controlling RGB LED effects in response to user input and detected presence.

Sending signals to ProtoPie to trigger specific screen changes and animations.

To connect the system, run the MicroPython code on Thonny, make sure ProtoPie Connect is set up for Arduino at the highest baud rate and correct port, and confirm the local ProtoPie interface is “running.”

## Integration
Thonny is used to upload and run the firmware. ProtoPie’s integration features allow real-time linkage between the hardware (sensors, LEDs) and digital weather visuals, ensuring that user actions (like turning the angle unit or approaching the sensor) immediately update both the lighting and the on-screen projection.

## State Diagram
(Refer to Google Drive Link at bottom of file)

## Conclusion
One challenge during development was integrating the angle unit and proximity sensor into the enclosure in a clean and user-friendly way. Limited by time and resources, I used double-sided tape to attach these components, which worked but felt like a temporary solution. In future iterations, I would prioritize designing dedicated mounts—using 3D printing or precisely cut acrylic slots—for a more seamless, intuitive, and visually integrated experience. This project highlighted for me the importance of considering both technical and physical design details from the very start.

## Flowchart and Demo Photo & Video

[Flowchart and Demo Photo & Video Google Drive Folder](https://drive.google.com/drive/folders/1FhZ_Sk9sxA3VqXrq39SCMkuBqH7y_fE5)


