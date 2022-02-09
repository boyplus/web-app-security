const express = require('express')
const app = express()
const port = 5050

app.get('/attack', (req, res) => {
  console.log(req.query.JWT)
  res.send(`JWT is ${req.query.JWT}`)
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})