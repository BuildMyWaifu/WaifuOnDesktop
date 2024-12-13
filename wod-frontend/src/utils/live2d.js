import * as PIXI from 'pixi.js';
import {
  Live2DModel,
  MotionPreloadStrategy,
} from 'pixi-live2d-display';

window.PIXI = PIXI; // Global Pixi

let app;
let model;
let originalWidth;
let originalHeight;

export async function init(index, path) {
  console.log('live2d.js: Initializing Live2D model...');
  try {
    const canvas = document.getElementById('canvas_view');
    if (!canvas) {
      console.error('live2d.js: Canvas element not found!');
      return;
    }
    console.log('live2d.js: Canvas element found:', canvas);

    // Set an initial background image dynamically
    setBackground('./src/assets/backgrounds/Living_room.jpg');

    // Create PIXI application with improved resolution
    app = new PIXI.Application({
      view: canvas,
      transparent: true,
      autoDensity: true,
      resizeTo: window,
      resolution: window.devicePixelRatio || 1, // Use device pixel ratio for better rendering
    });
    console.log('live2d.js: PIXI application created.');

    // Load the initial Live2D model
    await loadModel(path);

    // Handle window resize events
    window.addEventListener('resize', () => {
      console.log('live2d.js: Window resized, adjusting model...');
      app.renderer.resize(window.innerWidth, window.innerHeight); // Resize PIXI renderer
      fitModelToCanvas(); // Adjust model size and position
    });

    console.log('live2d.js: Live2D model added to the stage.');
  } catch (error) {
    console.error('live2d.js: Failed to initialize Live2D model:', error);
  }
}

async function loadModel(modelPath) {
  try {
    console.log(`live2d.js: Loading model from ${modelPath}`);
    if (model) {
      app.stage.removeChild(model); // Remove the previous model from the stage
      model.destroy(); // Clean up the previous model
    }

    // Load the new model
    model = await Live2DModel.from(modelPath, {
      motionPreload: MotionPreloadStrategy.NONE,
    });

    // Add the model to the PIXI stage
    app.stage.addChild(model);

    // Store the original dimensions of the model
    originalWidth = model.width;
    originalHeight = model.height;

    fitModelToCanvas(); // Set initial scale and position

    console.log('live2d.js: Model loaded and added to stage.');
  } catch (error) {
    console.error('live2d.js: Failed to load model:', error);
  }
}

function fitModelToCanvas() {
  if (!model) return;
  
  // 根據drawer調整大小
  const drawer = document.getElementById('drawer');
  const drawerWidth = drawer ? drawer.offsetWidth : 0;
  const availableWidth = window.innerWidth - drawerWidth;
  const availableHeight = window.innerHeight;

  const scaleX = availableWidth / originalWidth;
  const scaleY = availableHeight / originalHeight;
  const scale = Math.min(scaleX, scaleY) * 0.75; 

  model.scale.set(scale);
  model.position.set(
    (availableWidth - originalWidth * scale) / 2 + drawerWidth, 
    (availableHeight - originalHeight * scale) / 2 
  );
}

export function switchModel(modelPath) {
  loadModel(modelPath);
}

// Existing setBackground function remains the same
export function setBackground(imagePath) {
  const container = document.getElementById('canvas_view')?.parentElement;
  if (container) {
    container.style.backgroundImage = `url('${imagePath}')`;
    container.style.backgroundRepeat = 'no-repeat';
    container.style.backgroundPosition = 'center';
    container.style.backgroundSize = 'cover';
    console.log(`live2d.js: Background switched to ${imagePath}`);
  }
}
