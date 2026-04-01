import React, { useState, useCallback } from 'react';
import CameraFeed from '../components/CameraFeed';
import Cart from '../components/Cart';
import InvoicePreview from '../components/InvoicePreview';
import { createInvoice, updatePayment, getInvoicePdf } from '../services/api';
import toast from 'react-hot-toast';

const Checkout = () => {
  const [cart, setCart] = useState({});
  const [detections, setDetections] = useState([]);
  const [isActive, setIsActive] = useState(false);
  const [invoice, setInvoice] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState('especes');

  const handleDetections = useCallback((newDetections) => {
    setDetections(newDetections);
  }, []);

  const handleCartUpdate = useCallback((newCart) => {
    setCart(newCart);
  }, []);

  const handleClearCart = () => {
    setCart({});
    setDetections([]);
    setInvoice(null);
  };

  const handleGenerateInvoice = async () => {
    const cartItems = Object.values(cart);
    if (cartItems.length === 0) {
      toast.error('Le panier est vide!');
      return;
    }

    setGenerating(true);
    try {
      const invoiceData = {
        items: cartItems.map((item) => ({
          product_id: item.product_id,
          quantity: item.quantity,
          unit_price: item.price,
        })),
        payment_method: paymentMethod,
      };

      const res = await createInvoice(invoiceData);
      setInvoice(res.data);
      toast.success('Facture générée avec succès!');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Erreur de génération';
      toast.error(msg);
    } finally {
      setGenerating(false);
    }
  };

  const handlePayment = async () => {
    if (!invoice) return;
    
    try {
      await updatePayment(invoice.id, {
        payment_status: 'paye',
        payment_method: paymentMethod,
      });
      setInvoice({ ...invoice, payment_status: 'paye' });
      toast.success('Paiement confirmé!');
    } catch (err) {
      toast.error('Erreur lors du paiement');
    }
  };

  const handleDownloadPdf = () => {
    if (!invoice) return;
    window.open(getInvoicePdf(invoice.id), '_blank');
  };

  return (
    <div className="min-h-screen bg-surface-light p-3 sm:p-4 lg:p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-4 sm:mb-6 gap-3">
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
              <i className="fa-solid fa-cash-register mr-2 text-primary"></i>Mode Caisse
            </h1>
            <p className="text-xs sm:text-sm text-gray-500">Détection en temps réel des produits</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">Paiement:</span>
            <select
              value={paymentMethod}
              onChange={(e) => setPaymentMethod(e.target.value)}
              className="input-field !w-auto !py-2 text-sm"
            >
              <option value="especes"><i className="fa-solid fa-money-bill"></i> Espèces</option>
              <option value="carte"><i className="fa-solid fa-credit-card"></i> Carte</option>
            </select>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6">
          {/* Camera Feed */}
          <div className="lg:col-span-6">
            <div className="card h-full">
              <h2 className="text-base sm:text-lg font-bold text-gray-800 mb-3">
                <i className="fa-solid fa-video mr-2 text-primary"></i>Détection en Direct
              </h2>
              <CameraFeed
                onDetections={handleDetections}
                onCartUpdate={handleCartUpdate}
                isActive={isActive}
                setIsActive={setIsActive}
              />
            </div>
          </div>

          {/* Cart */}
          <div className="lg:col-span-3">
            <div className="card h-full">
              <Cart cart={cart} onClearCart={handleClearCart} />

              {/* Action buttons */}
              <div className="mt-4 space-y-2">
                <button
                  onClick={handleGenerateInvoice}
                  disabled={Object.keys(cart).length === 0 || generating}
                  className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {generating ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                      Génération...
                    </span>
                  ) : (
                    <><i className="fa-solid fa-file-invoice mr-2"></i>Générer Facture</>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Invoice Preview */}
          <div className="lg:col-span-3">
            <div className="card h-full">
              <h2 className="text-base sm:text-lg font-bold text-gray-800 mb-3">
                <i className="fa-solid fa-file-lines mr-2 text-primary"></i>Facture
              </h2>
              
              {invoice ? (
                <div>
                  <InvoicePreview invoice={invoice} />
                  <div className="mt-4 space-y-2">
                    {invoice.payment_status !== 'paye' && (
                      <button onClick={handlePayment} className="w-full btn-primary">
                        <i className="fa-solid fa-check-circle mr-2"></i>Confirmer Paiement
                      </button>
                    )}
                    <button onClick={handleDownloadPdf} className="w-full btn-secondary">
                      <i className="fa-solid fa-download mr-2"></i>Télécharger PDF
                    </button>
                    <button
                      onClick={() => { setInvoice(null); handleClearCart(); }}
                      className="w-full text-sm text-gray-500 hover:text-gray-700 py-2"
                    >
                      Nouvelle transaction
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                  <i className="fa-solid fa-file-circle-plus text-4xl mb-4"></i>
                  <p className="text-sm">Aucune facture générée</p>
                  <p className="text-xs mt-1">Ajoutez des articles et cliquez sur "Générer"</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Detection Info */}
        {detections.length > 0 && (
          <div className="mt-6 card">
            <h3 className="text-sm font-bold text-gray-600 mb-2">
              Détections ({detections.length})
            </h3>
            <div className="flex flex-wrap gap-2">
              {detections.map((det, idx) => (
                <span key={idx} className={`text-xs px-3 py-1.5 rounded-full font-medium ${
                  det.product_id ? 'bg-primary/10 text-primary' : 'bg-amber-100 text-amber-700'
                }`}>
                  {det.product_name} ({((det.similarity != null ? det.similarity : det.confidence) * 100).toFixed(0)}%)
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Checkout;
