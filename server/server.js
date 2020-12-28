const path = require('path');
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

const templatePath = path.join(__dirname, '..', 'templates');
const publicPath = path.join(__dirname, '..', 'static');
app.use(express.static(publicPath));

app.get('*', (req, res) => {
   res.sendFile(path.join(templatePath, 'index.html'));
});


app.listen(port, () => {
   console.log(`Server is up on port ${port}!`);
});
