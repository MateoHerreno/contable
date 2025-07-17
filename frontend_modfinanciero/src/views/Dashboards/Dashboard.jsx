import React, { useEffect, useState } from 'react';
import {
  getResumenDashboard,
  getCXCConceptos,
  getCXPConceptos,
  getEvolucionMensual,
  getCXCResumen,
  getCXPResumen,
} from '../../services/dashboardService';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line
} from 'recharts';

const Dashboard = () => {
  const [resumen, setResumen] = useState({});
  const [cxcConceptos, setCXCConceptos] = useState([]);
  const [cxpConceptos, setCXPConceptos] = useState([]);
  const [evolucion, setEvolucion] = useState({ cxc: [], cxp: [] });
  const [cxcResumen, setCXCResumen] = useState({});
  const [cxpResumen, setCXPResumen] = useState({});

  useEffect(() => {
    getResumenDashboard().then(res => setResumen(res.data));
    getCXCConceptos().then(res => setCXCConceptos(res.data));
    getCXPConceptos().then(res => setCXPConceptos(res.data));
    getEvolucionMensual().then(res => setEvolucion(res.data));
    getCXCResumen().then(res => setCXCResumen(res.data));
    getCXPResumen().then(res => setCXPResumen(res.data));
  }, []);

  const mergeConceptos = () => {
    const merged = {};
    cxcConceptos.forEach(c => {
      const key = c.conceptoFijo__nombre;
      merged[key] = { concepto: key, cxc: c.total, cxp: 0 };
    });
    cxpConceptos.forEach(p => {
      const key = p.conceptoFijo__nombre;
      if (!merged[key]) merged[key] = { concepto: key, cxc: 0, cxp: 0 };
      merged[key].cxp = p.total;
    });
    return Object.values(merged);
  };

  const formatMes = (n) => ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'][n - 1];

  const datosLinea = () => {
    const datos = {};
    evolucion.cxc.forEach(m => {
      const mes = formatMes(m.fecha__month);
      datos[mes] = { mes, cxc: m.total, cxp: 0 };
    });
    evolucion.cxp.forEach(m => {
      const mes = formatMes(m.fecha__month);
      if (!datos[mes]) datos[mes] = { mes, cxc: 0, cxp: 0 };
      datos[mes].cxp = m.total;
    });
    return Object.values(datos);
  };

  const barrasComparativas = (titulo, data, keys, colores) => (
    <div className="bg-white rounded-xl shadow p-3 w-full">
      <h3 className="text-xs font-semibold mb-1">{titulo}</h3>
      <ResponsiveContainer width="100%" height={100}>
        <BarChart
          layout="vertical"
          data={data}
          margin={{ top: 0, right: 20, left: 0, bottom: 0 }}
        >
          <XAxis type="number" />
          <YAxis dataKey="label" type="category" />
          <Tooltip />
          <Legend />
          {keys.map((k, i) => (
            <Bar key={k} dataKey={k} fill={colores[i]} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );

  const cxcData = [
    {
      label: "CxC",
      pendiente: cxcResumen.pendiente || 0,
      recaudado: cxcResumen.recaudado || 0,
    },
  ];
  const cxpData = [
    {
      label: "CxP",
      pendiente: cxpResumen.pendiente || 0,
      pagado: cxpResumen.pagado || 0,
    },
  ];

  return (
    <div className="p-3 space-y-4">
      <div className="grid grid-cols-3 gap-1">
        <div className="bg-white rounded shadow px-3 py-2 text-center text-sm">
          <div className="d-flex justify-content-center align-items-center gap-3 flex-wrap">
            <div className="text-success fw-bold">
              Ingresos: <span className="fw-normal text-dark">${resumen.ingresos?.toFixed(2) || 0}</span>
            </div>
            <div className="text-muted">|</div>
            <div className="text-danger fw-bold">
              Egresos: <span className="fw-normal text-dark">${resumen.egresos?.toFixed(2) || 0}</span>
            </div>
            <div className="text-muted">|</div>
            <div className="text-primary fw-bold">
              Utilidad: <span className="fw-normal text-dark">${resumen.utilidad_neta?.toFixed(2) || 0}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow p-3">
        <h2 className="text-sm font-semibold mb-1">Totales por concepto</h2>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={mergeConceptos()}>
            <XAxis dataKey="concepto" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="cxc" fill="#82ca9d" name="CxC" />
            <Bar dataKey="cxp" fill="#8884d8" name="CxP" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl shadow p-3">
        <h2 className="text-sm font-semibold mb-1">Evolución mensual</h2>
        <ResponsiveContainer width="100%" height={180}>
          <LineChart data={datosLinea()}>
            <XAxis dataKey="mes" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="cxc" stroke="#82ca9d" name="CxC" />
            <Line type="monotone" dataKey="cxp" stroke="#8884d8" name="CxP" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {barrasComparativas("CxC: Recaudado vs Pendiente", cxcData, ["recaudado", "pendiente"], ["#00C49F", "#FF8042"])}
        {barrasComparativas("CxP: Pagado vs Pendiente", cxpData, ["pagado", "pendiente"], ["#8884d8", "#FF8042"])}
      </div>
    </div>
  );
};

export default Dashboard;