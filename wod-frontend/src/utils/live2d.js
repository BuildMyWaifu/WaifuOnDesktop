import * as PIXI from 'pixi.js';
import {
  Live2DModel,
  MotionPreloadStrategy,
} from 'pixi-live2d-display';

window.PIXI = PIXI; // Global Pixi

// let app;
let model;
let originalWidth;
let originalHeight;

export async function init(elementId) {
  console.log('live2d.js: Initializing Live2D model...');
  try {
    const canvas = document.getElementById(elementId);
    const container = canvas.parentElement;
    if (!canvas) {
      console.error('live2d.js: Canvas element not found!');
      return;
    }
    console.log('live2d.js: Canvas element found:', canvas);

    // Set an initial background image dynamically
    setBackground(canvas, './src/assets/backgrounds/Living_room.jpg');

    // Create PIXI application with improved resolution
    let app = new PIXI.Application({
      view: canvas,
      transparent: true,
      autoDensity: true,
      resizeTo: container,
      resolution: window.devicePixelRatio || 1, // Use device pixel ratio for better rendering
    });
    console.log('live2d.js: PIXI application created.');

    // Load the initial Live2D model

    const modelPath = '../../src/assets/miku_model/runtime/miku_sample_t04.model3.json'
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

    fitModelToCanvas(canvas); // Set initial scale and position

    console.log('live2d.js: Model loaded and added to stage.');
  } catch (error) {
    console.error('live2d.js: Failed to load model:', error);
  }

    // Handle window resize events
    window.addEventListener('resize', () => {
      console.log('live2d.js: Window resized, adjusting model...');
      app.renderer.resize(container.clientWidth, container.clientHeight); // Resize PIXI renderer
      fitModelToCanvas(canvas); // Adjust model size and position
    });

    console.log('live2d.js: Live2D model added to the stage.');
  } catch (error) {
    console.error('live2d.js: Failed to initialize Live2D model:', error);
  }
}

function fitModelToCanvas(canvas) {
  if (!model) return;
  
  // 根據drawer調整大小
  const container = canvas.parentElement;
  const availableWidth = container.clientWidth;
  const availableHeight = container.clientHeight;

  const scaleX = availableWidth / originalWidth;
  const scaleY = availableHeight / originalHeight;
  const scale = Math.min(scaleX, scaleY) ; 

  model.scale.set(scale);
  model.position.set(
    (availableWidth - originalWidth * scale) / 2 , 
    (availableHeight - originalHeight * scale) / 2 
  );
}


// Existing setBackground function remains the same
export function setBackground(canvas, imagePath) {
  const container = canvas.parentElement;
  if (container) {
    container.style.backgroundImage = `url('${imagePath}')`;
    container.style.backgroundRepeat = 'no-repeat';
    container.style.backgroundPosition = 'center';
    container.style.backgroundSize = 'cover';
    console.log(`live2d.js: Background switched to ${imagePath}`);
  }
}
