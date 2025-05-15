document.addEventListener('DOMContentLoaded', () => {
  // 1) Cargar carrito
  let cart = JSON.parse(localStorage.getItem('cart')) || {};

  // 2) Actualiza badge
  function updateCartBadge() {
    const totalCount = Object.values(cart).reduce((sum, item) => sum + item.qty, 0);
    document.querySelector('#cart-badge').textContent = totalCount;
  }

  // 3) Guardar y refrescar badge
  function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
  }

  // 4) Añadir producto
  document.querySelectorAll('.add-to-cart').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      const name = btn.dataset.name;
      const price = parseFloat(btn.dataset.price);
      if (cart[id]) {
        cart[id].qty++;
      } else {
        cart[id] = { name, price, qty: 1 };
      }
      saveCart();
      fetch(`/cart/add/${id}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
      });
    });
  });

  // 5) Si estamos en /cart/, renderizar tabla
  const tbody = document.querySelector('#cart-table-body');
  if (tbody) {
    function renderCartTable() {
      tbody.innerHTML = '';
      let total = 0;
      for (const [id, item] of Object.entries(cart)) {
        const lineTotal = item.price * item.qty;
        total += lineTotal;
        tbody.innerHTML += `
          <tr>
            <td>${item.name}</td>
            <td>${item.qty}</td>
            <td>$${item.price.toFixed(2)}</td>
            <td>$${lineTotal.toFixed(2)}</td>
            <td>
              <button class="btn btn-sm btn-danger remove-from-cart" data-id="${id}">Eliminar</button>
            </td>
          </tr>`;
      }
      document.querySelector('#cart-total').textContent = `$${total.toFixed(2)}`;
      attachRemoveListeners();
    }

    function attachRemoveListeners() {
      document.querySelectorAll('.remove-from-cart').forEach(btn => {
        btn.addEventListener('click', () => {
          const id = btn.dataset.id;
          delete cart[id];
          saveCart();
          fetch(`/cart/remove/${id}/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
          });
          renderCartTable();
        });
      });
    }

    document.querySelector('#clear-cart').addEventListener('click', () => {
      cart = {};
      saveCart();
      fetch('/cart/clear/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
      });
      renderCartTable();
    });

    renderCartTable();
  }

  // 6) Badge inicial
  updateCartBadge();
});
