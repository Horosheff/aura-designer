# MCP Tools Used By Aura Designer

Aura Designer can run without MCP tools by using fallback assets, but its best workflow is inside Cursor with image and background-removal tools available.

## Expected Tools

### `gpt-image-2`

Used for:

- Hero images.
- Case-study images.
- Product objects.
- 3D or editorial visual assets.
- Style-specific visual motifs.

Rules:

- Generate assets from the current `AURADESIGN.md` style, not from generic prompts.
- Keep image prompts concrete: subject, composition, material, lighting, camera angle, color palette, background requirements.
- Review output before inserting it into the page.

### `recraft_remove_background`

Used for:

- Transparent hero PNGs.
- Floating product or object assets.
- Case-study cards where the object should sit on colored panels.

Rules:

- Remove background before placing hero objects on complex layouts.
- Do not place dark uncut images on dark sections.
- Prefer transparent PNG assets for neo-brutalist, glassmorphism, and editorial hero compositions.

## Cursor Subagent Behavior

Subagents inherit the parent agent's MCP tools. If a local environment has different MCP names, adapt the subagent prompt or parent instruction to the available tool names.

When calling MCP tools, first inspect the tool schema in the local Cursor MCP descriptors and then call the exact tool name with valid arguments.
