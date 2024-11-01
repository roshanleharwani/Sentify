const toggleButton = document.getElementById('toggleButton');
const toggleDiv = document.getElementById('toggleDiv');

toggleButton.addEventListener('click', () => {
    toggleDiv.classList.toggle('hidden'); // Toggle visibility
});

const input = document.getElementById('countryInput');
const suggestionsBox = document.getElementById('suggestions');
const countries = [
    "United States", "Canada", "Mexico", "Brazil", "Argentina", "Chile", "Peru", "Colombia",
    "United Kingdom", "Germany", "France", "Italy", "Spain", "Switzerland", "Netherlands", "Sweden",
    "Denmark", "Norway", "Poland", "Russia", "Turkey", "Greece", "Portugal", "Finland", "Austria",
    "Belgium", "Czech Republic", "Hungary", "Ireland", "Romania", "Luxembourg", "Ukraine", "Estonia",
    "Latvia", "Lithuania", "Slovenia", "Bulgaria", "Slovakia", "Croatia", "Cyprus",
    "China", "Japan", "India", "South Korea", "Hong Kong", "Taiwan", "Singapore", "Thailand",
    "Malaysia", "Indonesia", "Vietnam", "Philippines", "Bangladesh", "Pakistan", "Sri Lanka",
    "Kazakhstan", "United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait", "Oman", "Bahrain",
    "Jordan", "Israel", "South Africa", "Nigeria", "Egypt", "Kenya", "Morocco", "Ghana", "Botswana",
    "Mauritius", "Australia", "New Zealand"
];

input.addEventListener('input', () => {
    const query = input.value.toLowerCase();
    suggestionsBox.innerHTML = '';

    if (query) {
        const filteredCountries = countries.filter(country =>
            country.toLowerCase().startsWith(query)
        );

        filteredCountries.forEach(country => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = "p-2 text-sm text-gray-200 cursor-pointer hover:bg-blue-600";
            suggestionItem.textContent = country;
            suggestionItem.addEventListener('click', () => {
                input.value = country;
                suggestionsBox.classList.add('hidden');
            });
            suggestionsBox.appendChild(suggestionItem);
        });

        suggestionsBox.classList.remove('hidden');
    } else {
        suggestionsBox.classList.add('hidden');
    }
});

document.addEventListener('click', (event) => {
    if (!input.contains(event.target)) {
        suggestionsBox.classList.add('hidden');
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

    // Focus on 'Ctrl + K' and remove focus on 'Escape'
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