const sidebarItems = {
    "Setup": {"Requirements": "/Documentation/about.html", "Authentication": "/Documentation/about.html"},
    "Methods": {"getUser": "./", "getGroup": "./"},
    "Classes": {"User": "/Documentation/Classes/user.html", "Client": "/Documentation/Classes/client.html", "Group": "/Documentation/Classes/group.html", "ThumbnailSize": "/Documentation/Classes/user.html", "ImageFormat": "./"},
};

document.addEventListener("DOMContentLoaded", function(){
    var itemContainer = document.getElementById("sidebar");
    for (var title in sidebarItems){
        var container = document.createElement("a");
        container.className = "sidebutton";
        container.innerHTML = `<h3>${title}</h3>`;
        itemContainer.appendChild(container);
        for (var subclass in sidebarItems[title]){
            var node = document.createElement("a")
            node.className = "sidebutton";
            node.innerHTML = `- ${subclass}`;
            node.href = sidebarItems[title][subclass];
            itemContainer.appendChild(node);
        }

    }
})