const express = require("express");
const cors = require("cors");

const app = express();

// allow CORS from all origins
app.use(cors());

const myLogger = function (req, res, next) {
  console.log("LOGGED");
  next();
};

app.use(myLogger);

const myData = ["ido", "maya", "itay"];

app.get("/", (req, res) => {
  res.send(myData);
});

app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
