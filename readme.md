# Pixel Composer Documentations

A documentation page for [Pixel Composer](https://github.com/Ttanasart-pt/Pixel-Composer) made using custom static page generator.

Github page: https://docs.pixel-composer.com

## Generate static pages

Contents in `content/` will be formatted in to the `template.html` and send to `docs/` with the same subfolder structure using the provided `gen.py` file.

- PascalCase will be converted to space separated Title Case. 
- Page can begins with number to force ordering. Number needs to ends with underscore `_` before the actual name.

`styles.css` will be copy to `docs/styles.css` automatically. `src` directory is hardlinked to the `docs/src` (not sure how github deal with hardlink)