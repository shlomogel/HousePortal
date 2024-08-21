const monthYearElement = document.getElementById('monthYear');
const datesElement = document.getElementById('dates');

let currentDate = new Date();

const updateCalendar = () => {
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const totalDays = lastDay.getDate();
    const firstDayIndex = firstDay.getDay();
    const lastDayIndex = lastDay.getDay();
    const prevLastDay = new Date(currentYear, currentMonth, 0).getDate();
    
    monthYearElement.innerHTML = `<h4>${currentDate.toLocaleDateString('he-IL', { month: 'long' })}</h4>`;

    let dateHTML = '';

    // Add the days from the previous month
    for (let i = firstDayIndex; i > 0; i--) {
        dateHTML += `<div class="date inactive"></div>`;
        // dateHTML += `<div class="date inactive">${prevLastDay - i + 1}</div>`;
    }

    // Add the days of the current month
    for (let i = 1; i <= totalDays; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const activeClass = date.toDateString() === new Date().toDateString() ? 'active rounded-circle' : 'active-light';
        dateHTML += `<div class="date ${activeClass}">${i}</div>`;
    }

    // Add the days from the next month
    for (let i = lastDayIndex; i < 6; i++) {
        dateHTML += `<div class="date inactive"></div>`;
        // dateHTML += `<div class="date inactive">${i - lastDayIndex + 1}</div>`;
    }

    datesElement.innerHTML = dateHTML;
};

updateCalendar();
