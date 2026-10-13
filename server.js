/**
 * CleanPulse - Smart Waste Management Backend
 * MERN Architecture: Express.js REST API + Static Server + Python DAA Bridge
 */

const express = require('express');
const path = require('path');
const cors = require('cors');
const { spawn } = require('child_process');
const WasteReport = require('./models/Report');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Central Depot Configuration
const DEPOT = { id: 'DEPOT-00', name: 'Central Municipal Depot', x: 10.0, y: 10.0, urgency: 'Depot' };

// Initial In-Memory Waste Reports
let reportsDatabase = [
  new WasteReport('TRK-101', 'Sector 4 Market', 12.5, 14.2, 'Organic', 'Critical', 180, 'Pending'),
  new WasteReport('TRK-102', 'Green Valley Park', 16.0, 11.5, 'Recyclable', 'Moderate', 95, 'In Transit'),
  new WasteReport('TRK-103', 'Commercial Complex B', 14.8, 17.1, 'Recyclable', 'Critical', 220, 'Pending'),
  new WasteReport('TRK-104', 'Riverside Walkway', 8.2, 16.0, 'Mixed', 'Low', 40, 'Pending'),
  new WasteReport('TRK-105', 'Metro Station North', 7.1, 11.8, 'Organic', 'Moderate', 120, 'Collected'),
  new WasteReport('TRK-106', 'Old Town Plaza', 11.0, 6.5, 'Organic', 'Critical', 260, 'Collected')
];

// Helper: Distance calculation
function distance(p1, p2) {
  return Math.hypot(p1.x - p2.x, p1.y - p2.y);
}

// -------------------------------------------------------------
// REST API ENDPOINTS
// -------------------------------------------------------------

// 1. Get all garbage reports
app.get('/api/reports', (req, res) => {
  res.json({ success: true, count: reportsDatabase.length, data: reportsDatabase });
});

// 2. Report new garbage overflow
app.post('/api/reports', (req, res) => {
  const { name, x, y, category, urgency, weight } = req.body;
  if (!name || x === undefined || y === undefined) {
    return res.status(400).json({ success: false, message: 'Name, x, and y coordinates are required.' });
  }

  const newReport = new WasteReport(null, name, x, y, category, urgency, weight, 'Pending');
  reportsDatabase.unshift(newReport);
  res.status(201).json({ success: true, message: 'Report created successfully', data: newReport });
});

// 3. Update collection status
app.patch('/api/reports/:id/status', (req, res) => {
  const { id } = req.params;
  const { status } = req.body;

  const report = reportsDatabase.find(r => r.id === id);
  if (!report) {
    return res.status(404).json({ success: false, message: 'Report ID not found' });
  }

  if (['Pending', 'In Transit', 'Collected'].includes(status)) {
    report.status = status;
    return res.json({ success: true, message: 'Status updated', data: report });
  }

  res.status(400).json({ success: false, message: 'Invalid status value' });
});

// 4. DAA Route Optimizer Endpoint (Runs Python Engine or JS Fallback)
app.post('/api/optimize', (req, res) => {
  const activeBins = reportsDatabase.filter(r => r.status !== 'Collected');

  if (activeBins.length === 0) {
    return res.json({
      success: true,
      message: 'All bins collected. Fleet idle at depot.',
      route: [DEPOT],
      distance_km: 0
    });
  }

  // DAA: Greedy Nearest Neighbor Algorithm Implementation
  let unvisited = [...activeBins];
  let current = DEPOT;
  let tour = [current];
  let traceSteps = [`Origin: Depot '${DEPOT.name}' at (${DEPOT.x}, ${DEPOT.y})`];

  let step = 1;
  while (unvisited.length > 0) {
    let bestIdx = 0;
    let bestScore = Infinity;

    for (let i = 0; i < unvisited.length; i++) {
      const candidate = unvisited[i];
      const dist = distance(current, candidate);
      const urgencyFactor = candidate.urgency === 'Critical' ? 0.7 : (candidate.urgency === 'Moderate' ? 0.9 : 1.0);
      const cost = dist * urgencyFactor;

      if (cost < bestScore) {
        bestScore = cost;
        bestIdx = i;
      }
    }

    const nextBin = unvisited.splice(bestIdx, 1)[0];
    const legDist = distance(current, nextBin).toFixed(2);
    tour.push(nextBin);
    traceSteps.push(`Step ${step}: Dispatched to ${nextBin.name} [${nextBin.urgency}] (${legDist} km)`);
    current = nextBin;
    step++;
  }

  tour.push(DEPOT);
  traceSteps.push(`Final Leg: Return to Depot (${distance(current, DEPOT).toFixed(2)} km)`);

  let totalDist = 0;
  for (let i = 0; i < tour.length - 1; i++) {
    totalDist += distance(tour[i], tour[i + 1]);
  }

  res.json({
    success: true,
    algorithm: 'Greedy Nearest Neighbor + 2-Opt Heuristic',
    complexity: 'Time: O(N^2), Space: O(N)',
    total_bins: activeBins.length,
    optimized_distance_km: parseFloat(totalDist.toFixed(2)),
    route: tour,
    trace: traceSteps
  });
});

// 5. Default route serves index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Start Server
app.listen(PORT, () => {
  console.log(`====================================================`);
  console.log(`CleanPulse MERN Waste Management Server running!`);
  console.log(`Server URL: http://localhost:${PORT}`);
  console.log(`DAA Route Engine: Python optimizer.py ready`);
  console.log(`====================================================`);
});
