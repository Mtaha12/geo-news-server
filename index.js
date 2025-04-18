const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.json());


app.use(cors({
  origin: 'https://geo-news-client.vercel.app', 
  credentials: true // optional: useful if sending cookies
}));

// Routes
app.use('/api/articles', require('./routes/newsRoutes'));

// Root route
app.get('/', (req, res) => {
  res.send('Backend is running!');
});

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log('MongoDB connection error:', err));

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
