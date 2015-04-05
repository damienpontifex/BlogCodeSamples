/// <reference path="../typings/tsd.d.ts" />
import http = require('http');

var server: http.Server = http.createServer((request: http.ServerRequest, response: http.ServerResponse) => {  
    response.writeHead(200, {'Content-Type': 'text/plain'});
    response.write('Hello World from our TypeScript app');
    response.end();
});
var port = process.env.port || 1337;  
server.listen(port);  
console.log('Running server at http://localhost:' + port);  