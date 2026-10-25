'use strict';
const $ = id => document.getElementById(id);
const audio = $('audio');
const cache = new Map();
let playlist = [], selected = -1, generation = 0, callbackNumber = 0;
const clean = text => text.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase().replace(/[^a-z0-9]/g, '');
const artistName = text => clean(text) === 'curtis50centjackson' ? '50cent' : clean(text);
function splitSong(song) { const i = song.indexOf(' - '); return { title: song.slice(0, i), artist: song.slice(i + 3) }; }
function chooseFive(songs) {
  const result = [...songs];
  for (let i = result.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [result[i], result[j]] = [result[j], result[i]]; }
  return result.slice(0, 5);
}
function requestMetadata(path, parameters) {
  return new Promise((resolve, reject) => {
    const callback = `moodfiveCallback${++callbackNumber}`;
    const script = document.createElement('script');
    const cleanup = () => { clearTimeout(timer); script.remove(); window[callback] = () => {}; setTimeout(() => delete window[callback], 60000); };
    const timer = setTimeout(() => { cleanup(); reject(new Error('The music search took too long. Try this track again.')); }, 14000);
    window[callback] = data => { cleanup(); resolve(data); };
    script.onerror = () => { cleanup(); reject(new Error('Could not reach the music search. Check your connection and try again.')); };
    script.src = `https://itunes.apple.com/${path}?${new URLSearchParams({...parameters, country: 'NL', callback})}`;
    document.head.append(script);
  });
}
async function lookup(song) {
  if (cache.has(song)) return cache.get(song);
  const {title, artist} = splitSong(song);
  const data = song === 'Tired - beabadoobee'
    ? await requestMetadata('lookup', {id: '1444723452'})
    : await requestMetadata('search', {term: `${title} ${artist}`, entity: 'song', limit: '25', explicit: 'Yes'});
  const matches = (data.results || []).filter(track => clean(track.trackName || '') === clean(title) && artistName(track.artistName || '') === artistName(artist));
  const track = matches.find(item => item.previewUrl) || matches[0];
  if (!track) throw new Error('No exact match this time. Try another track or tap Retry.');
  cache.set(song, track);
  return track;
}
function stopAudio() { audio.pause(); audio.removeAttribute('src'); audio.load(); $('record').classList.remove('playing'); $('progress').value = 0; $('time').textContent = '0:00 / 0:15'; }
function renderQueue() {
  $('queue').replaceChildren();
  playlist.forEach((song, index) => {
    if (index === selected) return;
    const button = document.createElement('button'); button.type = 'button'; button.className = 'song';
    button.textContent = song;
    button.addEventListener('click', () => selectSong(index)); $('queue').append(button);
  });
}
async function selectSong(index) {
  const token = ++generation; selected = index; stopAudio(); renderQueue();
  const song = playlist[index], {title, artist} = splitSong(song);
  $('track-title').textContent = title; $('track-artist').textContent = artist;
  $('cover').hidden = true; $('cover').removeAttribute('src'); $('record-placeholder').hidden = false;
  $('store-link').hidden = true; $('store-link').removeAttribute('href');
  $('play').disabled = true; $('play').textContent = 'Loading…'; $('play').dataset.action = 'play';
  $('status').textContent = 'Finding your track…';
  try {
    const track = await lookup(song);
    if (token !== generation) return;
    if (track.artworkUrl100) {
      $('cover').onload = () => { if (token === generation) { $('cover').hidden = false; $('record-placeholder').hidden = true; } };
      $('cover').onerror = () => { if (token === generation) { $('cover').hidden = true; $('record-placeholder').hidden = false; } };
      $('cover').alt = `${track.collectionName || title} album cover`; $('cover').src = track.artworkUrl100;
    }
    if (track.trackViewUrl && new URL(track.trackViewUrl).protocol === 'https:') { $('store-link').href = track.trackViewUrl; $('store-link').hidden = false; }
    if (!track.previewUrl) { $('status').textContent = 'No preview for this track. You can find the full song in the store.'; $('play').textContent = 'Preview unavailable'; return; }
    audio.src = track.previewUrl; $('play').disabled = false; $('play').textContent = 'Play 15s preview';
    $('status').textContent = track.collectionName || 'Your next obsession?';
    await playPreview(token);
  } catch (error) {
    if (token !== generation) return;
    $('status').textContent = error.message; $('play').textContent = 'Retry'; $('play').dataset.action = 'retry'; $('play').disabled = false;
  }
}
async function playPreview(token = generation) {
  if (audio.currentTime >= 15 || audio.ended) audio.currentTime = 0;
  try { await audio.play(); }
  catch (error) { if (token !== generation) return; $('record').classList.remove('playing'); $('play').textContent = 'Play 15s preview'; $('status').textContent = error.name === 'NotAllowedError' ? 'Tap Play to start your preview.' : 'This preview could not play. Try again or choose another track.'; }
}
Object.keys(SONGS).forEach(mood => { const option = document.createElement('option'); option.value = mood; option.textContent = mood; $('mood').append(option); });
$('mood-form').addEventListener('submit', event => { event.preventDefault(); playlist = chooseFive(SONGS[$('mood').value]); $('results').hidden = false; selectSong(0); });
$('play').addEventListener('click', () => { if ($('play').dataset.action === 'retry') { selectSong(selected); return; } if (audio.paused) playPreview(); else audio.pause(); });
audio.addEventListener('playing', () => { $('record').classList.add('playing'); $('play').textContent = 'Pause preview'; });
audio.addEventListener('waiting', () => $('record').classList.remove('playing'));
audio.addEventListener('pause', () => { $('record').classList.remove('playing'); if (!$('play').disabled) $('play').textContent = audio.currentTime >= 15 ? 'Replay 15s' : 'Play 15s preview'; });
audio.addEventListener('timeupdate', () => { const time = Math.min(audio.currentTime, 15); $('progress').value = time; $('time').textContent = `0:${String(Math.floor(time)).padStart(2, '0')} / 0:15`; if (audio.currentTime >= 15) audio.pause(); });
audio.addEventListener('ended', () => { $('record').classList.remove('playing'); $('play').textContent = 'Replay 15s'; });
audio.addEventListener('error', () => { if (!audio.getAttribute('src')) return; $('record').classList.remove('playing'); $('status').textContent = 'This preview could not load. Try another track or retry.'; $('play').disabled = false; $('play').textContent = 'Retry'; $('play').dataset.action = 'retry'; });
