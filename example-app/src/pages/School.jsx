import { useState, useEffect } from 'react'
import { NavLink } from 'react-router-dom'

export default function School() {

  const [schools, setSchools] = useState(null)
  const [students, setStudents] = useState(null)
  const [invoices, setInvoices] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)
  const [activeSchoolId, setActiveSchoolId] = useState(null)

  useEffect(() => {
    Promise.all([
      fetch('/api/schools').then(res => {
        if (!res.ok) throw new Error(res.statusText)
        return res.json()
      }),
      fetch('/api/students')
      .then(res => {
        if (!res.ok) throw new Error(res.statusText)
        return res.json()
      }),
      fetch('/api/invoices')
      .then(res => {
        if (!res.ok) throw new Error(res.statusText)
        return res.json()
      })
    ]).then(([schoolsData, studentsData, invoicesData]) => {
      setSchools(schoolsData)
      setStudents(studentsData)
      setInvoices(invoicesData)
      if (schoolsData.length > 0) {
        setActiveSchoolId(schoolsData[0].id)
      }
    })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading)  return <p>Loading schools…</p>
  if (error)    return <p className="text-danger">Error: {error}</p>
  if (!schools) return null

  return (
    <div className="container my-5">
      <h2 className="mb-4">Schools Overview</h2>

      {/* Tabs */}
      <ul className="nav nav-tabs mb-4">
        {schools.map(sch => (
          <li className="nav-item" key={sch.id}>
            <button
              type="button"
              className={`nav-link ${activeSchoolId === sch.id ? 'active' : ''}`}
              onClick={() => setActiveSchoolId(sch.id)}
            >
              {sch.name}
              <span className="badge bg-secondary ms-2">{students.filter(student => student.school_id == sch.id).length}</span>
            </button>
          </li>
        ))}
      </ul>

      {/* Active school pane */}
      <div>
        {schools
          .filter(sch => sch.id === activeSchoolId)
          .map(sch => (
            <div key={sch.id}>
              <div className="table-responsive">
                <table className="table table-striped table-hover text-nowrap">
                  <thead className="table-dark">
                    <tr>
                      <th>Student</th>
                      <th>Email</th>
                      <th className="text-end">Total Due</th>
                      <th className="text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {students.filter(student => student.school_id == sch.id).map(std => {
                      const totalDue = invoices.filter(invoice => invoice.student_id == std.id && invoice.paid == false).reduce((sum, inv) => sum + inv.amount, 0)
                      return (
                        <tr key={std.id}>
                          <td>
                            <NavLink
                              to={`/student/${std.id}`}
                              state={{ student: std, invoices: invoices.filter(invoice => invoice.student_id == std.id) }}
                              className="text-decoration-none"
                            >
                              {std.name}
                            </NavLink>
                          </td>
                          <td>{std.email}</td>
                          <td className="text-end">${totalDue.toFixed(2)}</td>
                          <td className="text-center">
                            <span className={`badge ${totalDue > 0 ? 'bg-danger' : 'bg-success'}`}>
                              {totalDue > 0 ? 'Past Due' : 'Paid'}
                            </span>
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
      </div>
    </div>
  )
}
