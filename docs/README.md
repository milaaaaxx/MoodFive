# MoodFive web demo

This browser port recreates the layout of the original Python/PySide6 desktop app. The web port was created with AI assistance. The desktop source remains in the repository root.

GitHub Pages setup: Settings → Pages → Deploy from a branch → `main` → `/docs` → Save.

The static files need no build step. To preview locally, run `python -m http.server 8080 --directory docs` from the repository root, then open http://localhost:8080.

Select a mood and press Soundtracks for five songs. Click another song to feature it. Previews stop after 15 seconds; if the browser blocks autoplay, use Play. Album artwork and previews require an internet connection and depend on iTunes availability. The store badge links to the selected song. Audio is streamed, not downloaded.
