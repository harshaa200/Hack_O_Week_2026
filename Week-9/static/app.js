const API = "http://127.0.0.1:5008/api";

async function loadDashboard() {
    try {
        const stats = await fetch(API + "/stats").then(r => r.json());
        const forecast = await fetch(API + "/forecast").then(r => r.json());
        const historical = await fetch(API + "/historical").then(r => r.json());

        if (!stats.success || !forecast.success || !historical.success) {
            console.error("API error");
            return;
        }

        renderKPI(stats);
        renderForecast(forecast.forecast);
        renderHourly(historical.data);
        renderDaily(historical.data);
        renderSlider(historical.data);

    } catch (err) {
        console.error("Error loading dashboard", err);
    }
}

function renderKPI(stats) {

    const html = `
    <div class="card">
        <h3>Total Records</h3>
        <p>${stats.summary.records}</p>
    </div>

    <div class="card">
        <h3>Average Load</h3>
        <p>${stats.summary.avg_load} kWh</p>
    </div>

    <div class="card">
        <h3>Sunday Avg</h3>
        <p>${stats.summary.sunday_avg} kWh</p>
    </div>

    <div class="card">
        <h3>Naive Bayes Accuracy</h3>
        <p>${stats.nb_accuracy}</p>
    </div>
    `;

    document.getElementById("kpiCards").innerHTML = html;
}

function renderForecast(data) {

    const x = data.map(d => d.ds);
    const y = data.map(d => d.yhat);

    const trace = {
        x: x,
        y: y,
        type: "scatter",
        mode: "lines+markers"
    };

    Plotly.newPlot("forecastChart", [trace]);
}

function renderHourly(data) {

    let hourly = {};

    data.forEach(d => {
        const h = d.hour;
        if (!hourly[h]) hourly[h] = [];
        hourly[h].push(d.load_kwh);
    });

    const x = Object.keys(hourly);
    const y = x.map(h => {
        const arr = hourly[h];
        return arr.reduce((a, b) => a + b) / arr.length;
    });

    const trace = {
        x: x,
        y: y,
        type: "bar"
    };

    Plotly.newPlot("hourlyChart", [trace]);
}

function renderDaily(data) {

    let daily = {};

    data.forEach(d => {
        const day = d.day_of_week;
        if (!daily[day]) daily[day] = [];
        daily[day].push(d.load_kwh);
    });

    const x = Object.keys(daily);
    const y = x.map(d => {
        const arr = daily[d];
        return arr.reduce((a, b) => a + b) / arr.length;
    });

    const trace = {
        x: x,
        y: y,
        type: "bar"
    };

    Plotly.newPlot("dailyChart", [trace]);
}

function renderSlider(data) {
    const x = data.map(d => d.timestamp);
    const y = data.map(d => d.load_kwh);

    const trace = {
        x: x,
        y: y,
        type: "scatter",
        mode: "lines"
    };

    Plotly.newPlot("sliderChart", [trace]);
}

function onSlider(val) {
    document.getElementById("sliderVal").innerText =
        "Showing first " + val + " days";
}

window.onload = loadDashboard;