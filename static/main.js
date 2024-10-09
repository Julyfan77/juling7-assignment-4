document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    let query = document.getElementById('query').value;
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'query': query
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data received from server:', data);  // 调试信息
        displayResults(data);
        displayChart(data);
    })
    .catch(error => {
        console.error('Error:', error);  // 打印错误信息
    });
});

function displayResults(data) {
    console.log('Executing displayResults');  // 调试信息
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h2>Results</h2>';
    for (let i = 0; i < data.documents.length; i++) {
        let docDiv = document.createElement('div');
        docDiv.innerHTML = `<strong>Document ${data.indices[i]}</strong><p>${data.documents[i]}</p><br><strong>Similarity: ${data.similarities[i]}</strong>`;
        resultsDiv.appendChild(docDiv);
    }
}

function displayChart(data) {
    console.log('Executing displayChart');  // 确认是否执行了这个函数
    const chartCanvas = document.getElementById('similarity-chart');
    const ctx = chartCanvas.getContext('2d');

    // 如果已经有 chart 对象，先销毁它，避免重复绘制
    if (window.myChart) {
        console.log('Destroying previous chart');
        window.myChart.destroy();
    }

    // 检查传入的相似度数据是否正确
    console.log('Similarity data:', data.similarities);
    console.log('Indices:', data.indices);

    // 使用 Chart.js 绘制柱状图
    window.myChart = new Chart(ctx, {
        type: 'bar', // 图表类型为柱状图
        data: {
            labels: data.indices.map(i => `Doc ${i}`),  // 文档编号作为标签
            datasets: [{
                label: 'Document Similarity',  // 数据集标签
                data: data.similarities,  // 相似度作为数据
                backgroundColor: 'rgba(75, 192, 192, 0.2)',  // 背景颜色
                borderColor: 'rgba(75, 192, 192, 1)',  // 边框颜色
                borderWidth: 1  // 边框宽度
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true  // y轴从零开始
                }
            }
        }
    });

    console.log('Chart created successfully');
}

