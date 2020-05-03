// global variables
var sharedData;

try {
  sharedData = JSON.parse(new URLSearchParams(location.search).get('data'));
} catch (e) {}
// simplify the displayed URL in the address bar
// history.replace({}, document.title, location.origin + location.pathname);

if (sharedData.p_class == 0) {
    document.getElementById('predicted class').textContent += "fake";
} else {
    document.getElementById('predicted class').textContent += "real";
}
document.getElementById('score').textContent += sharedData.p_score;

document.getElementById('article stance ' + i).textContent += sharedData.a1_class;
document.getElementById('article link ' + i).textContent += sharedData.a1_link;
document.getElementById('article stance ' + i).textContent += sharedData.a2_class;
document.getElementById('article link ' + i).textContent += sharedData.a2_link;
document.getElementById('article stance ' + i).textContent += sharedData.a3_class;
document.getElementById('article link ' + i).textContent += sharedData.a3_link;
document.getElementById('article stance ' + i).textContent += sharedData.a3_class;
document.getElementById('article link ' + i).textContent += sharedData.a3_link;