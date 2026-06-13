const express = require('express');
const path = require('path');
const canonRoutes = require('./routes/canon');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.use('/api', canonRoutes);

// Test route
app.get('/test', (req, res) => {
  res.json({ message: 'Server running!' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📖 Canon API: http://localhost:${PORT}/api/canon/toc`);
  console.log(`📊 Diagrams API: http://localhost:${PORT}/api/diagrams`);
});
