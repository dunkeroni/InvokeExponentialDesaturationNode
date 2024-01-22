# InvokeExponentialDesaturationNode
A node that can desaturate an image based on a target color (specifically its Hue)

This node converts the image to HSV value, and then scales the saturation of all colors based on the input multiplier and an exponential distance calculation.  
**Color**: The input Hue to target. Use the Color Primitive node to select one.  
**Image**: The image to apply the changes to.  
**Saturation Multiplier**: How much to multiply the target color's saturation by. 
**Buffer**: How far from the target hue before the exponential distance calculation takes effect. Adding a small amount of buffer may help avoid fringing.
**Exponent**: How close to the target color pixels in the image need to be in order to be affected. Higher numbers will make the target color more precise.  
**Preserve Luminosity**: Since HSV Desaturation makes the affected parts of the image lighter, enable this to keep the greyscale brightness the same in the result.  
**Invert Result**: Preserve the target color and desaturate everything else.  

Usage Example:
![image](https://github.com/dunkeroni/InvokeExponentialDesaturationNode/assets/3298737/e9aaa1a4-3f68-4e6e-b37b-351b0b979588)


To keep only the target color and desaturate the rest, enable "Invert Result". Note: Your brain is a bit more sensitive to colors in a grayscale image, so you may need to play with the exponent and color inputs more to get a good result.
![image](https://github.com/dunkeroni/InvokeExponentialDesaturationNode/assets/3298737/001b3fdd-3878-4909-b277-6868b1788e35)



Use a Saturation Multiplier > 1 to increase the saturation of the target color instead.  
![image](https://github.com/dunkeroni/InvokeExponentialDesaturationNode/assets/3298737/6e53cfc3-de9b-4271-b644-1de72521caad)
