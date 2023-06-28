const moment = require('moment');
// ...
app.get('/api/hora', (req, res) => {
  const horaActual = moment().format('HH:mm:ss');
  res.json({ hora: horaActual });
});
