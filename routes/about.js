const {Router} = require('express')
const Url = require('../models/addUrl')
const router = Router()

router.get('/', (req, res) => {
    const frames = [{frame: 'out/Qd1uC7K3KaE/keyframe-00005.png'}, {frame: 'out/Qd1uC7K3KaE/keyframe-00058.png'}, {frame: 'out/Qd1uC7K3KaE/keyframe-00028.png'}, {frame: 'out/Qd1uC7K3KaE/keyframe-00033.png'}, {frame: 'out/Qd1uC7K3KaE/keyframe-00017.png'}, {frame: 'out/Qd1uC7K3KaE/keyframe-00051.png'}, {frame: 'out/Qd1uC7K3KaE/keyframe-00019.png'}]

    // res.render('about', {
    //     title: 'frames',
    //     lead: 'Комикс',
    //     frames: frames
    // })
})


module.exports = router