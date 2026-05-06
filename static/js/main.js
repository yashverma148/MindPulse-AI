document.addEventListener('DOMContentLoaded', () => {
    // --- State ---
    let isRoastMode = false;
    let timePieChart = null;
    let trendChart = null;
    let chromePieChart = null;
    let currentLogId = null;
    let chromeLoaded = false;
    let streakLoaded = false;

    // --- DOM Elements ---
    const roastToggleBtn = document.getElementById('roast-toggle-btn');
    const roastToggle = document.getElementById('roast-toggle');
    const roastIndicator = document.getElementById('roast-indicator');
    const activityForm = document.getElementById('activity-form');
    const submitBtn = document.getElementById('submit-btn');
    const scoreCircle = document.getElementById('score-circle');
    const scoreText = document.getElementById('score-text');
    const scoreStatusText = document.getElementById('score-status-text');
    const insightsContent = document.getElementById('insights-content');
    const aiLoading = document.getElementById('ai-loading');
    const reportsTableBody = document.getElementById('reports-table-body');
    
    // Mobile Sidebar Elements
    const sidebar = document.getElementById('sidebar');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileOverlay = document.getElementById('mobile-overlay');

    // Tab Elements
    const tabLinks = document.querySelectorAll('.nav-link');
    const tabContents = document.querySelectorAll('.tab-content');

    // Sliders and Values
    const sliders = {
        study: { input: document.getElementById('study-slider'), val: document.getElementById('study-val'), label: 'Study' },
        work: { input: document.getElementById('work-slider'), val: document.getElementById('work-val'), label: 'Work' },
        screen: { input: document.getElementById('screen-slider'), val: document.getElementById('screen-val'), label: 'Screen' },
        distraction: { input: document.getElementById('distraction-slider'), val: document.getElementById('distraction-val'), label: 'Distractions' },
        sleep: { input: document.getElementById('sleep-slider'), val: document.getElementById('sleep-val'), label: 'Sleep' }
    };

    // --- Init ---
    if(activityForm) {
        initSliders();
        initCharts();
        fetchHistory();
    }

    // --- Tab Switching Logic ---
    tabLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-target');
            
            // Update active link styling
            tabLinks.forEach(l => {
                l.classList.remove('bg-primary/20', 'text-white', 'border-primary/30');
                l.classList.add('text-gray-400', 'border-transparent');
            });
            link.classList.remove('text-gray-400', 'border-transparent');
            link.classList.add('bg-primary/20', 'text-white', 'border-primary/30');

            // Show target content
            tabContents.forEach(content => {
                content.classList.remove('block');
                content.classList.add('hidden');
            });
            document.getElementById('tab-' + targetId).classList.remove('hidden');
            document.getElementById('tab-' + targetId).classList.add('block');

            // Auto-load data when tab is opened
            if (targetId === 'chrome') {
                if (!chromeLoaded) {
                    loadChromeHistory();
                } else {
                    loadChromeHistory(true); // silent refresh
                }
                
                // Start auto-refresh polling every 5 seconds
                if (!window.chromeSyncInterval) {
                    window.chromeSyncInterval = setInterval(() => {
                        loadChromeHistory(true);
                    }, 5000);
                }
            } else {
                // Clear interval when switching away from chrome tab
                if (window.chromeSyncInterval) {
                    clearInterval(window.chromeSyncInterval);
                    window.chromeSyncInterval = null;
                }
            }
            
            if (targetId === 'streaks' && !streakLoaded) {
                loadStreakData();
            }

            // Close sidebar on mobile after clicking a link
            if (window.innerWidth < 768 && sidebar) {
                sidebar.classList.add('-translate-x-full');
                mobileOverlay.classList.add('hidden', 'opacity-0');
            }
        });
    });

    // --- Event Listeners ---
    // Mobile Sidebar Toggle
    if (mobileMenuBtn && sidebar && mobileOverlay) {
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.remove('-translate-x-full');
            mobileOverlay.classList.remove('hidden');
            // Small delay to allow display:block to apply before animating opacity
            setTimeout(() => {
                mobileOverlay.classList.remove('opacity-0');
            }, 10);
        });

        mobileOverlay.addEventListener('click', () => {
            sidebar.classList.add('-translate-x-full');
            mobileOverlay.classList.add('opacity-0');
            setTimeout(() => {
                mobileOverlay.classList.add('hidden');
            }, 300); // match transition duration
        });
    }

    if (roastToggleBtn) {
        roastToggleBtn.addEventListener('click', () => {
            isRoastMode = !isRoastMode;
            if (isRoastMode) {
                roastToggle.classList.replace('bg-slate-700', 'bg-orange-500');
                roastIndicator.classList.add('translate-x-4');
                roastToggleBtn.classList.add('border-orange-500/50', 'bg-orange-500/10');
            } else {
                roastToggle.classList.replace('bg-orange-500', 'bg-slate-700');
                roastIndicator.classList.remove('translate-x-4');
                roastToggleBtn.classList.remove('border-orange-500/50', 'bg-orange-500/10');
            }
        });
    }

    if (activityForm) {
        activityForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const payload = {
                study_hours: parseFloat(sliders.study.input.value),
                work_hours: parseFloat(sliders.work.input.value),
                screen_time: parseFloat(sliders.screen.input.value),
                distraction_time: parseFloat(sliders.distraction.input.value),
                sleep_hours: parseFloat(sliders.sleep.input.value)
            };

            setLoading(true);

            try {
                // Predict Score
                const predictRes = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                if (!predictRes.ok) throw new Error('Prediction failed');
                const predictData = await predictRes.json();
                currentLogId = predictData.log_id;
                
                updateScoreUI(predictData.score);
                updatePieChart(payload);
                fetchHistory(); // Refresh history for trend and reports

                // Move to Insights Tab automatically
                document.querySelector('[data-target="insights"]').click();

                // Generate Insights
                const insightsRes = await fetch('/insights', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        log_id: currentLogId,
                        roast_mode: isRoastMode
                    })
                });

                if (!insightsRes.ok) throw new Error('Insights failed');
                const insightsData = await insightsRes.json();
                
                renderInsights(insightsData);
                
            } catch (error) {
                console.error(error);
                showToast('Error generating analysis.', 'danger');
                document.querySelector('[data-target="dashboard"]').click();
            } finally {
                setLoading(false);
            }
        });
    }

    // --- Functions ---
    function initSliders() {
        Object.values(sliders).forEach(s => {
            if(!s.input) return;
            s.input.addEventListener('input', (e) => {
                s.val.textContent = `${e.target.value}h`;
                
                if(timePieChart) {
                    updatePieChart({
                        study_hours: parseFloat(sliders.study.input.value),
                        work_hours: parseFloat(sliders.work.input.value),
                        screen_time: parseFloat(sliders.screen.input.value),
                        distraction_time: parseFloat(sliders.distraction.input.value),
                        sleep_hours: parseFloat(sliders.sleep.input.value)
                    });
                }
            });
        });
    }

    function setLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing...';
            submitBtn.classList.add('opacity-70', 'cursor-not-allowed');
            aiLoading.classList.remove('hidden');
            
            insightsContent.innerHTML = `
                <div class="space-y-4">
                    <div class="skeleton h-4 w-3/4 rounded bg-slate-800"></div>
                    <div class="skeleton h-4 w-full rounded bg-slate-800"></div>
                    <div class="skeleton h-4 w-5/6 rounded bg-slate-800"></div>
                    <div class="mt-6 skeleton h-20 w-full rounded-xl bg-slate-800"></div>
                </div>
            `;
        } else {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Generate Analysis';
            submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
            aiLoading.classList.add('hidden');
        }
    }

    function updateScoreUI(score) {
        let start = 0;
        const duration = 1500;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentScore = start + (score - start) * easeOut;
            
            scoreText.textContent = Math.round(currentScore);
            
            let color = '#ef4444';
            let status = 'Needs Improvement';
            let statusColor = 'text-red-400';
            
            if (currentScore >= 75) {
                color = '#22c55e';
                status = 'Excellent';
                statusColor = 'text-green-400';
            } else if (currentScore >= 50) {
                color = '#eab308';
                status = 'Good';
                statusColor = 'text-yellow-400';
            }
            
            scoreCircle.style.background = `conic-gradient(${color} ${currentScore}%, #1e293b ${currentScore}%)`;
            scoreCircle.style.boxShadow = `0 0 20px ${color}33`;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                scoreStatusText.textContent = status;
                scoreStatusText.className = `mt-4 text-sm font-medium ${statusColor}`;
            }
        };
        
        requestAnimationFrame(animate);
    }

    function renderInsights(data) {
        const template = document.getElementById('insights-template').content.cloneNode(true);
        
        template.querySelector('.ai-summary').textContent = data.summary;
        template.querySelector('.ai-behavior').textContent = data.behavioral_analysis;
        
        const suggestionsList = template.querySelector('.ai-suggestions');
        data.suggestions.forEach(s => {
            const li = document.createElement('li');
            li.className = 'flex items-start gap-3 bg-slate-800/50 p-3 rounded-lg border border-slate-700/50';
            li.innerHTML = `<i class="fa-solid fa-check-circle text-green-500 mt-0.5"></i> <span class="text-gray-300 text-sm leading-snug">${s}</span>`;
            suggestionsList.appendChild(li);
        });

        const roastContainer = template.querySelector('#roast-container');
        if (isRoastMode && data.roast) {
            roastContainer.classList.remove('hidden');
            template.querySelector('.ai-roast').textContent = `"${data.roast}"`;
        }

        insightsContent.innerHTML = '';
        insightsContent.appendChild(template);
    }

    function initCharts() {
        const pieCtx = document.getElementById('timePieChart')?.getContext('2d');
        if (pieCtx) {
            Chart.defaults.color = '#94a3b8';
            Chart.defaults.font.family = "'Inter', sans-serif";
            
            timePieChart = new Chart(pieCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Study', 'Work', 'Screen', 'Distractions', 'Sleep'],
                    datasets: [{
                        data: [0, 0, 0, 0, 8],
                        backgroundColor: [
                            '#8b5cf6', '#3b82f6', '#ec4899', '#ef4444', '#10b981'
                        ],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { padding: 15, usePointStyle: true, boxWidth: 8 } }
                    },
                    cutout: '70%'
                }
            });
        }

        const trendCtx = document.getElementById('trendChart')?.getContext('2d');
        if (trendCtx) {
            trendChart = new Chart(trendCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Productivity Score',
                        data: [],
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#0f172a',
                        pointBorderColor: '#8b5cf6',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false } },
                        x: { grid: { display: false, drawBorder: false } }
                    },
                    plugins: { legend: { display: false } }
                }
            });
        }
    }

    function updatePieChart(data) {
        if (!timePieChart) return;
        timePieChart.data.datasets[0].data = [
            data.study_hours, data.work_hours, data.screen_time, data.distraction_time, data.sleep_hours
        ];
        timePieChart.update();
    }

    async function fetchHistory() {
        try {
            const res = await fetch('/history');
            if (res.ok) {
                const data = await res.json();
                
                // Update Trend Chart
                if (trendChart) {
                    const labels = data.map(d => {
                        const date = new Date(d.date);
                        return `${date.getMonth()+1}/${date.getDate()}`;
                    });
                    const scores = data.map(d => d.score);
                    
                    trendChart.data.labels = labels;
                    trendChart.data.datasets[0].data = scores;
                    trendChart.update();
                }

                // Update Reports Table
                if (reportsTableBody) {
                    reportsTableBody.innerHTML = '';
                    if (data.length === 0) {
                        reportsTableBody.innerHTML = '<tr><td colspan="5" class="text-center py-8 text-gray-500 italic">No logs found yet. Log activity to see records.</td></tr>';
                    } else {
                        data.forEach(d => {
                            const tr = document.createElement('tr');
                            tr.className = 'border-b border-glassBorder hover:bg-slate-800/30 transition-colors';
                            
                            let statusColor = 'text-red-400';
                            let statusText = 'Needs Imp.';
                            if(d.score >= 75) { statusColor = 'text-green-400'; statusText = 'Excellent'; }
                            else if(d.score >= 50) { statusColor = 'text-yellow-400'; statusText = 'Good'; }

                            tr.innerHTML = `
                                <td class="py-3 px-4 text-gray-300">${d.date}</td>
                                <td class="py-3 px-4 text-center font-bold text-white">${Math.round(d.score)}</td>
                                <td class="py-3 px-4 text-blue-400">${d.productive_time}</td>
                                <td class="py-3 px-4 text-red-400">${d.distraction_time}</td>
                                <td class="py-3 px-4 font-medium ${statusColor}">${statusText}</td>
                            `;
                            reportsTableBody.appendChild(tr);
                        });
                    }
                }
            }
        } catch (e) {
            console.error('Failed to fetch history', e);
        }
    }

    window.showToast = function(message, type = 'default') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        let classes = 'toast-message px-4 py-3 rounded-xl border shadow-lg backdrop-blur-md animate-slide-in text-sm font-medium ';
        if (type === 'success') classes += 'bg-green-500/10 text-green-400 border-green-500/20';
        else if (type === 'danger') classes += 'bg-red-500/10 text-red-400 border-red-500/20';
        else classes += 'bg-glass text-gray-200 border-glassBorder';
        
        toast.className = classes;
        toast.textContent = message;
        
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    };

    // Clear all activity logs
    window.clearAllLogs = async function() {
        if (!confirm('Are you sure? This will permanently delete ALL your activity logs.')) return;
        
        try {
            const res = await fetch('/clear-logs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            if (res.ok) {
                showToast('All activity logs cleared successfully!', 'success');
                
                if (trendChart) {
                    trendChart.data.labels = [];
                    trendChart.data.datasets[0].data = [];
                    trendChart.update();
                }
                if (reportsTableBody) {
                    reportsTableBody.innerHTML = '<tr><td colspan="5" class="text-center py-8 text-gray-500 italic">No logs found yet. Log activity to see records.</td></tr>';
                }
                scoreText.textContent = '--';
                scoreCircle.style.background = '';
                scoreCircle.style.boxShadow = '';
                scoreStatusText.textContent = 'Awaiting data...';
                scoreStatusText.className = 'mt-4 text-sm font-medium text-gray-400';
                streakLoaded = false;
            } else {
                showToast('Failed to clear logs.', 'danger');
            }
        } catch (e) {
            console.error(e);
            showToast('Error clearing logs.', 'danger');
        }
    };

    // --- BROWSER EXTENSION INTEGRATION ---
    window.generateBrowserToken = async function() {
        try {
            const res = await fetch('/api/browser-token/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await res.json();
            if (data.success) {
                document.getElementById('raw-token-display').textContent = data.token;
                document.getElementById('token-display-area').classList.remove('hidden');
                document.getElementById('btn-revoke-token').classList.remove('hidden');
                showToast('Token generated successfully!', 'success');
            } else {
                showToast(data.error || 'Failed to generate token', 'danger');
            }
        } catch (e) {
            console.error(e);
            showToast('Error generating token', 'danger');
        }
    };

    window.revokeBrowserToken = async function() {
        if (!confirm('Revoke your active sync token? Your browser extension will stop working until you generate a new one.')) return;
        try {
            const res = await fetch('/api/browser-token/revoke', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await res.json();
            if (data.success) {
                document.getElementById('token-display-area').classList.add('hidden');
                document.getElementById('btn-revoke-token').classList.add('hidden');
                showToast('Token revoked successfully.', 'success');
            } else {
                showToast(data.error || 'Failed to revoke token', 'danger');
            }
        } catch (e) {
            console.error(e);
            showToast('Error revoking token', 'danger');
        }
    };

    window.copyToken = function() {
        const tokenText = document.getElementById('raw-token-display').textContent;
        navigator.clipboard.writeText(tokenText).then(() => {
            showToast('Token copied to clipboard!', 'success');
        }).catch(err => {
            showToast('Failed to copy token', 'danger');
            console.error('Could not copy text: ', err);
        });
    };

    // --- CHROME HISTORY ANALYSIS ---
    window.loadChromeHistory = async function(isSilent = false) {
        const hoursSelect = document.getElementById('chrome-hours');
        const hours = hoursSelect ? hoursSelect.value : 24;
        const topSitesContainer = document.getElementById('chrome-top-sites');
        const errorContainer = document.getElementById('chrome-error');
        const errorMsg = document.getElementById('chrome-error-msg');
        const emptyState = document.getElementById('chrome-empty-state');

        if (!isSilent) {
            topSitesContainer.innerHTML = '<div class="skeleton h-6 w-full rounded mb-2"></div>'.repeat(5);
        }
        errorContainer.classList.add('hidden');
        if (emptyState) emptyState.classList.add('hidden');

        try {
            const res = await fetch(`/api/browser-history/analytics?hours=${hours}`);
            const data = await res.json();

            if (data.error) {
                errorContainer.classList.remove('hidden');
                errorMsg.textContent = data.error;
                return;
            }

            if (data.summary.total_visits === 0) {
                if (emptyState) emptyState.classList.remove('hidden');
                document.getElementById('chrome-productive').textContent = '0';
                document.getElementById('chrome-distraction').textContent = '0';
                document.getElementById('chrome-total').textContent = '0';
                topSitesContainer.innerHTML = '<p class="text-gray-500 text-sm italic text-center py-6">No data synced yet.</p>';
                if (chromePieChart) chromePieChart.destroy();
                return;
            }

            // Update stats
            document.getElementById('chrome-productive').textContent = data.summary.productive_count;
            document.getElementById('chrome-distraction').textContent = data.summary.distraction_count;
            document.getElementById('chrome-total').textContent = data.summary.total_visits;

            // Render Top Sites
            if (data.top_sites.length === 0) {
                topSitesContainer.innerHTML = '<p class="text-gray-500 text-sm italic text-center py-6">No browsing history found for this period.</p>';
            } else {
                topSitesContainer.innerHTML = '';
                data.top_sites.forEach((site, i) => {
                    let typeColor = 'text-gray-400';
                    let typeBg = 'bg-slate-700';
                    let typeIcon = 'fa-globe';
                    if (site.category === 'productive') {
                        typeColor = 'text-green-400'; typeBg = 'bg-green-500/10'; typeIcon = 'fa-check';
                    } else if (site.category === 'distraction') {
                        typeColor = 'text-red-400'; typeBg = 'bg-red-500/10'; typeIcon = 'fa-skull';
                    }

                    const div = document.createElement('div');
                    div.className = `flex items-center gap-3 p-3 rounded-lg ${typeBg} border border-slate-700/50 hover:border-slate-600/50 transition-colors`;
                    div.innerHTML = `
                        <span class="text-xs text-gray-500 w-5 text-center">${i + 1}</span>
                        <i class="fa-solid ${typeIcon} ${typeColor} text-xs"></i>
                        <span class="text-sm text-gray-200 flex-1 truncate">${site.domain}</span>
                        <span class="text-xs font-bold ${typeColor}">${site.visits} visits</span>
                    `;
                    topSitesContainer.appendChild(div);
                });
            }

            // Update Chrome Pie Chart
            const chromePieCtx = document.getElementById('chromePieChart')?.getContext('2d');
            if (chromePieCtx) {
                if (chromePieChart) chromePieChart.destroy();
                chromePieChart = new Chart(chromePieCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Productive', 'Distraction', 'Neutral'],
                        datasets: [{
                            data: [data.category_breakdown.productive, data.category_breakdown.distraction, data.category_breakdown.neutral],
                            backgroundColor: ['#22c55e', '#ef4444', '#6366f1'],
                            borderWidth: 0, hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        cutout: '65%',
                        plugins: { legend: { position: 'bottom', labels: { padding: 15, usePointStyle: true, boxWidth: 8 } } }
                    }
                });
            }

            chromeLoaded = true;
        } catch (e) {
            console.error('Chrome history error:', e);
            errorContainer.classList.remove('hidden');
            errorMsg.textContent = 'Failed to load browser analytics.';
        }
    };

    // --- HABIT STREAKS ---
    async function loadStreakData() {
        try {
            const res = await fetch('/streak');
            const data = await res.json();

            document.getElementById('streak-current').textContent = data.current_streak;
            document.getElementById('streak-longest').textContent = data.longest_streak;
            document.getElementById('streak-total').textContent = data.total_logs;
            document.getElementById('streak-avg').textContent = data.avg_score;

            // Render Heatmap
            renderHeatmap(data.heatmap);
            streakLoaded = true;
        } catch (e) {
            console.error('Streak data error:', e);
        }
    }

    function renderHeatmap(heatmapData) {
        const container = document.getElementById('heatmap-container');
        if (!container) return;
        container.innerHTML = '';

        const today = new Date();
        const days = 90;

        for (let i = days - 1; i >= 0; i--) {
            const d = new Date(today);
            d.setDate(today.getDate() - i);
            const dateStr = d.toISOString().split('T')[0];
            const score = heatmapData[dateStr];

            const cell = document.createElement('div');
            cell.className = 'w-3 h-3 rounded-sm transition-colors cursor-pointer';
            cell.title = `${dateStr}: ${score ? 'Score ' + score : 'No log'}`;

            if (score === undefined) {
                cell.classList.add('bg-slate-800', 'border', 'border-slate-700');
            } else if (score >= 75) {
                cell.classList.add('bg-green-400');
            } else if (score >= 50) {
                cell.classList.add('bg-green-500');
            } else if (score >= 25) {
                cell.classList.add('bg-green-700');
            } else {
                cell.classList.add('bg-green-900');
            }

            container.appendChild(cell);
        }
    }
});
