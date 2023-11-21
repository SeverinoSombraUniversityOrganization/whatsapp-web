const WhatsAppClientRoutes = require('./whatsAppClientRoutes');

module.exports = (app) => {
    app.use(`/api/`, WhatsAppClientRoutes);
}