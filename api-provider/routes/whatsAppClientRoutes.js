const WhatsAppClientController = require('../controllers/whatsAppClientController')
const express = require('express');

const router = express.Router();

router.post('/initialize-client/:identifier', WhatsAppClientController.initializeClient);

module.exports = router