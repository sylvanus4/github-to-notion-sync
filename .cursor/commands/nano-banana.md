## Nano Banana — Direct Google GenAI Image Generation + Prompt Library

Generate or edit images using Google's `gemini-3.1-flash-image-preview` model directly via the GenAI API. Includes a 7,600+ prompt library with search, browse, and one-click generation. No gateway dependency.

### Usage

```
# Text-to-Image
/nano-banana "A serene mountain lake at sunrise, photorealistic" --resolution 2K

# Image Editing
/nano-banana "Add a rainbow across the sky" --input-image "original.png"

# With output directory
/nano-banana "Corporate logo, minimalist" --output-dir outputs/images/

# Custom filename
/nano-banana "Pixel art cat" --filename "pixel_cat.png"

# Generate from a library prompt by ID
/nano-banana --id 12445 --resolution 2K --output-dir outputs/images/
```

> **Tip:** Use `/nano-banana-browse` to search and discover prompts from the 7,600+ library, then generate with `--id`.

### Workflow

1. **Parse** — Extract prompt (or `--id` for library prompt), optional input image, resolution, output directory from user request
2. **Build command** — Construct `uv run generate_image.py` or `uv run prompt_library.py generate` command with appropriate flags
3. **Execute** — Run the script via Shell
4. **Report** — Show saved file path and any model text response

### Output

PNG image saved to the specified path (defaults to current directory).

### Execution

Read and follow the `nano-banana` skill (`.cursor/skills/standalone/nano-banana/SKILL.md`).
