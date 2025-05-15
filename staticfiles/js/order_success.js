// Limpia el localStorage y actualiza el badge
localStorage.removeItem('cart');
document.addEventListener('DOMContentLoaded', () => {
  const badge = document.querySelector('#cart-badge');
  if (badge) {
    badge.textContent = '0';
  }
});