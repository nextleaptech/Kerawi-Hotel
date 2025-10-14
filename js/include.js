// Function to include HTML content
function includeHTML() {
    var z, i, elmnt, file, xhttp;
    z = document.getElementsByTagName("*");
    for (i = 0; i < z.length; i++) {
        elmnt = z[i];
        file = elmnt.getAttribute("include-html");
        if (file) {
            xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        elmnt.innerHTML = this.responseText;
                        console.log("Footer loaded successfully");
                    }
                    if (this.status == 404) {
                        elmnt.innerHTML = "Footer file not found. Please check if footer.html exists.";
                        console.error("Footer file not found: " + file);
                    }
                    if (this.status == 0) {
                        elmnt.innerHTML = "Cannot load footer. Please use a local server (http://localhost:8000) instead of opening file directly.";
                        console.error("CORS error: Please use a local server");
                    }
                    elmnt.removeAttribute("include-html");
                    includeHTML();
                }
            }
            xhttp.open("GET", file, true);
            xhttp.send();
            return;
        }
    }
}

// Run the function when page loads
document.addEventListener('DOMContentLoaded', includeHTML);

// Also try to run after a short delay in case DOMContentLoaded already fired
setTimeout(includeHTML, 100);
