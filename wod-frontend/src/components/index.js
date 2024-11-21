import * as PIXI from 'pixi.js';
import {
  Live2DModel,
  MotionPreloadStrategy,
} from 'pixi-live2d-display';

// Attach PIXI to global
window.PIXI = PIXI;

export async function init() {
  console.log('index.js: Initializing Live2D model...');
  try {
    // Verify the canvas element
    const canvas = document.getElementById('canvas_view');
    if (!canvas) {
      console.error('index.js: Canvas element not found!');
      return;
    }
    console.log('index.js: Canvas element found:', canvas);

    // Create PIXI application with improved resolution
    const app = new PIXI.Application({
      view: canvas,
      transparent: true,
      autoDensity: true,
      resizeTo: window,
      resolution: window.devicePixelRatio || 1, // Use device pixel ratio for better rendering
    });
    console.log('index.js: PIXI application created.');

    // Load the Live2D model
    const model = await Live2DModel.from('../../src/assets/miku_model/runtime/miku_sample_t04.model3.json', {
      motionPreload: MotionPreloadStrategy.NONE,
    });
    console.log('index.js: Live2D model loaded successfully!');

    // Add the model to the PIXI stage
    app.stage.addChild(model);

    // Store the original dimensions of the model
    const originalWidth = model.width;
    const originalHeight = model.height;

    // Dynamic scaling and centering logic
    const fitModelToCanvas = () => {
      const scaleX = window.innerWidth / originalWidth;
      const scaleY = window.innerHeight / originalHeight;
      const scale = Math.min(scaleX, scaleY) * 0.75; // Leave some padding

      model.scale.set(scale); // Apply scale
      model.position.set(
        (window.innerWidth - originalWidth * scale) / 2, // Center horizontally
        (window.innerHeight - originalHeight * scale) / 2 // Center vertically
      );
    };

    fitModelToCanvas(); // Set initial scale and position

    // Handle window resize events
    window.addEventListener('resize', () => {
      console.log('index.js: Window resized, adjusting model...');
      app.renderer.resize(window.innerWidth, window.innerHeight); // Resize PIXI renderer
      fitModelToCanvas(); // Adjust model size and position
    });

    console.log('index.js: Live2D model added to the stage.');

  } catch (error) {
    console.error('index.js: Failed to initialize Live2D model:', error);
  }
}
