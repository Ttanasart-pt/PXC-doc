# Pixel Composer Documentations

A documentation page for [Pixel Composer](https://github.com/Ttanasart-pt/Pixel-Composer).

Github page: https://docs.pixel-composer.com

## Generating pages

Call `gen/main.py` to generate all pages.

### Node data

Static content should be added to `content/_nodes` which will be inserted to `content/3_nodes` automatically.

Make sure to set `scriptDir` to point to the script directory.

### Other data

All files in `content/` except `content/3_nodes` are editable static content.

- PascalCase will be converted to  Title Case. 
- Page can begins with number to force ordering. Number needs to ends with underscore `_` before the actual name.

`styles.css` will be copy to `docs/styles.css` automatically. `src` directory is hardlinked to the `docs/src`.

## Media

All media are stored in `src`. Every image should use different name (even in different directory.) to allow tag shortcuts.

## Tag shortcuts

There are multiple tag shortcuts that can be use to simplify writing. There tag will be replaced when call `gen/main.py`.

`<img [image name]>`

Add image with default style (image name without extension).

`<img-deco [image name]>`

Add image with corner + frame decoration.

`<node [node name]>`

Add link to specific node page.

`<junc [junction]>`

(Only works in `content/__nodes`) Add decorated junction with type data.

`<attr [attribute name]>`

(Only works in `content/__nodes`) Add decorated attrubute.