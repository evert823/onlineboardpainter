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
