const selectTime = document.getElementById('select_time');
const customTimeInputs = document.querySelectorAll('.custom-time');
const submitBtn = document.getElementById('submitBtn');
const cve_id = document.getElementById('cve_id');
let lastClickTime = 0;
const clickInterval = 5000; // 限制两次点击之间的间隔为5秒
const frequencyLimitMessage = document.getElementById('frequency-limit-message');
let isRequesting = false;
let isFrequencyLimited = false;

$.fn.dataTable.ext.type.order['severity'] = function (data) {
console.log('Data before sorting:', data);
console.log('Data type:', typeof data);
switch (data.toLowerCase()) {
    case 'critical':
        return 1;
    case 'high':
        return 2;
    case 'medium':
        return 3;
    case 'low':
        return 4;
    default:
        return 5;
}
};
selectTime.addEventListener('change', function() {
    const selectedValue = this.value;

    if (selectedValue === 'custom') {
        customTimeInputs.forEach(function(input) {
            input.style.display = 'block';
        });
    } else {
        customTimeInputs.forEach(function(input) {
            input.style.display = 'none';
        });
    }
});
$(document).ready(function() {
const table = $('#table').DataTable({
    columns: [
        { data: 'id' },
        { data: 'descriptions' },
        { data: 'baseSeverity' },
        { data: 'privilegesRequired'},
        { data: 'published' },
        { data: 'lastModified' },
    ],
    columnDefs: [  {
            targets: 1, // 'descriptions' 列的索引
            width: '40%' // 设置 'descriptions' 列的宽度为 30%
        },{
        type: 'severity',
        targets: 2
    }],
    paging: true, // 启用分页
    pageLength: 10 // 每页行数
});


submitBtn.addEventListener('click', function() {
 if (isRequesting) {
    alert('上一个请求还在处理中，请等待...');
    return;
}

if (isFrequencyLimited) {
    alert('点击太频繁，请稍后再试...');
    return;
}

isRequesting = true;

    const selectedValue = selectTime.value;
    const cve_idValue = cve_id.value;
    let startDate, endDate, cveid;

    if (selectedValue === '1') {
        // 设置日期范围为最近一天
        const currentDate = new Date();
        const yesterday = new Date(currentDate);
        yesterday.setDate(yesterday.getDate() - 1);
        startDate = formatDate(yesterday);
        endDate = formatDate(currentDate);
    } else if (selectedValue === 'custom') {
        // 获取自定义日期范围
        const startDateInput = document.getElementById('start_date');
        const endDateInput = document.getElementById('end_date');
        startDate = startDateInput.value;
        endDate = endDateInput.value;
    } else if (selectedValue == '7'){
         const currentDate = new Date();
        const tempday = new Date(currentDate);
        tempday.setDate(tempday.getDate() - 7);
        startDate = formatDate(tempday);
        endDate = formatDate(currentDate);
    }else if (selectedValue == '3'){
         const currentDate = new Date();
        const tempday = new Date(currentDate);
        tempday.setDate(tempday.getDate() - 3);
        startDate = formatDate(tempday);
        endDate = formatDate(currentDate);
    }else if (selectedValue == '30'){
         const currentDate = new Date();
        const tempday = new Date(currentDate);
        tempday.setDate(tempday.getDate() - 30);
        startDate = formatDate(tempday);
        endDate = formatDate(currentDate);
    }



    cveid = cve_id.value;
    // 构造请求数据对象
    const requestData = {
        startDate: startDate,
        endDate: endDate,
        cveid: cveid,
        // 添加其他提交条件的数据
    };


    // 发送AJAX请求
    const xhr = new XMLHttpRequest();
    const url = 'commit'; // 替换为您的后端URL

    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        isRequesting = false;
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);

            // 更新表格数据
            table.clear().draw();
            table.rows.add(response).draw();
        } else {
            console.error('请求失败');
            if (xhr.status === 500) {

            alert('An error occurred. Please try again later.');

            }
        }

    alert(''); // 清空当前 alert 队列，确保下一个 alert 不会被延迟弹出
    };
    xhr.onerror = function() {
        isRequesting = false;
        alert('网络错误发生时');
        // 处理网络错误，显示网络错误消息或执行其他操作
    };
    xhr.send(JSON.stringify(requestData));
    isFrequencyLimited = true;
        setTimeout(() => {
            isFrequencyLimited = false;
        }, 10000);
    });
});


function formatDate(date) {
    const year = date.getUTCFullYear();
const month = (date.getUTCMonth() + 1).toString().padStart(2, '0');
const day = date.getUTCDate().toString().padStart(2, '0');
const hours = date.getUTCHours().toString().padStart(2, '0');
const minutes = date.getUTCMinutes().toString().padStart(2, '0');
const seconds = date.getUTCSeconds().toString().padStart(2, '0');
return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}Z`;
}
