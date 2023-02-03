const {Router} = require('express')
const Url = require('../models/addUrl')
const router = Router() 
const fs = require("fs");
const { deleteUrl } = require('../models/addUrl');
const mongoose = require('mongoose')
const Schema = mongoose.Schema;

const { exec } = require('child_process')
// const { PythonShell } = require('python-shell')

// установка схемы
const urlScheme = new Schema({
    url: {
        type: String,
        required: true
    },
    id: {
        type: String,
        default: 'noId'
    },
    discription: {
        type: Boolean,
        default: false
    },
    screenlist: {
        type: Boolean,
        default: true
    },
    screencomix: {
        type: Boolean,
        default: true
    }

});

// определяем модель User
const MongoUrl = mongoose.model("mongoUrl", urlScheme);

router.get('/', async (req, res) => {
    // const urls = await Url.getAll()
    const urls = await MongoUrl.find({}).lean();
    // console.log(urls)
    
    // let time = String(+(urls[0]['length'] / 60).toFixed(0)) + " : " + String(urls[0]['length'] % 60)
    res.render('index', {
        title: 'Результаты поиска',
        isHome: true,
        isWait: false,
        lead: 'Добавлено',
        urls: urls,
        // time: time
    })
    // console.log(res);
})


router.post('/', async (req, res) => {
    const url = new Url(req.body.url)
    // await url.saveToMongo()
    const newUrl = new MongoUrl({ "url": url.url, 'id': url.id });
    await newUrl.save();
    // console.log(res);
    // res.render('index', {
    //     isWait: true,
    // })
    
    try {
        exec('descVideo.py', (error, stdout, stderr) => {
            if (error) {
            console.error(`exec error: ${error}`);
            return;
            }
            console.log(`stdout: ${stdout}`);
            // console.error(`stderr: ${stderr}`);
            res.redirect('/')
            
        });
    } catch {
        console.log('Connection problem...')
    } 

    
})

router.get("/api/urls", async (req, res)=>{
    // получаем всех 
    const urls = await MongoUrl.find({});
    res.send(urls);
});


router.get('/:id/del', async (req, res) => {
    const id = req.params.id
    
    await MongoUrl.findOneAndDelete({id: id});
    res.redirect('/')
})

router.get('/:id/edit', async (req, res) => {
    const id = req.params.id
    await MongoUrl.findOneAndUpdate({id: id}, { $set: {screenlist: false}});

    try {
        exec('screenList.py', (error, stdout, stderr) => {
            if (error) {
            console.error(`exec error: ${error}`);
            return;
            }
            console.log(`stdout: ${stdout}`);
            // console.error(`stderr: ${stderr}`);
            res.redirect('/')
            
        }); 
    } catch {
        console.log('Connection problem... Try again')
    }      


    // res.redirect('/')
})

router.get('/:id/comix', async (req, res) => {
    const id = req.params.id
    await MongoUrl.findOneAndUpdate({id: id}, { $set: {screencomix: false}});
    
    // const urls = await MongoUrl.find({}).lean();
    // res.render('index', {
    //     title: 'Результаты поиска',
    //     isHome: true,
    //     isWait: true,
    //     lead: 'Добавлено',
    //     // urls: urls,
    // })
    // res.redirect('/')
    
    try {
        exec('makeFrames.py', (error, stdout, stderr) => {
            if (error) {
            console.error(`exec error: ${error}`);
            return;
            }
            console.log(`stdout: ${stdout}`);
            // console.error(`stderr: ${stderr}`);
            res.redirect('/')
            
        }); 
    } catch {
        console.log('Connection problem... Try again')
    }    

})


router.get('/:id', async (req, res) => {
    const id = req.params.id
   
    const urls = await MongoUrl.find({}).lean();

    // console.log(urls)
    /// попробовать вместо этого reduce, может им сделать проще
    const title = urls.map((elem) => {
        if (elem.id === id) {
            return elem.title
        }
    }).filter((i) => { return i })

    const url_video = urls.map((elem) => {
        if (elem.id === id) {
            return elem.url_video
        }
    }).filter((i) => { return i })


    // console.log(title)

    const data_frame = urls.map((elem) => {
        if (elem.id === id) {
            const frames2 = []
            elem.frame.forEach(element => {
                frames2.push({'frame': element})
            });
            console.log(elem.data_frame)
            return elem.frames2
        }
    })

    const frames = urls.map((elem) => {
        if (elem.id === id) {
            const frames = []
            elem.frame.forEach(element => {
                frames.push({'frame': element})
            });
            return frames
        } 
    }).filter((i) => { return i })[0]
    // console.log(frames)

    const startSec = urls.map((elem) => {
        if (elem.id === id) {
            const startSec = []
            elem.i_frame_seconds.forEach(element => {
                startSec.push({'i_frame_seconds': element})
            });
            return startSec
        } 
    }).filter((i) => { return i })[0]
    // console.log(startSec)

    res.render('about', {
        title: title,
        urls: urls,
        frames: frames,
        id,
        url_video,
        startSec: startSec,
        data_frame 

    })

})




module.exports = router

