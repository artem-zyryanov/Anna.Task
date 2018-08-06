var source = document.getElementById("entry-template").innerHTML;
var template = Handlebars.compile(source);

const wsUri = 'ws://' + window.location.host + '/api/v1/buzzword/';
const conn = new WebSocket(wsUri);
conn.onmessage = function (e) {

    const elem = document.getElementById("counter");
    if (elem) {
        const data = JSON.parse(e.data);
        data.words_count = Object.keys(data.words_count).map(k => {
            return {
                word: k,
                count: data.words_count[k]
            }
        });
        elem.innerHTML = template(data);
    }
};

