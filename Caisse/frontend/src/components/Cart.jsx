import React from 'react';

const Cart = ({ cart, onClearCart }) => {
  const cartItems = Object.values(cart);
  const subtotal = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const tax = subtotal * 0.18;
  const total = subtotal + tax;

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-base sm:text-lg font-bold text-gray-800">
          <i className="fa-solid fa-cart-shopping mr-2 text-primary"></i>Panier
          {cartItems.length > 0 && (
            <span className="ml-2 badge-success text-xs">
              {cartItems.reduce((sum, i) => sum + i.quantity, 0)} articles
            </span>
          )}
        </h3>
        {cartItems.length > 0 && (
          <button
            onClick={onClearCart}
            className="text-xs text-red-500 hover:text-red-700 font-medium"
          >
            Vider
          </button>
        )}
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 min-h-[200px]">
        {cartItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400">
            <svg className="w-12 h-12 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M3 3h2l.4 2M7 13h10l4-8H5.4m1.6 8L5 6H3m4 7v6a1 1 0 001 1h1a1 1 0 001-1v-6m5 0v6a1 1 0 001 1h1a1 1 0 001-1v-6" />
            </svg>
            <p className="text-sm">Aucun article détecté</p>
            <p className="text-xs mt-1">Placez des articles devant la caméra</p>
          </div>
        ) : (
          cartItems.map((item) => (
            <div
              key={item.product_id}
              className="flex items-center justify-between p-3 bg-surface-light rounded-xl border border-surface-border animate-fade-in"
            >
              <div className="flex-1">
                <p className="font-semibold text-gray-800 text-sm">{item.product_name}</p>
                <p className="text-xs text-gray-500">
                  {item.price.toFixed(0)} FCFA × {item.quantity}
                </p>
              </div>
              <div className="text-right">
                <p className="font-bold text-primary text-sm">
                  {(item.price * item.quantity).toFixed(0)} FCFA
                </p>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Totals */}
      {cartItems.length > 0 && (
        <div className="mt-4 pt-4 border-t-2 border-surface-border space-y-2">
          <div className="flex justify-between text-sm text-gray-600">
            <span>Sous-total</span>
            <span>{subtotal.toFixed(0)} FCFA</span>
          </div>
          <div className="flex justify-between text-sm text-gray-600">
            <span>TVA (18%)</span>
            <span>{tax.toFixed(0)} FCFA</span>
          </div>
          <div className="flex justify-between text-lg font-bold text-primary pt-2 border-t border-surface-border">
            <span>Total</span>
            <span>{total.toFixed(0)} FCFA</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Cart;
