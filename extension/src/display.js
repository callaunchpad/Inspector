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