import * as PIXI from 'pixi.js';
import {
  Live2DModel,
  MotionPreloadStrategy,
} from 'pixi-live2d-display';

declare global {
  interface Window {
    PIXI: typeof PIXI;
  }
}
window.PIXI = PIXI; // Global Pixi

let app = undefined as PIXI.Application | undefined;
let model = undefined as Live2DModel | undefined;
let originalWidth = 0;
let originalHeight = 0;
window.addEventListener('resize', () => {
  console.log('live2d.js: Window resized, adjusting model...');
  if (!model) return;
  if (!app) return;
  const canvas = app.view as HTMLCanvasElement;
  const container = canvas.parentElement as HTMLElement;
  app.renderer.resize(container.clientWidth, container.clientHeight); // Resize PIXI renderer
  fitModelToCanvas(model, canvas, originalWidth, originalHeight); // Adjust model size and position
});

export async function init(elementId: string, fromUrl: string | undefined) {
  console.log('live2d.js: Initializing Live2D model...');
  try {
    const canvas = document.getElementById(elementId) as HTMLCanvasElement;
    const container = canvas.parentElement as HTMLElement;
    if (!canvas) {
      console.error('live2d.js: Canvas element not found!');
      return;
    }
    console.log('live2d.js: Canvas element found:', canvas);

    // Set an initial background image dynamically
    setBackground(canvas, '../../src/assets/backgrounds/Living_room.jpg');

    // Create PIXI application with improved resolution
    if (app) {
      app.destroy(); // Clean up the previous PIXI application
    }
    app = new PIXI.Application({
      view: canvas,
      transparent: true,
      autoDensity: true,
      resizeTo: container,
      resolution: window.devicePixelRatio || 1, // Use device pixel ratio for better rendering
    });
    console.log('live2d.js: PIXI application created.');

    // Load the initial Live2D model
    // let modelSource = '../../src/assets/mao_model/runtime/mao_pro.model3.json' as string | File;
    let modelSource = '../../src/assets/mao_test/mao_pro_test.model3.json' as string | File;
    // let modelSource = '../../src/assets/miku_model/runtime/miku_sample_t04.model3.json' as string | File;
    if (fromUrl != undefined) {
      console.log(fromUrl)
      modelSource = fromUrl
    }
    console.log(`live2d.js: Loading model from ${modelSource}`);
    try {
      if (model) {
        app.stage.removeChild(model); // Remove the previous model from the stage
        model.destroy(); // Clean up the previous model
      }
      model = await Live2DModel.from(modelSource, {
        motionPreload: MotionPreloadStrategy.NONE,
      });

      // Add the model to the PIXI stage
      app.stage.addChild(model);

      // Store the original dimensions of the model


      console.log('live2d.js: Model loaded and added to stage.');
    } catch (error) {
      console.error('live2d.js: Failed to load model:', error);
    }
    
    if (!model) {
      alert("Live2d模型載入失敗")
      return
    }
    // let then = performance.now();
    // function tick(now: number) {
    //   if (!model) return;
    //   model.update(now - then);
    //   then = now;
    //   requestAnimationFrame(tick);
    // }

    // requestAnimationFrame(tick);
    originalWidth = model.width;
    originalHeight = model.height;

    fitModelToCanvas(model, canvas, originalWidth, originalHeight); // Set initial scale and position

    // Handle window resize events
    

    console.log('live2d.js: Live2D model added to the stage.');
  } catch (error) {
    console.error('live2d.js: Failed to initialize Live2D model:', error);
  }
}

function fitModelToCanvas(model: Live2DModel, canvas: HTMLCanvasElement, originalWidth: number, originalHeight: number) {
  if (!model) return;
  const container = canvas.parentElement;
  if (!container) return;
  const availableWidth = container.clientWidth;
  const availableHeight = container.clientHeight;

  const scaleX = availableWidth / originalWidth;
  const scaleY = availableHeight / originalHeight;
  const scale = Math.min(scaleX, scaleY);

  model.scale.set(scale);
  model.position.set(
    (availableWidth - originalWidth * scale) / 2,
    (availableHeight - originalHeight * scale) / 2
  );
  console.log('live2d.js: Model adjusted to fit the canvas.');
}


// Existing setBackground function remains the same
export function setBackground(canvas: HTMLCanvasElement, imagePath: string) {
  const container = canvas.parentElement;
  if (container) {
    container.style.backgroundImage = `url('${imagePath}')`;
    container.style.backgroundRepeat = 'no-repeat';
    container.style.backgroundPosition = 'center';
    container.style.backgroundSize = 'cover';
    // container.style.zIndex = '1';
    console.log(`live2d.js: Background switched to ${imagePath}`);
  }
}
