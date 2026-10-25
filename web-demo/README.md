# MoodFive browser demo

A small browser version of the Python/PySide6 desktop project. Pick a mood, discover five songs, switch the featured record, and stream up to 15 seconds of a song preview. Includes album art and links to the full songs in the iTunes store.

This web version was implemented with AI assistance. The original desktop app is in the parent directory.

The site is plain HTML, CSS and JavaScript in `dist/`. No install or build step is required. For local preview, run `python -m http.server 8080 --directory dist` here and open http://localhost:8080.

`dist/songs.js` is a snapshot of the desktop app's song catalogue. Music metadata and preview streams come from iTunes and need an internet connection. Some browsers require an explicit click on Play. Availability depends on the store; unavailable tracks show a retry message. Audio is streamed, not saved.
