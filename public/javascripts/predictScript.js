document.addEventListener('keydown', function (event) {
    const inputField = document.getElementById('tickerInput');

    // Check if 'Ctrl + K' is pressed to focus
    if (event.ctrlKey && event.key === 'k') {
        event.preventDefault(); // Prevent default action of 'Ctrl + K'
        inputField.focus(); // Focus on the input field
    }

    // Check if 'Escape' is pressed to remove focus
    if (event.key === 'Escape') {
        inputField.blur(); // Remove focus from the input field
    }
});

document.getElementById('searchButton').addEventListener('click', async function () {
    // Show the loading screen
    document.getElementById('loadingScreen').classList.remove('hidden');


    // Simulate a delay or replace with your actual route
    await new Promise(resolve => setTimeout(resolve, 6000)); // Replace with fetch or async call

    // Hide the loading screen once done
    document.getElementById('loadingScreen').classList.add('hidden');
});

const toggleButton = document.getElementById('toggleButton');
const toggleDiv = document.getElementById('toggleDiv');

toggleButton.addEventListener('click', () => {
    toggleDiv.classList.toggle('hidden'); // Toggle visibility
});

