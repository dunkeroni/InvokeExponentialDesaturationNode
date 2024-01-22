# InvokeExponentialDesaturationNode
A node that can desaturate an image based on a target color (specifically its Hue)

This node converts the image to HSV value, and then scales the saturation of all colors based on the input multiplier and an exponential distance calculation.  
**Color**: The input Color to target. Use the Color Primitive node to select one.  
**Image**: The image to apply the changes to.  
**Target Saturation**: How much to multiply the target color's saturation by. 
**Buffer**: How far from the target hue before the exponential distance calculation takes effect. You can apply a form of clamping by adding a buffer to control distance and using a high exponent so that the effect falls off immediately.
**Exponent**: How close to the target color pixels in the image need to be in order to be affected. Higher numbers will make the target color more precise.  
**Preserve Luminosity**: Since HSV Desaturation makes the affected parts of the image lighter, enable this to keep the greyscale brightness the same in the result.  
**Invert Result**: Preserve the target color and desaturate everything else.  

Usage Example:
![image](https://github.com/dunkeroni/InvokeExponentialDesaturationNode/assets/3298737/2349804d-5ea7-4d3e-b010-8d31875a11f3)


To keep only the target color and desaturate the rest, enable "Invert Result". Note: Your brain is a bit more sensitive to colors in a grayscale image, so you may need to play with the exponent and color inputs more to get a good result.
![image](https://github.com/dunkeroni/InvokeExponentialDesaturationNode/assets/3298737/7f959ada-befc-424e-9bbc-4b9dbf7e6872)
