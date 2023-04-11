const sstk = require("shutterstock-api");
const fs = require("fs");

const applicationConsumerId = "aBvGWnvalx4FiAOAWFgIC114ntnuCAuk";
const applicationConsumerSecret = "KHVdDuWFI7vf7hOK";
sstk.setBasicAuth(applicationConsumerId, applicationConsumerSecret);



// const SHUTTERSTOCK_API_TOKEN = 'v2/YUJ2R1dudmFseDRGaUFPQVdGZ0lDMTE0bnRudUNBdWsvMTg0NTEwNTM2L2N1c3RvbWVyLzQvZjVJLWdMT2x5ZzQ0Rkk1d3l5N01KWmhzR2NPT3dGMzc1alBvVkEtYy1IM1p6Yzd1UlM3b3AyLUcyb1NFZktkTVVvRXVMRE8xSjg5SGtDdUlSN1dLZkt3MzNEbEZCMEVkN0g5c0ZrVE1XZEFYMlJoU1Fyd3owMzEzNjExd1dybzlESktVZkp6Mk0yaHc2d3FFWGRIRExBUFlmOW14LUc5alRtVm1pblZsdk4tTWUzVHVIVmJwejBGVlRwdlFyblQ0dHd2ZDV0bjV1NmtQU0luSThqaHEtUS9OU0tEemRaTGhjVHZtSTlxZUpHTHRB'
sstk.setAccessToken(process.env.SHUTTERSTOCK_API_TOKEN);

const computerVisionApi = new sstk.ComputerVisionApi();

const imageFile = fs.readFileSync("1.jpg");
const base64File = Buffer.from(imageFile).toString("base64");

const body = new sstk.ImageCreateRequest(base64File);

computerVisionApi.uploadImage(body)
  .then((data) => {
    console.log(data.upload_id);
    return computerVisionApi.getKeywords(data.upload_id);
  })
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.error(error);
  });