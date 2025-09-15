// ===== WEATHER DASHBOARD APPLICATION =====
// Demonstrating JavaScript concepts: scope, parameters, return values, and animation triggers

// Global scope variables
const API_KEY = 'your_api_key_here'; // Replace with actual API key
const BASE_URL = 'https://api.openweathermap.org/data/2.5/weather';
const RECENT_SEARCHES_KEY = 'recentWeatherSearches';

// DOM Elements - Module scope
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const currentLocationBtn = document.getElementById('currentLocationBtn');
const weatherCard = document.getElementById('weatherCard');
const loadingElement = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');

// Function to initialize the application
function initApp() {
    console.log('Initializing Weather Dashboard...');
    
    // Load recent searches from localStorage
    loadRecentSearches();
    
    // Event listeners with proper scope handling
    setupEventListeners();
    
    // Check if we have a recent search to show
    const recentSearches = getRecentSearches();
    if (recentSearches.length > 0) {
        getWeatherData(recentSearches[0]); // Show most recent search
    }
}

// Function to set up event listeners (demonstrating function scope)
function setupEventListeners() {
    // Event listener for search button
    searchBtn.addEventListener('click', handleSearch);
    
    // Event listener for Enter key in input field
    cityInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    
    // Event listener for current location button
    currentLocationBtn.addEventListener('click', getCurrentLocationWeather);
}

// Function to handle search (demonstrating parameters and return values)
function handleSearch() {
    const cityName = cityInput.value.trim();
    
    if (!cityName) {
        showError('Please enter a city name');
        return; // Early return
    }
    
    // Clear previous error
    hideError();
    
    // Get weather data (function with parameter)
    getWeatherData(cityName);
}

// Function to get weather data (demonstrating async/await and API calls)
async function getWeatherData(cityName) {
    showLoading();
    
    try {
        // Construct URL with parameters
        const url = `${BASE_URL}?q=${encodeURIComponent(cityName)}&appid=${API_KEY}&units=metric`;
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Process and display weather data
        displayWeatherData(data);
        
        // Add to recent searches
        addToRecentSearches(cityName);
        
    } catch (error) {
        console.error('Error fetching weather data:', error);
        showError('City not found. Please try again.');
    } finally {
        hideLoading();
    }
}

// Function to get weather by current location (demonstrating geolocation API)
function getCurrentLocationWeather() {
    if (!navigator.geolocation) {
        showError('Geolocation is not supported by your browser');
        return;
    }
    
    showLoading();
    
    // Success callback function
    const successCallback = async (position) => {
        const { latitude, longitude } = position.coords;
        
        try {
            const url = `${BASE_URL}?lat=${latitude}&lon=${longitude}&appid=${API_KEY}&units=metric`;
            const response = await fetch(url);
            const data = await response.json();
            
            displayWeatherData(data);
            addToRecentSearches(data.name);
            
        } catch (error) {
            showError('Unable to get location weather data');
        } finally {
            hideLoading();
        }
    };
    
    // Error callback function
    const errorCallback = (error) => {
        hideLoading();
        showError('Unable to retrieve your location');
        console.error('Geolocation error:', error);
    };
    
    // Get current position
    navigator.geolocation.getCurrentPosition(successCallback, errorCallback, {
        timeout: 10000,
        enableHighAccuracy: true
    });
}

// Function to display weather data (demonstrating DOM manipulation and parameters)
function displayWeatherData(data) {
    const {
        name: cityName,
        main: { temp, feels_like, humidity },
        weather: [weatherInfo],
        wind: { speed: windSpeed }
    } = data;
    
    // Update DOM elements
    document.getElementById('cityName').textContent = cityName;
    document.getElementById('temperature').textContent = `${Math.round(temp)}°C`;
    document.getElementById('weatherDescription').textContent = weatherInfo.description;
    document.getElementById('humidity').textContent = `${humidity}%`;
    document.getElementById('windSpeed').textContent = `${Math.round(windSpeed * 3.6)} km/h`; // Convert m/s to km/h
    document.getElementById('feelsLike').textContent = `${Math.round(feels_like)}°C`;
    
    // Update weather icon based on condition
    updateWeatherIcon(weatherInfo.main);
    
    // Trigger animation
    triggerWeatherCardAnimation();
}

// Function to update weather icon (demonstrating switch statement and return values)
function updateWeatherIcon(weatherCondition) {
    const iconElement = document.getElementById('weatherIcon');
    let icon = '☀️'; // Default icon
    
    switch(weatherCondition.toLowerCase()) {
        case 'clear':
            icon = '☀️';
            break;
        case 'clouds':
            icon = '☁️';
            break;
        case 'rain':
            icon = '🌧️';
            break;
        case 'drizzle':
            icon = '🌦️';
            break;
        case 'thunderstorm':
            icon = '⛈️';
            break;
        case 'snow':
            icon = '❄️';
            break;
        case 'mist':
        case 'fog':
            icon = '🌫️';
            break;
        default:
            icon = '🌤️';
    }
    
    iconElement.textContent = icon;
    return icon; // Return the icon for potential use
}

// Function to trigger weather card animation (demonstrating animation triggers)
function triggerWeatherCardAnimation() {
    weatherCard.classList.remove('fade-in');
    // Trigger reflow
    void weatherCard.offsetWidth;
    weatherCard.classList.add('fade-in');
}

// Function to show loading state
function showLoading() {
    loadingElement.classList.remove('hidden');
    weatherCard.style.opacity = '0.5';
}

// Function to hide loading state
function hideLoading() {
    loadingElement.classList.add('hidden');
    weatherCard.style.opacity = '1';
}

// Function to show error message
function showError(message) {
    errorMessage.innerHTML = `<p>❌ ${message}</p>`;
    errorMessage.classList.remove('hidden');
    
    // Auto-hide error after 5 seconds
    setTimeout(hideError, 5000);
}

// Function to hide error message
function hideError() {
    errorMessage.classList.add('hidden');
}

// Recent searches functionality (demonstrating localStorage and array methods)
function getRecentSearches() {
    const recent = localStorage.getItem(RECENT_SEARCHES_KEY);
    return recent ? JSON.parse(recent) : [];
}

function saveRecentSearches(searches) {
    localStorage.setItem(RECENT_SEARCHES_KEY, JSON.stringify(searches));
}

function addToRecentSearches(cityName) {
    let recentSearches = getRecentSearches();
    
    // Remove if already exists (avoid duplicates)
    recentSearches = recentSearches.filter(city => city.toLowerCase() !== cityName.toLowerCase());
    
    // Add to beginning of array
    recentSearches.unshift(cityName);
    
    // Keep only last 5 searches
    recentSearches = recentSearches.slice(0, 5);
    
    saveRecentSearches(recentSearches);
    updateRecentSearchesUI();
}

function loadRecentSearches() {
    updateRecentSearchesUI();
}

function updateRecentSearchesUI() {
    const recentSearches = getRecentSearches();
    const recentList = document.getElementById('recentSearchesList');
    
    recentList.innerHTML = '';
    
    recentSearches.forEach(city => {
        const item = document.createElement('div');
        item.className = 'recent-item';
        item.textContent = city;
        item.addEventListener('click', () => {
            cityInput.value = city;
            getWeatherData(city);
        });
        recentList.appendChild(item);
    });
}

// Temperature conversion utility function (demonstrating return values)
function convertCelsiusToFahrenheit(celsius) {
    return (celsius * 9/5) + 32;
}

function convertFahrenheitToCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5/9;
}

// Weather description formatter (demonstrating string manipulation)
function formatWeatherDescription(description) {
    return description
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);

// Export functions for testing (in a real module system)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        convertCelsiusToFahrenheit,
        convertFahrenheitToCelsius,
        formatWeatherDescription,
        updateWeatherIcon
    };
}