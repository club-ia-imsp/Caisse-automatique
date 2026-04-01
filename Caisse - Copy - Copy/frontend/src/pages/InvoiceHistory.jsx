import React, { useState, useEffect } from 'react';
import { getInvoices, getInvoicePdf } from '../services/api';
import InvoicePreview from '../components/InvoicePreview';
import toast from 'react-hot-toast';

const InvoiceHistory = () => {
  const [invoices, setInvoices] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [selectedInvoice, setSelectedInvoice] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await getInvoices();
        setInvoices(res.data.invoices);
        setTotal(res.data.total);
      } catch {
        toast.error('Erreur de chargement');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-light flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-light p-3 sm:p-4 lg:p-6">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6 sm:mb-8">
          <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
            <i className="fa-solid fa-file-invoice mr-2 text-primary"></i>Historique des Factures
          </h1>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">{total} facture(s) au total</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
          {/* Invoice List */}
          <div className="lg:col-span-2">
            {invoices.length === 0 ? (
              <div className="card text-center py-12 sm:py-16">
                <i className="fa-solid fa-file-circle-xmark text-5xl sm:text-6xl text-gray-300 mb-4 block"></i>
                <h3 className="text-lg sm:text-xl font-bold text-gray-700 mb-2">Aucune facture</h3>
                <p className="text-gray-500 text-sm">Les factures apparaîtront ici après les transactions</p>
              </div>
            ) : (
              <div className="space-y-3">
                {invoices.map((inv) => (
                  <div
                    key={inv.id}
                    onClick={() => setSelectedInvoice(inv)}
                    className={`card cursor-pointer flex items-center justify-between transition-all ${
                      selectedInvoice?.id === inv.id ? 'border-primary ring-2 ring-primary/20' : ''
                    }`}
                  >
                    <div className="flex items-center gap-3 sm:gap-4">
                      <div className="w-10 h-10 sm:w-12 sm:h-12 bg-surface rounded-xl flex items-center justify-center">
                        <i className="fa-solid fa-file-invoice text-lg sm:text-xl text-primary"></i>
                      </div>
                      <div>
                        <p className="font-bold text-gray-800 text-sm sm:text-base">
                          Facture #{String(inv.id).slice(0, 8).toUpperCase()}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(inv.transaction_date).toLocaleString('fr-FR')}
                          {' • '}{inv.items?.length || 0} article(s)
                        </p>
                      </div>
                    </div>

                    <div className="text-right">
                      <p className="font-bold text-primary text-base sm:text-lg">{inv.total_amount.toFixed(0)} FCFA</p>
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                        inv.payment_status === 'paye'
                          ? 'bg-primary/10 text-primary'
                          : 'bg-amber-100 text-amber-600'
                      }`}>
                        {inv.payment_status === 'paye' ? (
                          <><i className="fa-solid fa-check-circle mr-1"></i>Payé</>
                        ) : (
                          <><i className="fa-solid fa-clock mr-1"></i>En attente</>
                        )}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Invoice Detail */}
          <div className="lg:col-span-1">
            <div className="sticky top-20">
              {selectedInvoice ? (
                <div>
                  <InvoicePreview invoice={selectedInvoice} />
                  <div className="mt-4">
                    <button
                      onClick={() => window.open(getInvoicePdf(selectedInvoice.id), '_blank')}
                      className="w-full btn-primary"
                    >
                      <i className="fa-solid fa-download mr-2"></i>Télécharger PDF
                    </button>
                  </div>
                </div>
              ) : (
                <div className="card text-center py-12">
                  <i className="fa-solid fa-hand-point-left text-3xl sm:text-4xl text-gray-300 mb-3 block"></i>
                  <p className="text-gray-500 text-sm">Sélectionnez une facture pour voir les détails</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InvoiceHistory;
