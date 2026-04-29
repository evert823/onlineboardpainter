// Bot authentication logic
function authenticateUser() {
  const userOrBot = document.getElementById('user-or-bot').value;
  fetch('/onlineboardpainter/api/authenticate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: userOrBot })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      isAuthenticated = true;
      document.getElementById('auth-result').innerText = data.message || 'Authenticated!';
      document.getElementById('send-btn').disabled = false;
      // Store authentication in cookie if consent given
      if (cookieConsentGiven) {
        setCookie('bot_auth', 'yes', 7);
      }
      // Hide bot defense section
      document.getElementById('bot-defense-section').style.display = 'none';
    } else {
      isAuthenticated = false;
      document.getElementById('auth-result').innerText = data.message || 'Authentication failed.';
      document.getElementById('send-btn').disabled = true;
    }
  })
  .catch(err => {
    isAuthenticated = false;
    document.getElementById('auth-result').innerText = 'Error: ' + err;
    document.getElementById('send-btn').disabled = true;
  });
}

// Cookie helpers
function setCookie(name, value, days) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days*24*60*60*1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
  const nameEQ = name + "=";
  const ca = document.cookie.split(';');
  for(let i=0;i < ca.length;i++) {
    let c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1,c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
  }
  return null;
}
function eraseCookie(name) {   
  document.cookie = name+'=; Max-Age=-99999999; path=/';  
}

// Cookie consent logic
function showCookieConsentBanner() {
  document.getElementById('cookie-consent-banner').style.display = 'block';
}
function hideCookieConsentBanner() {
  document.getElementById('cookie-consent-banner').style.display = 'none';
}
function acceptCookieConsent() {
  setCookie('cookie_consent', 'yes', 365);
  cookieConsentGiven = true;
  hideCookieConsentBanner();
  checkBotAuthOnLoad();
}
function declineCookieConsent() {
  eraseCookie('cookie_consent');
  cookieConsentGiven = false;
  hideCookieConsentBanner();
  // Optionally, disable the rest of the page or show a message
  document.getElementById('bot-defense-section').innerHTML = "<p>You must accept cookies to use this site.</p>";
  document.getElementById('send-btn').disabled = true;
}

function sendText4boardpainter() {
  if (!isAuthenticated) {
    document.getElementById('text-api-result').innerText = 'You must authenticate first.';
    return;
  }
  const text = document.getElementById('user-text').value;
  // Get selected theme
  const theme = document.querySelector('input[name="theme"]:checked').value;
  // The API endpoint may differ; you can pass it as a variable if needed
  const apiEndpoint = window.sendTextApiEndpoint || '/onlineboardpainter/api/makeboard';
  fetch(apiEndpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: text, theme: theme })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('text-api-result').innerText = data.message;
    if (data.image_file) {
      currentImageFile = data.image_file;
      document.getElementById('image-filename').innerText = data.image_file;
      const imageUrl = `/onlineboardpainter/api/image/${data.image_file}`;
      document.getElementById('board-image').src = imageUrl;
      document.getElementById('download-link').href = imageUrl;
      document.getElementById('download-link').setAttribute('download', data.image_file);
      document.getElementById('image-section').style.display = 'block';
    } else {
      document.getElementById('image-section').style.display = 'none';
    }
  })
  .catch(err => {
    document.getElementById('text-api-result').innerText = 'Error: ' + err;
    document.getElementById('image-section').style.display = 'none';
  });
}
