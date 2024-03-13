function fetchDataAndUpdate() {
  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
          console.log("11111111")
          const data = JSON.parse(xhr.responseText);
          let dataContainer = document.getElementById('data-container');
          console.log(document.getElementById('data-container'));
          if (dataContainer) {
          dataContainer.innerHTML = ''; // 清空容器
          }
          else {
          console.error('dataContainer element not found');
          }

          let updateElement = document.getElementById('items');
          let update_ul_Element = document.getElementById('update');
          const today = new Date();
          const year = today.getFullYear();
          const month = (today.getMonth() + 1).toString().padStart(2, '0');
          const day = today.getDate().toString().padStart(2, '0');
          const formattedDate = `${year}年${month}月${day}日`;
          console.log(formattedDate);
          updateElement.innerHTML = ''
          data.forEach(dataItem => {
              let main = document.createElement('div');
              main.className = 'page';
              dataContainer.appendChild(main);
              let Title = document.createElement('h2');
              Title.className = 'title';
              Title.textContent = dataItem.rss_title;
              main.appendChild(Title);
              let link = document.createElement('a');
              const rssId = dataItem.rss_id;
              const detailUrl = `/article/detail/${rssId}`;  // 构建带有rss_id的URL
              link.href = detailUrl;
              link.target = '_blank';
              link.textContent = '查看更多';
              main.appendChild(link);
              let indexLink = document.createElement('div');
              indexLink.className = 'index_link';


              dataItem.entries.forEach(entry => {
                  const entryDate = entry.date;
                  if (entryDate === formattedDate) {
                      let updateData = document.createElement('li');
                      let dataLink = document.createElement('a');
                      dataLink.href = entry.link;
                      dataLink.target = '_blank';
                      dataLink.textContent = entry.title;
                      updateData.appendChild(dataLink);
                      updateElement.appendChild(updateData);
                      console.log("2222222222");
                      // 创建和添加元素的代码
                    }
                    else{
                    console.log("1111111");
                    }

                  let entryDiv = document.createElement('div');
                  entryDiv.className = 'entry';
                  let entryLink = document.createElement('a');
                  entryLink.href = entry.link;
                  entryLink.target = '_blank';
                  entryLink.textContent = entry.title;
                  entryDiv.appendChild(entryLink);

                  let linkDate = document.createElement('div');
                  linkDate.className = 'link_date';
                  let questionTime = document.createElement('span');
                  questionTime.className = 'question-time';
                  questionTime.textContent = entry.date;
                  linkDate.appendChild(questionTime);

                  indexLink.appendChild(entryDiv);
                  indexLink.appendChild(linkDate);
              });

              main.appendChild(indexLink);
          });
      }
  };

  xhr.open('GET', '/article/get_data', true);
  xhr.send();
}


fetchDataAndUpdate();
setInterval(fetchDataAndUpdate, 60000);
