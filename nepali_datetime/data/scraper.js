// https://nepalipatro.com.np/calendar/yearly/bs/2101
// save in Chrome.Console > Sources > Snippets as js file.
// press Ctrl + Enter to run this script and save data as csv in localstorage.
// This saves the data from current year then go to next year and re press Ctrl + Enter.

const KEY = 'calendar_bs';

let year = location.pathname.split('/');
year = year[year.length - 1];
year = parseInt(year, 10);

const months = document.querySelectorAll('.calendar');
const month_ends = [];
months.forEach(month => {
    const cols = month.querySelectorAll('.year-text');
    const _date = cols[cols.length - 1].textContent;
    month_ends.push(parseInt(_date, 10));
});

const current_data = `${year}, ` + month_ends.join(',');
let data = localStorage.getItem(KEY) || '';
data = data + '\n' + current_data;
localStorage.setItem(KEY, data);

window.location.assign(window.location.href.replace(year, ++year));