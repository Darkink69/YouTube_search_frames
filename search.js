// const { execSync } = require('child_process');

// execSync('dir', (error, stdout, stderr) => {
//   if (error) {
//     // console.error(`error: ${error.message}`);
//     return;
//   }

//   if (stderr) {
//     // console.error(`stderr: ${stderr}`);
//     return;
//   }

//   console.log(`stdout:\n${stdout}`);
// });

// process_call_str = 'yt-dlp "ytsearch3:angelina joly" --get-id'
// output = subprocess.check_output(process_call_str, shell=True)
// print(output)

let execSync = require('child_process').execSync;
execSync('dir', {stdio: ['ignore', process.stdout, 'ignore']});





