 // Declare the CSRF token variable
// const canvas = document.getElementById('audioWaveform');
// const canvasContext = canvas.getContext('2d');
// let audioContext;
// let analyser;
// let microphone;
// let animationFrameId;
// const barWidth = 10; // Width of each bar
// const barSpacing = 2; // Spacing between bars

// Function to initialize audio visualization bars
// function initAudioVisualization(stream) {
//     audioContext = new (window.AudioContext || window.webkitAudioContext)();
//     analyser = audioContext.createAnalyser();
//     microphone = audioContext.createMediaStreamSource(stream);
//     microphone.connect(analyser);
//     analyser.fftSize = 256;
//     const bufferLength = analyser.frequencyBinCount;
//     const dataArray = new Uint8Array(bufferLength);
//     const numBars = Math.floor(canvas.width / (barWidth + barSpacing));

//     // Start visualization loop
//     function visualize() {
//         analyser.getByteFrequencyData(dataArray);

//         canvasContext.clearRect(0, 0, canvas.width, canvas.height);
//         canvasContext.fillStyle = 'limegreen';

//         for (let i = 0; i < numBars; i++) {
//             const barHeight = dataArray[Math.floor((i / numBars) * bufferLength)] / 2;
//             const x = i * (barWidth + barSpacing);
//             const y = canvas.height - barHeight;

//             canvasContext.fillRect(x, y, barWidth, barHeight);
//         }

//         animationFrameId = requestAnimationFrame(visualize);
//     }

//     visualize();
// }


// $(document).ready(function() {
//     // Get the CSRF token from the cookie
//     const csrftoken = getCookie('csrftoken');

//     // Add event listener for the startButton
//     $("#startButton").on("click", function() {
//         startLoop();
//     });

//     // Add event listener for the stopButton
//     $("#stopButton").on("click", function() {
//         stopLoop();
//     });

//     // Function to start the loop
//     function startLoop() {
//         sendAjaxRequest("/start_loop/", "Active");
//     }

//     // Function to stop the loop
//     function stopLoop() {
//         sendAjaxRequest("/stop_loop/", "Inactive");
//     }

//     // Function to send an AJAX request
//     function sendAjaxRequest(url, statusText) {
//         // Include the CSRF token in the headers of the AJAX request
//         $.ajax({
//             url: url,
//             type: "POST",
//             headers: {
//                 "X-CSRFToken": csrftoken
//             },
//             success: function(data) {
//                 if (data.status === 'success') {
//                     $("#status").text(statusText);
//                 }
//             }
//         });
//     }

//     // Function to get the CSRF token from the cookie
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
// });
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const audioPlayer1 = document.getElementById('audioPlayer1'); // Unique variable name
const txtToSpeech = document.getElementById('txtToSpeech');
const listenAudio = document.getElementById('listenAudio');


let mediaRecorder;
let audioChunks = [];

let csrfToken;

let audioContext;
let analyser;
let microphone;
let animationFrameId;
let canvas = document.getElementById("audioCanvas");
let canvasContext = canvas.getContext("2d");

// const audioPlayer = document.getElementById('audioPlayer');
// // Constants for visualization
const barWidth = 4;
const barSpacing = 1;

function initAudioVisualization(stream) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    microphone = audioContext.createMediaStreamSource(stream);
    microphone.connect(analyser);
    analyser.fftSize = 256;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    const numBars = Math.floor(canvas.width / (barWidth + barSpacing));

    // Start visualization loop
    function visualize() {
        analyser.getByteFrequencyData(dataArray);

        canvasContext.clearRect(0, 0, canvas.width, canvas.height);
        canvasContext.fillStyle = 'blue';

        for (let i = 0; i < numBars; i++) {
            const barHeight = dataArray[Math.floor((i / numBars) * bufferLength)] / 2;
            const x = i * (barWidth + barSpacing);
            const y = canvas.height - barHeight;

            canvasContext.fillRect(x, y, barWidth, barHeight);
        }

        animationFrameId = requestAnimationFrame(visualize);
    }

    visualize();
}
 // Function to get the CSRF token from cookies
 function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize the canvas when the page loads
document.addEventListener("DOMContentLoaded", function () {
    if (!audioContext) {
        navigator.mediaDevices
            .getUserMedia({ audio: true })
            .then(initAudioVisualization)
            .catch(function (error) {
                console.error("Error accessing microphone:", error);
            });
    }
});

$(document).ready(function() {
    // Get the CSRF token from the cookie
    const csrftoken = getCookie('csrftoken');

    // Add event listener for the startButton
    $("#startButton").on("click", function() {
        console.log("Start button clicked"); // Add this line
        startLoop();
        showcanvas();
    });

    // Add event listener for the stopButton
    $("#stopButton").on("click", function() {
        console.log("Stop button clicked"); // Add this line
        stopLoop();
        stopcanvas();
    });

    // Function to start the loop
    function startLoop() {
        sendAjaxRequest("/start_loop/", "Active");
    }

    // Function to stop the loop
    function stopLoop() {
        sendAjaxRequest("/stop_loop/", "Inactive");
    }

    function showcanvas() {
        canvas.style.display = 'block'; // Show the canvas element
        if (!audioContext) {
            navigator.mediaDevices
                .getUserMedia({ audio: true })
                .then(initAudioVisualization)
                .catch(function (error) {
                    console.error("Error accessing microphone:", error);
                });
        }
    }

    function stopcanvas() {
        canvas.style.display = 'none'; // Hide the canvas element
        // Stop the audio visualization
        cancelAnimationFrame(animationFrameId);
        if (audioContext) {
            audioContext.close().then(function () {
                audioContext = null;
            });
        }
    }

    // Function to send an AJAX request
    function sendAjaxRequest(url, statusText) {
        // Include the CSRF token in the headers of the AJAX request
        $.ajax({
            url: url,
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(data) {
                if (data.status === 'success') {
                    $("#status").text(statusText);
                }
            }
        });
    }


    // Function to play audio from a local file path
    function playAudioFromFile() {
        const audioFilePath = "{% static 'recorded_audio.wav' %}";
        // Set the source of the audio player to the provided file path
        audioPlayer1.src = audioFilePath;
        
        // Play the audio
        audioPlayer1.play();
     }

    

    // Add a click event listener for the "Play" button
$("#play-pause-button").on("click", function () {
    // Fetch the latest audio file path from the server
    fetch('/get_latest_audio_path/')
        .then(response => response.json())
        .then(data => {
            if (data.latest_audio_path) {
                playAudioFromFile(data.latest_audio_path); // Use the latest_audio_path
            } else {
                console.error('Error getting audio path:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});


// Define the play/pause button element
const playPauseButton = document.getElementById('play-pause-button');

// Define the progress bar element
const progressBar = document.getElementById('progress-bar');

// Define the audio status element
const audioStatus = document.getElementById('audio-status');

// Initialize the isPlaying flag
let isPlaying = false;

// Function to toggle play/pause
function togglePlayPause() {
    if (!isPlaying) {
        audioPlayer1.play();
        playPauseButton.textContent = "Pause";
    } else {
        audioPlayer1.pause();
        playPauseButton.textContent = "Play";
    }
    isPlaying = !isPlaying;
}

// Event listener for play/pause button click
playPauseButton.addEventListener('click', togglePlayPause);

// Event listener for timeupdate (progress) of the audio
audioPlayer1.addEventListener("timeupdate", function() {
    const currentTime = audioPlayer1.currentTime;
    const duration = audioPlayer1.duration;
    const progressPercentage = (currentTime / duration) * 100;
    progressBar.style.width = progressPercentage + "%";
});

// Event listener for when audio playback ends
audioPlayer1.addEventListener("ended", function() {
    playPauseButton.textContent = "Play";
    isPlaying = false;
});

// Event listener for the stop button (assuming you have a stop button)
$("#stop").on("click", function() {
    audioPlayer1.pause();
    audioPlayer1.currentTime = 0;
    playPauseButton.textContent = "Play";
    isPlaying = false;
});
// Function to update the audio status message
function updateAudioStatus(message) {
    audioStatus.textContent = message;
}

// Function to toggle play/pause
function togglePlayPause() {
    if (isPlaying) {
        $.post('/play_audio/', { action: 'pause' }, function (data) {
            updateAudioStatus(data.message);
        });
    } else {
        $.post('/play_audio/', { action: 'play' }, function (data) {
            updateAudioStatus(data.message);
        });
    }
    isPlaying = !isPlaying;
}
});

//This is for transcription
const transcribeButton = document.getElementById('transcribeButton');
const transcribeButtonText = document.getElementById('transcribeButtonText'); // Updated ID
const transcribeLoadingSpinner = document.getElementById('transcribeLoadingSpinner'); // Updated ID
const transcriptions = document.getElementById('transcriptions');

// Get the number of speakers input element
const numSpeakersInput = document.getElementById('numSpeakers');

csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function transcribeAudio() {
    const numSpeakers = numSpeakersInput.value; // Get the user's input for the number of speakers

    // Show loading spinner and hide button text
    transcribeButtonText.style.display = 'none'; // Updated ID
    transcribeLoadingSpinner.style.display = 'inline-block'; // Updated ID

    // Create a FormData object to include the CSRF token and send it in the request
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken); // Include the CSRF token
    formData.append('num_speakers', numSpeakers); // Include the number of speakers
    
    // Send a request to the server to transcribe the audio with the specified number of speakers
    fetch('/transcribe-audio/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Display the transcribed message on the web page
            transcriptions.innerHTML = `<p>${data.message}</p>`;
        } else {
            console.error('Error getting transcriptions:', data.error);
        }
        // Hide loading spinner and show button text in case of an error
        transcribeLoadingSpinner.style.display = 'none';
        transcribeButtonText.style.display = 'inline-block';
    })
    .catch(error => {
        console.error('Error:', error);
        // Hide loading spinner and show button text in case of an error
        transcribeLoadingSpinner.style.display = 'none';
        transcribeButtonText.style.display = 'inline-block';
    });
}

transcribeButton.addEventListener('click', () => {
    transcribeAudio();
});

//this is for audio generation
const callGenerateAudioButton = document.getElementById('GenerateAudio');

// Function to generate audio
function generateAudio(targetLanguage) {
   // const targetLanguage = document.getElementById('targetLanguage').value; // Get the selected language
    // Send the target language to the server for audio generation
    fetch('/generate_audio/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ target_language: targetLanguage }),  // Use 'target_language'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // Log the response data
        if (data.result) {
            console.log('Audio generated successfully:', data.result);
            // Optionally, you can update the UI or provide feedback to the user here
        } else {
            console.error('Error:', data.result);
            // Handle the error or provide feedback to the user
        }
    })
    
    .catch(error => {
        console.error('AJAX Error:', error);
        // Handle the error or provide feedback to the user
    })
    .finally(() => {
        // Disable loading state for Generate Audio button
        document.getElementById('generateAudioLoadingSpinner').style.display = 'none';
        document.getElementById('generateAudioButtonText').style.display = 'inline-block';
    });
}

// Add an event listener for the "Generate Audio" button
document.addEventListener('DOMContentLoaded', function () {

    callGenerateAudioButton.addEventListener('click', () => {
        // Enable loading state for Generate Audio button
        const generateAudioLoadingSpinner = document.getElementById('generateAudioLoadingSpinner');
        const generateAudioButtonText = document.getElementById('generateAudioButtonText');
        
        generateAudioLoadingSpinner.style.display = 'inline-block';
        generateAudioButtonText.style.display = 'none';

        // Get the selected target language from the dropdown
        const targetLanguage = document.getElementById('targetLanguage').value;

        // Call the generateAudio function
        generateAudio(targetLanguage);
    });
});

    // Translate Section
    const translateButton = document.getElementById('translateButton');
    const translateBox = document.getElementById('translateBox');
    const translateButtonText = document.getElementById('translateButtonText'); // Updated ID
    const translateLoadingSpinner = document.getElementById('translateLoadingSpinner'); // Updated ID

    // Function to translate audio
function translateAudio() {
    // Enable loading state for Translate button
    translateButtonText.style.display = 'none'; // Updated ID
    translateLoadingSpinner.style.display = 'inline-block'; // Updated ID

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const targetLanguage = document.getElementById('targetLanguage').value; // Get the selected language

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('target_language', targetLanguage); // Include the selected language

    fetch('/translate/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.translated_text !== undefined) { // Check if translated_text is defined
            translateBox.innerHTML = `<p>${data.translated_text}</p>`;
        } else {
            console.error('Error getting translation: Unexpected response', data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        // Disable loading state for Translate button
        translateLoadingSpinner.style.display = 'none'; // Updated ID
        translateButtonText.style.display = 'inline-block'; // Updated ID
    });
}

    if (translateButton) {
        translateButton.addEventListener('click', () => {
            translateAudio();
        });
    }
    
