let psl = require('psl');
let url = 'http://www.youtube.com/watch?v=ClkQA2Lb_iE';
psl.get(extractHostname(url)); // returns youtube.com
