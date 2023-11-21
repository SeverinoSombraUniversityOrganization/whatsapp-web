const flaskAppConfig = {
    host: process.env.APP_SERVICE,
    port: process.env.APP_PORT
  }
  
const flaskAppBaseUrl = `http://${flaskAppConfig.host}:${flaskAppConfig.port}/api/`

module.exports = {
  flaskAppBaseUrl
};