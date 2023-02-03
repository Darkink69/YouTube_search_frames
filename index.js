const express = require('express')
const path = require('path')
const app = express()
const ejs = require('ejs')
const exphbs = require('express-handlebars')
const aboutRoutes = require('./routes/about')
const homeRoutes = require('./routes/home')
const fs = require("fs");
const mongoose = require('mongoose')
// const Schema = mongoose.Schema;
// const Url = require('../express_2/models/addUrl')
const mysql = require("mysql2");

  
// const connection = mysql.createConnection({
//   host: "localhost",
//   user: "root",
//   database: "usersdb",
//   password: "Qwerty_69"
// });
// connection.connect(function(err){
// if (err) {
//     return console.error("Ошибка: " + err.message);
// }
// else{
//     console.log("Подключение к серверу MySQL успешно установлено");
// }
// });


// const sql = "DELETE FROM users WHERE firstname=?";
// const data = ["Tom"];
// connection.query(sql, data, function(err, results) {
//     if(err) console.log(err);
//     console.log(results);
// });

// connection.end();


const { title } = require('process')
// const MongoClient = require("mongodb").MongoClient
// const objectId = require("mongodb").ObjectId
const jsonParser = express.json();


const hbs = exphbs.create({
    defaultLayout: 'main',
    extname: 'hbs'
})

app.engine('hbs', hbs.engine)
app.set('view engine', 'hbs')
app.set('views', 'views')


async function main() {
    // подключемся к базе данных
    await mongoose.connect("mongodb://127.0.0.1:27017/urldb");
    app.listen(3000);
    console.log("Сервер ожидает подключения...");
     
    // сохраняем модель user в базу данных
    // await url.save();
    // console.log("Сохранен объект", url);

    // добавляем объект в БД
    // const user = await Url.create({url: "Sam", age: 28})
    // console.log(user);
    // const urls = await Url.find({id: 'tqt3YZ6gG2w'});
    // const id = "638eb56c99ffa07dc8f9c5a1";
    // const url = await Url.findByIdAndDelete(id);
    // const url = await Url.updateOne({id: "Tom Smith"}, {url: "youtu"})
    // console.log(url);
    // const url = await Url.insertOne({id: "1111"}, {url: "11111111"})

    // отключаемся от базы данных
    // await mongoose.disconnect();
}
// запускаем подключение и взаимодействие с базой данных
main().catch(console.log);


// const PORT = process.env.PORT || 3000
// app.listen(PORT, () => {
//     console.log(`Running on ${PORT}`)
// })


app.use(express.static('views'))
app.use(express.urlencoded({extended: true}))
app.use('/about', aboutRoutes)
app.use('/', homeRoutes)

// const jsonParser = express.json();
  
// app.post("/user", jsonParser, function (request, response) {
//     console.log(request.body);
//     if(!request.body) return response.sendStatus(400);
     
//     response.json(request.body); // отправляем пришедший ответ обратно
// });
  
// app.get("/user", function(request, response){
      
//     response.sendFile(__dirname + "/index.html");
// });

// hbs.registerHelper("getTime", function(){
      
//     const myDate = new Date();
//     const hour = myDate.getHours();
//     let minute = myDate.getMinutes();
//     let second = myDate.getSeconds();
//     if (minute < 10) {
//         minute = "0" + minute;
//     }
//     if (second < 10) {
//         second = "0" + second;
//     }
//     return `${hour}:${minute}:${second}`;
// });


// app.use('/contact', (req, res) => {
//     res.render('contact', {
//         title: 'Контакты',
//         emailVisible: true,
//         email: ['sdhfg@mail.ru', 'sdhjf@gmail.com'],
//         phone: ['+835413542', '+735437434']
//     })
    
// })




// const mongoClient = new MongoClient("mongodb://127.0.0.1:27017/");

// const urls = [{url: 'urldfhfdghdgf', id: '87364587'}, {url: 'ryugfuy', id: 'hjhsdbfj'}]

async function run() {
    try {
        // Подключаемся к серверу
        await mongoClient.connect();
        console.log("Подключение установлено");
        // взаимодействие с базой данных
        const db = mongoClient.db("shop");
        const collection = db.collection("courses");
        // app.locals.collection = mongoClient.db("shop").collection("courses");

        const url = {url: "вася", id: '545'};
        // const result = await collection.insertOne(url);
        // const result = await collection.insertMany(urls)
        // const result = await collection.find({}).sort({price: 1}).limit(3).toArray();
        // const result = await collection.find({price: {$in: [867, 550]}}).toArray();
        const result = await collection.find({}).toArray();
        // const result = await collection.findOneAndUpdate({id: 25}, { $set: {id: '50'}}, { returnDocument: "after" });
        // const result = await collection.drop()
        // const result = await collection.deleteOne({title: 'Третий'})
        // const result = await collection.find({title: 'Красивый пляж'}).count()
        // result.forEach((i) => {
        //     console.log(i)
        // });
        console.log(result)
        // console.log();

        const count = await collection.countDocuments();
        console.log(`В коллекции ${count} документа/ов`);

        


        // const result = await db.command({ ping: 1 });
        // console.log(result);
    }catch(err) {
        console.log(err);
        console.log("Возникла ошибка");
        await mongoClient.close();
        console.log("Подключение закрыто");
    } 
}
// run().catch(console.log);

// process.on("SIGINT", async() => {
      
//     await mongoClient.close();
//     console.log("Приложение завершило работу");
//     process.exit();
// });

// app.use(express.static(`${__dirname}/public`));
// (async () => {
//     try {
//        await mongoClient.connect();
//        app.locals.collection = mongoClient.db("shop").collection("courses");
//        app.listen(3000);
//        console.log("Сервер ожидает подключения...");
//    }catch(err) {
//        return console.log(err);
//    } 
// })();
 


// app.get("/api/urls", async(req, res) => {
          
//     const collection = req.app.locals.collection;
//     console.log(collection)
//     try{
//         const urls = await collection.find({}).toArray();
//         res.send(urls);
//     }
//     catch(err){
//         console.log(err);
//         res.sendStatus(500);
//     }  
// });

// app.get("/api/urls/:id", async(req, res) => {
          
//     const collection = req.app.locals.collection;

//     try{
//         const id = new objectId(req.params.id);
//         console.log(id)
//         const urls = await collection.findOne({_id: id});
//         if(urls) res.send(urls);
//         else res.sendStatus(404);
//     }
//     catch(err){
//         console.log(err);
//         res.sendStatus(500);
//     }
// });


// async function start() {
//     try {
//         // const url = `mongodb+srv://Vladimir:4KxcugEKEsHOfOz7@cluster0.bil34jn.mongodb.net/?retryWrites=true&w=majority`
//         const url = `mongodb://localhost:27017/shop`
//         await mongoose.connect(url, {
//             useUnifiedTopology: true,
//             useNewUrlParser: true
//         })
//         // app.listen(PORT, () => {
//         //     console.log(`Server is running on port ${PORT}`)
//         // })
    
        
//     } catch (e) {
//         console.log(e)
//     }
// }

// start()

// const db = 


// const urlencodedParser = express.urlencoded({extended: false})
// app.get("/1", (request, response) => {
     
//     response.send(`   <h1>Введите данные</h1>
//     <form method="post">
//         <label>Имя</label><br>
//         <input type="text" name="userName" /><br><br>
//         <label>Возраст</label><br>
//         <input type="number" name="userAge" /><br><br>
//         <input type="submit" value="Отправить" />
//     </form>`);
//     // console.log(request.query)
//     // response.send(request.query.id)
//     // response.send(Buffer.from("Hello Express"));
// });
// app.use(express.static(__dirname + "/public"));
// app.use('/', function (request, response) {
//     response.sendFile(__dirname + "/pp.jpg");
// });

// app.use("/1",function (request, response) {
//     response.sendStatus(404)
// });
// app.post('/1', urlencodedParser, (req, res) => {
//     if(!req.body) return res.sendStatus(400);
//     console.log(req.params)
//     res.send(`${req.body.userName}, ${req.body.userAge}`)
// })







// server log
app.use(function(request, response, next){
    let now = new Date()
    let data = `${now} ${request.method} ${request.url} ${request.get("user-agent")}`;
    fs.appendFile("server.log", data + "\n", function(){});
    next();
});


