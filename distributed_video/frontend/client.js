
const fileInput = document.querySelector('input[id="fileUpload"]');
const reader = new FileReader();
document.getElementById("uploadButton").style.display = 'none';
let selectedFile = null; 

fileInput.addEventListener('change', (e) => {
    selectedFile = fileInput.files[0];
    if (selectedFile) {
        reader.readAsDataURL(selectedFile);
        document.querySelector('.fileName').textContent = selectedFile.name;
        document.getElementById("uploadButton").style.display = 'block';
    }
});


function uploadFile() {
    console.log(reader);
    let fileName = selectedFile.name.replace(/[.].*/, '');
    const randomId = Math.floor(Math.random() * 9000 + 1000);
    fileName = fileName + "_" + randomId
    console.log(fileName);

}