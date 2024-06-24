export function extractEmoji(headline) {
  const emojiRegex = /\p{Emoji}/u;
  const match = headline.match(emojiRegex);
  return match ? match[0] : "🗞️";
}

export function createEmojiMarker(emoji, isActive) {
  const canvas = document.createElement('canvas');
  const size = 16;
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  ctx.globalAlpha = isActive ? 1.0 : 0.4;
  ctx.font = `${size - 2}px Arial`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = '#1c1917';
  ctx.fillText(emoji, size / 2, size / 2);

  return canvas.toDataURL();
}