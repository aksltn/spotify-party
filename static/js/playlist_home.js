d3.json("/data/playlist_home").then(data => {
     const newDiv = document.createElement("ul");
     data.items.forEach(function (item) {
          let list = document.createElement("li");
          list.innerHTML = `<a href="/playlist/${item.id}/">${item.name}</a>`;
          newDiv.appendChild(list);
     });
     document.body.append(newDiv);
});