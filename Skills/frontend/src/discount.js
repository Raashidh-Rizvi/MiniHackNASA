export function discount(total, percent) {
  if (total < 0 || percent < 0 || percent > 100) throw new RangeError('Invalid discount');
  return Math.round(total * (1 - percent / 100) * 100) / 100;
}
