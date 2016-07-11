function saveChart() {
    console.log("saving...");
    saveSvgAsPng(document.getElementsByTagName("svg")[0], "chart.png", {backgroundColor: "white"});
}
