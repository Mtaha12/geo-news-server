const mongoose = require('mongoose');
// model to store title and content 
const newsSchema = new mongoose.Schema({
  title: String,
  content: String,
}, { timestamps: true,
    collection: 'articles'
 });

module.exports = mongoose.model('News', newsSchema);
