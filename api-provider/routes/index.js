const WhatsAppClientRoutes = require('./WhatsAppClientRoutes');

module.exports = (app) => {
    app.use(`/api/`, WhatsAppClientRoutes);
}