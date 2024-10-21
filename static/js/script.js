// OpenWeatherMap API key - replace with your own
const apiKey = 'cf8364130087951494a0a60d9f56e2c9';
const city = 'Ashdod'; // החלף עם העיר הרצויה

async function getWeatherData() {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching weather data:', error.message);
        return null;
    }
}

function getWeatherIcon(weatherData) {
    if (!weatherData || !weatherData.weather || weatherData.weather.length === 0) {
        return '01'; // Default icon for clear sky
    }

    const iconCode = weatherData.weather[0].icon;

    const iconMap = {
        '01d': '01', '01n': '33', '02d': '04', '02n': '35',
        '03d': '07', '03n': '38', '04d': '06', '04n': '36',
        '09d': '18', '09n': '40', '10d': '12', '10n': '39',
        '11d': '15', '11n': '41', '13d': '22', '13n': '44',
        '50d': '11', '50n': '37'
    };

    return iconMap[iconCode] || '01';
}

function getHebrewDescription(englishDescription) {
    const descriptionMap = {
        'clear sky': 'שמיים בהירים',
        'few clouds': 'מעט עננים',
        'scattered clouds': 'עננים מפוזרים',
        'broken clouds': 'עננים מפוזרים',
        'shower rain': 'מטר',
        'rain': 'גשם',
        'thunderstorm': 'סופת רעמים',
        'snow': 'שלג',
        'mist': 'ערפל'
        // הוסף עוד תרגומים לפי הצורך
    };

    return descriptionMap[englishDescription] || englishDescription;
}

async function updateWeather() {
    const weatherData = await getWeatherData();
    if (weatherData && weatherData.weather && weatherData.weather.length > 0) {
        const iconCode = getWeatherIcon(weatherData);
        const iconUrl = `https://developer.accuweather.com/sites/default/files/${iconCode}-s.png`;
        const temperature = Math.round(weatherData.main.temp);
        const hebrewDescription = getHebrewDescription(weatherData.weather[0].description);
        
        const weatherDisplay = document.getElementById('weather-display');
        weatherDisplay.innerHTML = `
            <div class="weather-icon">
                <img src="${iconUrl}" alt="Weather icon">
            </div>
            <div class="weather-temp">${temperature}°C</div>
            <div class="weather-description">${hebrewDescription}</div>
        `;
    } else {
        document.getElementById('weather-display').textContent = 'מידע על מזג האוויר לא זמין';
    }
}

async function fetchIsraeliNews() {
    try {
        const response = await fetch('/get_news');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('שגיאה בטעינת החדשות:', error);
        return [];
    }
}

function displayNews(items) {
    const newsContainer = document.querySelector('#news-container');
    if (!newsContainer) {
        console.error('Element with id "news-container" not found');
        return;
    }
    newsContainer.innerHTML = '';

    // שמירת הכותרות הייחודיות
    const uniqueItems = items.filter((item, index, self) =>
        index === self.findIndex((t) => t.title === item.title)
    );

    uniqueItems.forEach((item) => {
        const div = document.createElement('div');
        div.className = 'news-item';
        const pubDate = new Date(item.pubDate);
        div.innerHTML = `
            <div class="news-title">${item.title}</div>
            <div class="news-date">${pubDate.toLocaleTimeString('he-IL', { hour: '2-digit', minute: '2-digit' })}</div>
        `;
        newsContainer.appendChild(div);
    });

    // כפילת החדשות לאפקט גלילה אינסופי, אבל רק אם יש יותר מפריט אחד
    if (uniqueItems.length > 1) {
        const newsItems = newsContainer.innerHTML;
        newsContainer.innerHTML = newsItems + newsItems;
    }
}

function updateDateTime() {
    const now = new Date();
    const options = { timeZone: 'Asia/Jerusalem' };
    
    const timeString = now.toLocaleTimeString('he-IL', {
        ...options,
        hour: '2-digit',
        minute: '2-digit'
    });

    const dateString = now.toLocaleDateString('he-IL', {
        ...options,
        year: '2-digit',
        month: 'short',
        day: 'numeric'
    });

    const dayOfWeek = now.toLocaleDateString('he-IL', {
        ...options,
        weekday: 'long'
    });

    const dateTimeDisplay = document.getElementById('datetime-display');
    if (dateTimeDisplay) {
        dateTimeDisplay.innerHTML = `
            <div class="date-icon">📅</div>
            <div class="date-info">
                <div class="day-of-week">${dayOfWeek}</div>
                <div class="current-date">${dateString}</div>
            </div>
            <div class="current-time">${timeString}</div>
        `;
    } else {
        console.error('Element with id "datetime-display" not found');
    }
}

function initializeApp() {
    updateDateTime();
    updateWeather();
    fetchIsraeliNews().then(displayNews).catch(error => {
        console.error('Error displaying news:', error);
    });

    // עדכון כל דקה
    setInterval(updateDateTime, 60000);
    setInterval(updateWeather, 900000); // כל 15 דקות
    setInterval(() => fetchIsraeliNews().then(displayNews).catch(error => {
        console.error('Error updating news:', error);
    }), 300000); // כל 5 דקות
}

document.addEventListener('DOMContentLoaded', initializeApp);