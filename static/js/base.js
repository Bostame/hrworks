function updateLiveHours() {
    fetch("/get_live_hours/")  
        .then(response => response.json())
        .then(data => {
            console.log("🔄 Live Hours Updated:", data);

            // ✅ Update Quick Overview Section (Dashboard)
            const quickOverviewHours = document.getElementById("quick-overview-hours");
            if (quickOverviewHours) {
                quickOverviewHours.innerText = data.hours_worked.toFixed(2) + "h";
            }

            // ✅ Update elapsed time display in Time Tracker UI (Navbar)
            const elapsedTimeElement = document.getElementById("elapsed-time");
            if (elapsedTimeElement) {
                elapsedTimeElement.innerText = data.hours_worked.toFixed(2) + "h";
            }

            // ✅ Update "Today's Hours" in the donut chart
            const liveHoursElement = document.getElementById("live-hours");
            if (liveHoursElement) {
                liveHoursElement.innerText = data.hours_worked.toFixed(2) + "h";
            }

            let dailyChart = Chart.getChart("dailyHoursChart");
            if (dailyChart) {
                dailyChart.data.datasets[0].data[0] = data.hours_worked;
                dailyChart.data.datasets[0].data[1] = Math.max(10 - data.hours_worked, 0);
                dailyChart.update();
            }

            // ✅ Update Countdown Timer
            startCountdown(data.remaining_work_seconds, data.clocked_in);

            // ✅ Update Clock-in Button
            const clockButton = document.querySelector(".clock-button");
            if (clockButton) {
                if (data.clocked_in) {
                    clockButton.style.backgroundColor = "#dc3545"; // Red for clocked in
                    clockButton.innerHTML = '<i class="fa fa-pause"></i>';
                } else {
                    clockButton.style.backgroundColor = "#007bff"; // Blue for clocked out
                    clockButton.innerHTML = '<i class="fa fa-play"></i>';
                }
            }
        })
        .catch(error => console.error("❌ Error fetching live hours:", error));
}

function startCountdown(remainingSeconds, clockedIn) {
    const timerElement = document.getElementById("workday-timer");

    if (!clockedIn) {
        if (timerElement) timerElement.innerText = "⏸ Not Clocked In";
        return;
    }

    function updateTimer() {
        if (remainingSeconds > 0) {
            let hours = Math.floor(remainingSeconds / 3600);
            let minutes = Math.floor((remainingSeconds % 3600) / 60);
            if (timerElement) {
                timerElement.innerText = `${hours}h ${minutes}m`;
            }
            remainingSeconds--;
            setTimeout(updateTimer, 1000); // ✅ Smooth countdown
        } else {
            if (timerElement) {
                timerElement.innerText = "✅ Workday Completed!";
            }
        }
    }

    updateTimer();
}

// ✅ Chart.js Integration (Moved from dashboard)
document.addEventListener("DOMContentLoaded", function () {
    try {
        let chartData = JSON.parse(document.getElementById("chart-data").textContent);

        if (!Array.isArray(chartData) || chartData.length === 0) {
            console.warn("No chart data available");
            return;
        }

        function createChart(canvasId, worked, max, color) {
            const ctx = document.getElementById(canvasId);
            if (!ctx) return;

            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: ["Used", "Remaining"],
                    datasets: [{
                        data: [worked, Math.max(max - worked, 0)],
                        backgroundColor: [color, "#ecf0f1"],
                        borderWidth: 1,
                    }],
                },
                options: {
                    cutout: "65%",
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: true },
                    },
                },
            });
        }

        chartData.forEach(chart => {
            createChart(chart.chart_id, chart.worked, chart.max, chart.color);
        });

    } catch (error) {
        console.error("Error parsing chart data:", error);
    }
});

// ✅ Run immediately on page load & every 1 minute
document.addEventListener("DOMContentLoaded", function () {
    updateLiveHours(); 
    setInterval(updateLiveHours, 60000); // Refresh every 1 minute
});