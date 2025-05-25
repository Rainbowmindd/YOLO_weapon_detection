let currentImage = null;

function openCamera() {
    const video = document.getElementById('video');
    const img = document.getElementById('imagePreview');
    const captureButton = document.getElementById('capture');
  
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
        video.style.display = 'block';      
        img.style.display = 'none';         
        captureButton.style.display = 'inline';
      })
      .catch(err => console.error('Camera error:', err));
  }
  
  function capturePhoto() {
    const video = document.getElementById('video');
    const img = document.getElementById('imagePreview');
    const captureButton = document.getElementById('capture');
  
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
  
    video.srcObject.getTracks().forEach(track => track.stop());
    video.style.display = 'none';        
    captureButton.style.display = 'none';
  
    canvas.toBlob(blob => {
      currentImage = blob;
      const url = URL.createObjectURL(blob);
      img.src = url;
      img.style.display = 'block';         
    }, 'image/jpeg');
  }
  

function showImage(src) {
  const img = document.getElementById('imagePreview');
  img.src = src;
}

async function uploadImage() {
  const fileInput = document.getElementById('fileInput');

  if (fileInput.files.length > 0) {
    currentImage = fileInput.files[0];
    const url = URL.createObjectURL(currentImage);
    showImage(url);

    fileInput.value = '';
  }

  if (!currentImage) {
    alert('No image selected');
    return;
  }

  const formData = new FormData();
  formData.append('image', currentImage);

  try {
    const response = await fetch('http://127.0.0.1:5000/detect', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    const result = document.getElementById('result');
    const log = document.getElementById('log');

    if (data.detected) {
      result.textContent = 'Weapon detected!';
    } else {
      result.textContent = 'No weapon detected.';
    }

    log.innerHTML = data.detections.map((d, i) =>
      `#${i + 1}: <strong>${d.label}</strong> - ${(d.confidence * 100).toFixed(2)}%`
    ).join('<br>') || 'No detections to display.';

  } catch (err) {
    console.error(err);
    document.getElementById('result').textContent = 'Error during detection.';
    document.getElementById('log').textContent = '';
  }
}
