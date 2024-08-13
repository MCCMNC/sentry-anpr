const PORT = 80;
const SOCKPORT = 681;

var express = require('express');
const session = require('express-session');
var path = require('path');
const bcrypt = require("bcrypt");
const bodyParser = require('body-parser');
var app = express();
const fs = require('fs');

const http = require('http');
const httpServer = http.createServer(app);
const io = require("socket.io")(httpServer, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

io.on('connection', (socket) => {
    console.log('A client connected');

    socket.on('frame', (base64Frame) => {
        socket.broadcast.emit('frame', base64Frame);
    });

    socket.on('disconnect', () => {
        console.log('A client disconnected');
    });
});

httpServer.listen(SOCKPORT, () => {
    console.log("IO listening on port", SOCKPORT);
});


const { execQuery, getRows } = require('./dbinterface');
const { createHash } = require('crypto');

app.set('views', path.join(__dirname, 'www'));

app.set('view engine', 'ejs')
app.use(bodyParser.urlencoded({ extended: true }))

app.use(session({
    secret: 'fd17320a4c84af82203348c9cf843439e7ca5871c4ed7ff4d4935f9721068832',
    resave: false,
    saveUninitialized: true
}));

const users = [
    { id: 1, username: 'admin', password: '$2b$10$FSraBAEbj7Pg5qSh6mO68eJSjRDW/EKAsXPOIzgzt2J/XhVK8F79y' }, //pass: "pdenterprise-lpr"
];


app.use(express.static(path.join(__dirname, './www/assets/')));

function auth(req, res, next) {
    if ((req.session && req.session.userId)) {
        next();
    } else {
        res.redirect('/login');
    }
}

app.get('/login', function(req, res){
    if ((req.session && req.session.userId)) {
        res.redirect('/dashboard')
    }else{
        res.render('login')
    }
});

app.get('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
            console.error('Error destroying session:', err);
            res.status(500).send('Internal Server Error');
        } else {
            res.redirect('/login');
        }
    });
});

app.post('/login_submit', async (req, res) => {
    console.log("reached post", req.body)
    username = req.body.username;
    password = req.body.password;
    console.log("username", username);

    const user = users.find(user => user.username === username);
    userpass_correct = await bcrypt.compare(password, user.password);
    if (!userpass_correct) {
        return res.redirect('/login');
    }else{
        req.session.userId = user.id;
        res.redirect('/dashboard');
    }
});

/////////////////////////////////////////////////////////
////////////////// REQUIRES AUTH BELOW //////////////////
/////////////////////////////////////////////////////////

app.get('/view/db_caught/*', auth, (req, res) => {
    const folder_dir = "../db_caught";
    const img = req.params[0];

    const imgpath = path.join(folder_dir, img);
    
    if(fs.existsSync(imgpath)){
        const stream = fs.createReadStream(imgpath);
        stream.pipe(res)
    }else{
        res.status(404).send("NOT FOUND - Image may have been deleted.")
    }
})

app.post('/insert_whitelist', auth, (req, res) => {
    const query = "INSERT INTO whitelist (regnum, owner, msisdn, date_added) VALUES (?, ?, ?, datetime('now'))";
    const values = [req.body.regnum, req.body.owner, req.body.msisdn];
    console.log("INSERTED VALUES to whitelist: ", values)

    execQuery(query, values);

    res.redirect('/whitelist');

});

app.post('/delete_entry/:dbid/value/:val', auth, (req, res) => {
    dbid = req.params.dbid;
    val = req.params.val;
    
    if(dbid == "whitelist"){
        query = "DELETE FROM whitelist WHERE regnum = ?";
        execQuery(query, val);
    
    }else if(dbid == "history"){
        query = "DELETE FROM history WHERE pid = ?";
        execQuery(query, val);
    }
    else{
        res.status(400);
        res.send("Wrong table");
    }
});

app.get('/', auth, function(req, res){
    res.redirect("/dashboard")
});

app.get('/dashboard', auth, function(req, res){
    res.render("dashboard", {username})
});

app.get('/whitelist', auth, function(req, res){
    res.render("whitelist", {username})
});

app.get('/db/history', auth, function(req, res){
    getRows("SELECT * FROM history ORDER BY pid DESC", [])
    .then(rows => {
        res.json(rows)
    })
    .catch(err => {
        console.error('Error:', err);
        res.status(500).send('Internal Server Error');
    });
});

app.get('/db/timetable', auth, function(req, res){
    getRows("SELECT regnum, TIME(passing_date) AS TIME FROM history ORDER BY pid DESC LIMIT 5;", [])
    .then(rows => {
        res.json(rows)
    })
    .catch(err => {
        console.error('Error:', err);
        res.status(500).send('Internal Server Error');
    });
});

app.get('/db/whitelist', auth, function(req, res){
    getRows("SELECT * FROM whitelist ORDER BY date_added DESC", [])
    .then(rows => {
        res.json(rows)
    })
    .catch(err => {
        console.error('Error:', err);
        res.status(500).send('Internal Server Error');
    });
});

app.get('/history', auth, function(req, res){
    res.render("history", {username})
});


app.get('*', auth, function(req, res){
    res.status(404);
    res.send("<h1>404 Not found.</h1>")
});


app.listen(PORT, function (err) {
    if (err) console.log(err);
    console.log("Server listening on PORT", PORT);
});