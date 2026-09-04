// ===== Vues =====
const cartView = document.getElementById('cartView');
const paymentView = document.getElementById('paymentView');

// ===== Vue panier =====
const cartBadge = document.getElementById('cartBadge');
const cartTitle = document.getElementById('cartTitle');
const totalPill = document.getElementById('totalPill');
const itemsList = document.getElementById('itemsList');
const emptyState = document.getElementById('emptyState');
const recapCard = document.getElementById('recapCard');
const subtotalValue = document.getElementById('subtotalValue');
const feeValue = document.getElementById('feeValue');
const promoValue = document.getElementById('promoValue');
const grandTotal = document.getElementById('grandTotal');
const payButton = document.getElementById('payButton');
const resetButton = document.getElementById('resetButton');
const simulateButton = document.getElementById('simulateButton');
const scanToast = document.getElementById('scanToast');

// ===== Vue paiement =====
const backButton = document.getElementById('backButton');
const paymentArticleCount = document.getElementById('paymentArticleCount');
const paymentAmount = document.getElementById('paymentAmount');
const paymentSubtotal = document.getElementById('paymentSubtotal');
const paymentFees = document.getElementById('paymentFees');
const confirmAmount = document.getElementById('confirmAmount');
const confirmPaymentButton = document.getElementById('confirmPaymentButton');
const methodCards = document.querySelectorAll('.method-card');

// ===== Confirmation de paiement =====
const paymentConfirmation = document.getElementById('paymentConfirmation');
const confirmationMeta = document.getElementById('confirmationMeta');
let confirmationTimer = null;

const ICON_CHECK_CIRCLE = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>';
const ICON_ALERT_TRIANGLE = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>';

const PAYMENT_METHOD_LABELS = {
  mobile_money: 'Mobile Money',
  card: 'Carte bancaire',
  cash: 'Espèces',
};

let cart = [];
let total = 0;
let selectedMethod = 'mobile_money';
let lastScanTimestamp = null;

function showView(view) {
  [cartView, paymentView].forEach((v) => v.classList.add('view-hidden'));
  view.classList.remove('view-hidden');
}

function formatDate(date) {
  return new Intl.DateTimeFormat('fr-FR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

function makeReceiptNumber(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  const h = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  const s = String(date.getSeconds()).padStart(2, '0');
  return `REC-${y}${m}${d}-${h}${min}${s}`;
}

function groupItems(items) {
  const groups = {};
  items.forEach((item) => {
    // Deux exemplaires différents (UID distincts) du même produit — même nom
    // et même prix — sont affichés comme un seul article groupé (ex: "Livre x2").
    const key = `${item.nom}__${item.prix}`;
    if (!groups[key]) {
      groups[key] = { uid: item.uid, nom: item.nom, prix: item.prix, quantite: 0 };
    }
    groups[key].quantite += 1;
  });
  return Object.values(groups);
}

function computeTotals() {
  const subtotal = total;
  const fees = Math.round(subtotal * 0.02);
  const promo = 0;
  return { subtotal, fees, promo, finalTotal: subtotal + fees - promo };
}

// ===== Notifications de scan =====

function showScanToast(lastScan) {
  if (!lastScan || !lastScan.timestamp || lastScan.timestamp === lastScanTimestamp) {
    return;
  }
  lastScanTimestamp = lastScan.timestamp;

  const card = document.createElement('div');
  card.className = `toast-card ${lastScan.found ? 'toast-ok' : 'toast-error'}`;
  const message = lastScan.action === 'retire'
    ? `${lastScan.nom} retiré du panier`
    : `${lastScan.nom} ajouté au panier`;
  card.innerHTML = lastScan.found
    ? `<span class="toast-icon">${ICON_CHECK_CIRCLE}</span><span>${message}</span>`
    : `<span class="toast-icon">${ICON_ALERT_TRIANGLE}</span><span>Article non reconnu — UID ${lastScan.uid}</span>`;

  scanToast.appendChild(card);
  requestAnimationFrame(() => card.classList.add('toast-visible'));

  setTimeout(() => {
    card.classList.remove('toast-visible');
    setTimeout(() => card.remove(), 250);
  }, 3000);
}

// ===== Rendu du panier =====

function renderCart() {
  const grouped = groupItems(cart);
  const articleCount = grouped.reduce((sum, item) => sum + item.quantite, 0);

  cartBadge.textContent = String(articleCount);

  itemsList.innerHTML = '';

  if (cart.length === 0) {
    cartTitle.textContent = 'Aucun article';
    emptyState.style.display = 'block';
    itemsList.style.display = 'none';
    recapCard.style.display = 'none';
  } else {
    cartTitle.textContent = `${articleCount} article${articleCount > 1 ? 's' : ''} scanné${articleCount > 1 ? 's' : ''}`;
    emptyState.style.display = 'none';
    itemsList.style.display = 'block';
    recapCard.style.display = 'block';

    grouped.forEach((item) => {
      const li = document.createElement('li');
      const lineTotal = item.prix * item.quantite;
      li.innerHTML = `
        <div>
          <span class="item-label">${item.nom}</span>
          <span class="item-meta">× ${item.quantite}</span>
        </div>
        <span class="item-price">${lineTotal} FCFA</span>
      `;
      itemsList.appendChild(li);
    });
  }

  const { subtotal, fees, promo, finalTotal } = computeTotals();
  totalPill.textContent = `${total} FCFA`;
  subtotalValue.textContent = `${subtotal} FCFA`;
  feeValue.textContent = `${fees} FCFA`;
  promoValue.textContent = `- ${promo} FCFA`;
  grandTotal.textContent = `${finalTotal} FCFA`;

  payButton.disabled = cart.length === 0;
  resetButton.disabled = cart.length === 0;
}

async function refreshCart() {
  try {
    const response = await fetch(`/api/cart?t=${Date.now()}`, { cache: 'no-store' });
    const data = await response.json();
    cart = data.items || [];
    total = data.total || 0;
    renderCart();
    showScanToast(data.last_scan);
  } catch (error) {
    console.error('Impossible de récupérer le panier', error);
  }
}

async function simulateScan() {
  simulateButton.disabled = true;
  try {
    const response = await fetch('/api/simulate_scan', { method: 'POST' });
    await response.json();
    await refreshCart();
  } catch (error) {
    alert('Erreur de connexion au serveur. Vérifie que le backend tourne.');
    console.error(error);
  } finally {
    simulateButton.disabled = false;
  }
}

async function resetCart() {
  try {
    await fetch('/api/clear', { method: 'POST' });
    await refreshCart();
  } catch (error) {
    alert('Erreur de connexion au serveur. Vérifie que le backend tourne.');
    console.error(error);
  }
}

// ===== Vue paiement =====

function selectMethod(method) {
  selectedMethod = method;
  methodCards.forEach((card) => {
    card.classList.toggle('selected', card.dataset.method === method);
  });
}

function openPaymentView() {
  if (cart.length === 0) {
    return;
  }

  const grouped = groupItems(cart);
  const articleCount = grouped.reduce((sum, item) => sum + item.quantite, 0);
  const { subtotal, fees, finalTotal } = computeTotals();

  paymentArticleCount.textContent = `${articleCount} article${articleCount > 1 ? 's' : ''}`;
  paymentAmount.textContent = `${finalTotal} FCFA`;
  paymentSubtotal.textContent = `${subtotal} FCFA`;
  paymentFees.textContent = `${fees} FCFA`;
  confirmAmount.textContent = `${finalTotal} FCFA`;

  showView(paymentView);
}

function showPaymentConfirmation(amount, methodLabel) {
  if (confirmationTimer) {
    clearTimeout(confirmationTimer.fadeId);
    clearTimeout(confirmationTimer.hideId);
  }

  const now = new Date();
  confirmationMeta.textContent = `${amount} FCFA · Reçu ${makeReceiptNumber(now)} · ${methodLabel} · ${formatDate(now)}`;
  paymentConfirmation.classList.remove('view-hidden', 'fade-out');

  const fadeId = setTimeout(() => {
    paymentConfirmation.classList.add('fade-out');
  }, 4500);
  const hideId = setTimeout(() => {
    paymentConfirmation.classList.add('view-hidden');
    paymentConfirmation.classList.remove('fade-out');
  }, 4800);

  confirmationTimer = { fadeId, hideId };
}

async function confirmPayment() {
  confirmPaymentButton.disabled = true;
  try {
    const response = await fetch('/api/pay', { method: 'POST' });
    const data = await response.json();

    if (!response.ok) {
      alert(data.error || 'Erreur lors du paiement');
      return;
    }

    showView(cartView);
    showPaymentConfirmation(data.total, PAYMENT_METHOD_LABELS[selectedMethod]);
    await refreshCart();
  } catch (error) {
    alert('Erreur de connexion au serveur. Vérifie que le backend tourne.');
    console.error(error);
  } finally {
    confirmPaymentButton.disabled = false;
  }
}

// ===== Écouteurs =====

payButton.addEventListener('click', openPaymentView);
resetButton.addEventListener('click', resetCart);
simulateButton.addEventListener('click', simulateScan);
backButton.addEventListener('click', () => showView(cartView));
confirmPaymentButton.addEventListener('click', confirmPayment);
methodCards.forEach((card) => {
  card.addEventListener('click', () => selectMethod(card.dataset.method));
});

refreshCart();
setInterval(refreshCart, 1000);
