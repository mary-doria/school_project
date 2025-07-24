import { useState } from 'react'
import { useLocation } from 'react-router-dom'

export default function Student() {
  
  const { state } = useLocation()
  const { student, invoices } = state || {}

  if (!student || !invoices) {
    return (
      <div className="container my-5">
        <div className="alert alert-warning text-center">
          Missing data.
        </div>
      </div>
    )
  }

  const [isAdding, setIsAdding]     = useState(false)
  const [newAmount, setNewAmount]   = useState('')
  const [invoicesList, setInvoicesList] = useState(invoices ?? [])

  const markPaid = (invoiceId) => {
  fetch(`/api/invoices/${invoiceId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ paid: true })
  })
    .then(res => {
      if (!res.ok) throw new Error(res.statusText)
      return res.json()
    })
    .then(updated => {

      setInvoicesList(prev =>
        prev.map(inv =>
          inv.id === updated.id ? { ...inv, paid: updated.paid } : inv
        )
      )
    })
    .catch(err => alert(`Error marking paid: ${err.message}`))
}


  const totalDue = invoicesList.filter(invoice => invoice.paid == false)
    .reduce((sum, inv) => sum + inv.amount, 0)
    .toFixed(2)

  return (
    <div className="container my-5">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="h3">{student.name}</h1>
        <span className="badge bg-primary">
          {student.email}
        </span>
      </div>

      {/* Summary Card */}
      {isAdding ? (
        <div className="card mb-4 shadow-sm">
          <div className="card-body d-flex gap-2 align-items-center">
            <input
              type="number"
              className="form-control"
              placeholder="Invoice amount"
              value={newAmount}
              onChange={e => setNewAmount(e.target.value)}
            />
            <button
              className="btn btn-primary"
              onClick={() => {
                fetch('/api/invoices', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    student_id: student.id,
                    amount:  Number(newAmount),
                    paid:     false
                  })
                })
                  .then(r => r.json())
                  .then(created => {
                    setInvoicesList(prev => [...prev, created])
                    setIsAdding(false)  
                    setNewAmount('') 
                  })
                }}
            >
              Save
            </button>
            <button
              className="btn btn-outline-secondary"
              onClick={() => {
                setIsAdding(false)
                setNewAmount('')
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="card mb-4 shadow-sm">
          <div className="card-body d-flex justify-content-between align-items-center">
            <div>
              <h5 className="card-title mb-1">Total Outstanding</h5>
              <p className="card-text display-6 mb-0">${totalDue}</p>
            </div>
            <button
              className="btn btn-success btn-lg"
              onClick={() => setIsAdding(true)}
            >
              <i className="bi bi-plus-square me-2"></i>
              New Invoice
            </button>
          </div>
        </div>
      )}

      {/* Invoices Table */}
      <div className="table-responsive shadow-sm rounded">
        <table className="table table-striped table-hover mb-0">
          <thead className="table-dark">
            <tr>
              <th>#</th>
              <th>Description</th>
              <th className="text-end">Amount</th>
              <th className="text-end">Due</th>
              <th className="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            {invoicesList.map((inv, idx) => (
              <tr key={inv.id}>
                <td>{idx + 1}</td>
                <td>Invoice #{inv.id}</td>
                <td className="text-end">${inv.amount.toFixed(2)}</td>
                <td className="text-end">
                  <span className={`badge ${inv.paid == false ? 'bg-danger' : 'bg-success'}`}>
                    ${inv.amount.toFixed(2)}
                  </span>
                </td>
                <td className="text-center">
                  <button
                    className="btn btn-outline-primary btn-sm"
                    onClick={() => markPaid(inv.id)}
                    disabled={inv.paid}             
                    title={inv.paid ? 'Already paid' : 'Mark as paid'}
                  >
                    <i className="bi bi-plus-square"></i>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
