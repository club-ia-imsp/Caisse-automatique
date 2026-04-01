import React from 'react';

const InvoicePreview = ({ invoice }) => {
  if (!invoice) return null;

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 max-w-sm mx-auto font-mono text-sm animate-fade-in">
      {/* Header */}
      <div className="text-center border-b-2 border-dashed border-gray-300 pb-4 mb-4">
        <h2 className="text-xl font-bold text-primary">automaticCHECK</h2>
        <p className="text-xs text-gray-500 mt-1">Caisse Automatique Intelligente</p>
        <p className="text-xs text-gray-400 mt-2">
          {new Date(invoice.transaction_date).toLocaleString('fr-FR')}
        </p>
        <p className="text-xs text-gray-400">
          Facture: {String(invoice.id).slice(0, 8).toUpperCase()}
        </p>
      </div>

      {/* Items */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between text-xs text-gray-500 font-bold pb-1 border-b border-gray-200">
          <span className="w-1/2">Article</span>
          <span className="w-1/6 text-center">Qté</span>
          <span className="w-1/6 text-right">P.U</span>
          <span className="w-1/6 text-right">Total</span>
        </div>
        {invoice.items?.map((item, idx) => (
          <div key={idx} className="flex justify-between text-xs">
            <span className="w-1/2 truncate">{item.product_name}</span>
            <span className="w-1/6 text-center">×{item.quantity}</span>
            <span className="w-1/6 text-right">{item.unit_price.toFixed(0)}</span>
            <span className="w-1/6 text-right font-medium">{item.total.toFixed(0)}</span>
          </div>
        ))}
      </div>

      {/* Totals */}
      <div className="border-t-2 border-dashed border-gray-300 pt-3 space-y-1">
        <div className="flex justify-between text-xs text-gray-600">
          <span>Sous-total</span>
          <span>{invoice.subtotal.toFixed(0)} FCFA</span>
        </div>
        <div className="flex justify-between text-xs text-gray-600">
          <span>TVA (18%)</span>
          <span>{invoice.tax_amount.toFixed(0)} FCFA</span>
        </div>
        <div className="flex justify-between text-base font-bold text-primary pt-2 border-t border-gray-200">
          <span>TOTAL</span>
          <span>{invoice.total_amount.toFixed(0)} FCFA</span>
        </div>
      </div>

      {/* Footer */}
      <div className="text-center mt-4 pt-3 border-t-2 border-dashed border-gray-300">
        <p className="text-xs text-gray-400">
          Paiement: {invoice.payment_method || 'Non spécifié'}
        </p>
        <p className={`text-xs font-medium mt-1 ${
          invoice.payment_status === 'paye' ? 'text-primary' : 'text-amber-600'
        }`}>
          Statut: {invoice.payment_status === 'paye' ? (
            <><i className="fa-solid fa-check-circle mr-1"></i>Payé</>
          ) : (
            <><i className="fa-solid fa-clock mr-1"></i>En attente</>
          )}
        </p>
        <p className="text-xs text-gray-400 mt-3 italic">Merci de votre visite!</p>
      </div>
    </div>
  );
};

export default InvoicePreview;
