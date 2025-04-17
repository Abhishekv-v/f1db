// NAVBAR SETUP
const navLinks = document.querySelectorAll(".nav-item");
const sections = document.querySelectorAll(".content-section");

navLinks.forEach(link => {
    link.addEventListener("click", () => {
        // Remove active class from all links
        navLinks.forEach(nav => nav.classList.remove("active"));

        // Hide all sections
        sections.forEach(section => section.classList.add("hidden"));

        // Activate the clicked link
        link.classList.add("active");

        // Show the associated section
        const target = link.getAttribute("data-section");
        document.getElementById(target).classList.remove("hidden");
    });
});


// RENDER TABLE SETUP
function renderTableGeneric(data, tableBodyId, columns, currentPage, rowsPerPage) {
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const tableBody = document.getElementById(tableBodyId);
    tableBody.innerHTML = "";

    const visibleData = data.slice(start, end);
    visibleData.forEach((item, index) => {
        const serialNumber = start + index + 1;

        let row = `<tr><td>${serialNumber}</td>`;
        columns.forEach(col => {
            row += `<td>${item[col]}</td>`;
        });
        row += `</tr>`;

        tableBody.innerHTML += row;
    });
}

// PAGINATION SETUP
function setupPaginationGeneric(data, paginationId, currentPage, rowsPerPage, onPageChange) {
    const pagination = document.getElementById(paginationId);
    const pageCount = Math.ceil(data.length / rowsPerPage);
    pagination.innerHTML = "";

    const createButton = (text, page, disabled = false, active = false) => {
        const btn = document.createElement("button");
        btn.textContent = text;
        if (disabled) btn.disabled = true;
        if (active) btn.classList.add("active");
        btn.onclick = () => onPageChange(page);
        pagination.appendChild(btn);
    };

    createButton("Prev", currentPage - 1, currentPage === 1);

    if (currentPage !== 1) createButton("1", 1);
    else createButton("1", 1, false, true);

    if (currentPage > 4) {
        const dots = document.createElement("span");
        dots.textContent = "...";
        pagination.appendChild(dots);
    }

    for (let i = currentPage - 2; i <= currentPage + 2; i++) {
        if (i > 1 && i < pageCount) {
            createButton(i, i, false, i === currentPage);
        }
    }

    if (currentPage < pageCount - 3) {
        const dots = document.createElement("span");
        dots.textContent = "...";
        pagination.appendChild(dots);
    }

    if (pageCount > 1) {
        if (currentPage === pageCount) createButton(pageCount, pageCount, false, true);
        else createButton(pageCount, pageCount);
    }

    createButton("Next", currentPage + 1, currentPage === pageCount);
}

//DRIVERS TABLE
let driverData = [];
let driverPage = 1;
const rowsPerPage = 20;
const driverColumns = ["driver_name", "nationality", "total_wins", "career_points", "teams"];

function fetchDriverData() {
    fetch("/drivers")
        .then(res => res.json())
        .then(data => {
            driverData = data;
            renderDriverTable();
        });
}
function renderDriverTable() {
    renderTableGeneric(driverData, "tableBodyDrivers", driverColumns, driverPage, rowsPerPage);
    setupPaginationGeneric(driverData, "paginationDrivers", driverPage, rowsPerPage, (page) => {
        driverPage = page;
        renderDriverTable();
    });
}
window.onload = () => {
    fetchDriverData();
};

