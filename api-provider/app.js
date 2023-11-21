const express = require('express');
const routes = require('./routes'); 
const { flaskAppBaseUrl } = require('./config/flaskAppConfig');
const axios = require('axios');

const app = express();
routes(app)

const port = process.env.API_PROVIDER_PORT || 3000;
const host = process.env.API_PROVIDER_HOST || '0.0.0.0';

app.listen(port, host, (err) => {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  console.log(`Server is now listening on http://${host}:${port}`);
});
