// function updateTime() {
//     const now = new Date();
//     const timeString = now.toLocaleTimeString('he-IL', { hour: '2-digit', minute: '2-digit' });
//     const dateString = now.toLocaleDateString('he-IL', { year: 'numeric', month: 'long', day: 'numeric' });
//     document.getElementById('current-time').textContent = `📅  ${dateString}   | 🕐  ${timeString}`;
// }
function updateTime() {
    const now = new Date();
    const options = { 
        timeZone: 'Asia/Jerusalem',
        hour: '2-digit', 
        minute: '2-digit', 
        hour12: false 
    };
    const timeString = now.toLocaleTimeString('he-IL', options);
    
    const hour = now.getHours();
    const isDaytime = hour >= 6 && hour < 18;
    
    const icon = isDaytime 
        ? '<span>☀️</span>'
        : '<span>🌛</span>';
    
    document.getElementById('current-time').innerHTML = `${icon}<span>${timeString}</span>`;
}

updateTime();
setInterval(updateTime, 60000);
updateTime(); // קריאה ראשונית
