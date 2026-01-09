var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  const samp = ['itay', 'jonathan', 'ido', 'dean']
  console.log('SAMP:', samp);
  res.render('index', { samp });
});

module.exports = router;
