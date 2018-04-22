let webpack = require('webpack');
let WebpackDevServer = require('webpack-dev-server');
let config = require('./webpack.config');

let express = require('express');

let app = express();

const accountSid = 'ACdb42839152001dd533b660dc56627132'; // Your Account SID from www.twilio.com/console
const authToken = '19e9b7ed9b5697ff28af14849f21e45d';   // Your Auth Token from www.twilio.com/console
let twilio = require('twilio');
let client = new twilio(accountSid, authToken);

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/twilio', function(req, res) {
    let can_id = 'can_1';
    res.send('hi');

    client.messages.create({
      body: 'Hello, ' + can_id + ' is full!',
      to: '+15084100364',  // Text this number
      from: '+15089288734' // From a valid Twilio number
    })
    .then((message) => console.log('Sent text for ' + can_id));
});

new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  hot: true,
  historyApiFallback: true
}).listen(3000, 'localhost', function (err, result) {
  if (err) {
    return console.log(err);
  }

  console.log('Webpack dev server listening at http://localhost:3000/');
});

app.listen(5000);
console.log('Twillio server listening at http://localhost:5000/');