const express = require('express');
const router = express.Router();
const { getAllNews } = require('../controllers/newsController');
//end point to get data
router.get('/', getAllNews);

module.exports = router;
