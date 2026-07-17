# Akka SDK Fundamentals

Developer training deck. Introduces the Akka SDK to developers new to Akka, alongside a sample project hosted in a separate GitHub repository.

## Build

```bash
python3 training/akka-sdk-fundamentals/builder/build.py
```

Output: `generated/overview/index.html`.

## Sample project

The companion sample project lives in a separate GitHub repository (URL to be added). Slides link out to that repo for hands-on exercises.

## Adding a slide

1. Create `slides/NN-<name>/` with `slide.html`, `slide.css`, `slide.js`, `meta.json`.
2. Add the folder to `builder/slide-registry.json` (unregistered folders don't build).
3. Rebuild and, if committing to `main`, re-run `python3 build-index.py` from the repo root.
