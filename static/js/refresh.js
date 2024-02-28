
const loader = document.getElementById("loader");
const clickTimeElement = document.getElementById("clickTime");
let clickTime = null;
document.getElementById("myButton").addEventListener("click", function() {
 showLoadingIndicator();
 const clickTime = new Date().toLocaleString();
 localStorage.setItem("lastClickTime", clickTime);
    clickTimeElement.textContent = "上次更新时间：" + clickTime;
    fetch('/article/refresh', { method: 'POST' })
        .then(() => {
            // 函数执行完成
            location.reload();
            console.log("函数执行完成");
            hideLoadingIndicator();
        })
        .catch(error => {
            // 处理错误
            console.error(error);
             hideLoadingIndicator();
        });
});
          window.addEventListener("load", function() {
        const lastClickTime = localStorage.getItem("lastClickTime");
        if (lastClickTime !== null) {
          clickTimeElement.textContent = "上一次更新时间：" + lastClickTime;
        }
      });
 function showLoadingIndicator() {
        loader.style.display = "block";
      }

  function hideLoadingIndicator() {
    loader.style.display = "none";
  }