const video = document.getElementById('video');
const captureButton = document.getElementById('capture');
const webcamForm = document.getElementById('webcamForm');
const webcamImageInput = document.getElementById('webcamImage');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => console.error('Error accessing webcam:', err));

captureButton.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    const dataURL = canvas.toDataURL('image/png');
    webcamImageInput.value = dataURL;
    webcamForm.submit();
});