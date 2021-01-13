d3.json("/data").then(data => {
     const newDiv = document.createElement("ul");
     data.items.forEach(function (item) {
          let list = document.createElement("li");
          list.innerHTML = `<a href=${item.external_urls.spotify}>${item.name}</a>`;
          newDiv.appendChild(list);
     });
     document.body.append(newDiv);
});