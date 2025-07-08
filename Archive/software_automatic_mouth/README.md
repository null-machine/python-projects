A customizable retro text-to-speech library using s-macke's C implementation of SAM
Version 1.0.0 doesn't support things like giving SAM an array of text and making SAM speak each one item by item yet however that feature is planned.
There's a lot planned for this library however i just want it to be out there for now.

If you're gonna be using this in it's current state please be sure to make your own wrapper function to call the speak function so you won't have to change every call to sam.speak in your code when the library changes to 2.x
