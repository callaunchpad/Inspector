// global variables
var sharedData;

try {
  sharedData = JSON.parse(new URLSearchParams(location.search).get('data'));
} catch (e) {}
// simplify the displayed URL in the address bar
// history.replace({}, document.title, location.origin + location.pathname);

document.getElementById('predicted class').textContent += sharedData.p_class;
document.getElementById('score').textContent += sharedData.p_score;
