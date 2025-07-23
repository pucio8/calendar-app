/*
Setup variables:
- monthSelect,
- yearSelect,
- eventTypeSelect,
- calendarGrid,
- dayHeadersGrid,
- statusDiv,
*/
const monthSelect = document.getElementById("month-select");
const yearSelect = document.getElementById("year-select");
const eventTypeSelect = document.getElementById("event-type-select");
const calendarGrid = document.getElementById("calendar-grid");
const dayHeadersGrid = document.getElementById("day-headers");
const statusDiv = document.getElementById("status");

// new map for selected events
let selectedEvents = new Map();
// colors for shifts (3 colors)
const shiftColors = ["shift-1", "shift-2", "shift-3"];
// event types (5 types)
const eventTypes = ["duty", "duty_off", "delegation", "training", "blood"];

/*
 * Reference date from which the shift cycle is calculated.
 * We set a date that is known to be a "Shift 3" day.
 */
const epochDate = new Date("2024-01-03");

/**
 * @description
 * Generates and displays the calendar grid for a given month and year.
 * @param {number} year - The year for which the calendar should be generated (e.g., 2025).
 * @param {number} month- The month for which the calendar should be generated (0-11).
 */
function generateCalendar(year, month) {
  // Clears the previous grid and selected events
  calendarGrid.innerHTML = "";
  selectedEvents.clear(); // Date calculations
  const date = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const startDay = (date.getDay() + 6) % 7; // 0 = Poniedziałek (Monday)

  for (let i = 0; i < startDay; i++) {
    calendarGrid.innerHTML += `<div class="day empty"></div>`;
  } // Adds the actual days of the month

  for (let i = 1; i <= daysInMonth; i++) {
    const dayDiv = document.createElement("div");
    dayDiv.className = "day";
    dayDiv.textContent = i;


    // Coloring logic based on the reference date
    const currentDate = new Date(year, month, i);
    // Calculate the difference in milliseconds
    const diffInMs = currentDate - epochDate;
    // Convert milliseconds to days
    const totalDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
    // Use the modulo operator to find the correct color in the 3-day cycle
    const colorIndex = Math.abs(totalDays) % shiftColors.length;
    dayDiv.classList.add(shiftColors[colorIndex]);

    const dateString = `${year}-${String(month + 1).padStart(2, "0")}-${String(
      i
    ).padStart(2, "0")}`;
    dayDiv.onclick = () => toggleDay(dayDiv, dateString);
    calendarGrid.appendChild(dayDiv);
  }
}

/**
 * @description
 * Toggles the selection state for a day cell. It handles selecting, deselecting, and changing the type of an already selected day.
 * @param {HTMLElement} dayDiv - The div element of the day cell that was clicked.
 * @param {string} dateString- The date of the cell in "YYYY-MM-DD" format.
 */
function toggleDay(dayDiv, dateString) {
  // Get the current event type from the select element
  const currentEventType = eventTypeSelect.value;
  // Check if the day is already selected
  const wasSelected = selectedEvents.has(dateString);
  // Get the previous event type of the day
  const previousEventType = selectedEvents.get(dateString);

  // Remove all event type classes from the day cell
  eventTypes.forEach((type) => dayDiv.classList.remove(type));

  // Decide what to do: deselect, or select/change.
  if (wasSelected && previousEventType === currentEventType) {
    selectedEvents.delete(dateString);
  } else {
    selectedEvents.set(dateString, currentEventType);
    dayDiv.classList.add(currentEventType);
  }
}

/**
 * @description
 * Changes the displayed month by the given offset.
 * @param {number} offset - The number of months to shift (-1 for previous, 1 for next).
 */
function changeMonth(offset) {
  // Get the current month and year from the select elements
  let currentMonth = parseInt(monthSelect.value);
  let currentYear = parseInt(yearSelect.value);
  // Change the month by the given offset
  currentMonth += offset;
  // If the month is greater than 11, set it to 0 and increment the year
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
    // If the month is less than 0, set it to 11 and decrement the year
  } else if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  // If the year is not in the select options, add it
  if (!Array.from(yearSelect.options).some((opt) => opt.value == currentYear)) {
    const option = new Option(currentYear, currentYear);
    // If the offset is positive, add the year to the end of the select options
    if (offset > 0) {
      yearSelect.add(option);
    } else {
      // If the offset is negative, add the year to the beginning of the select options
      yearSelect.add(option, 0);
    }
  }
  // Set the month and year in the select elements
  monthSelect.value = currentMonth;
  yearSelect.value = currentYear;
  // Generate the calendar for the new month and year
  generateCalendar(currentYear, currentMonth);
}

/**
 * @description
 * Changes the displayed month to the previous month.
 */
function previousMonth() {
  changeMonth(-1);
}

/**
 * @description
 * Changes the displayed month to the next month.
 */
function nextMonth() {
  changeMonth(1);
}

/**
 * @description
 * Submits the selected events to the server.
 */
async function submitEvents() {
  // If no events are selected, show an error message
  if (selectedEvents.size === 0) {
    statusDiv.textContent = "Proszę wybrać przynajmniej jeden dzień.";
    statusDiv.style.color = "red";
    return;
  }
  // Show a loading message
  statusDiv.textContent = "Dodawanie wydarzeń...";
  statusDiv.style.color = "orange";

  // Create a payload for the request
  const payload = {
    events: Array.from(selectedEvents.entries()).map(([date, type]) => ({
      date,
      type,
    })),
  };

  // Send the request to the server
  try {
    const response = await fetch("/api/add-events", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    // If the request is successful, show a success message
    if (response.ok) {
      statusDiv.textContent = result.message;
      statusDiv.style.color = "green"; // Change the color of the status message to green
      if (result.redirect_url) {
        // If the server returns a redirect URL, redirect to it after 1.5 seconds
        setTimeout(() => {
          window.location.href = result.redirect_url;
        }, 1500);
      }
    } else {
      // If the request is not successful, show an error message
      throw new Error(result.detail || "Wystąpił nieznany błąd.");
    }
  } catch (error) {
    // If an error occurs, show an error message
    statusDiv.textContent = `Błąd: ${error.message}`;
    statusDiv.style.color = "red";
  }
}

/**
 * @description
 * Sets up the controls for the calendar.
 */
function setupControls() {
  // Fill months select options (12 months)
  const months = [
    "Styczeń",
    "Luty",
    "Marzec",
    "Kwiecień",
    "Maj",
    "Czerwiec",
    "Lipiec",
    "Sierpień",
    "Wrzesień",
    "Październik",
    "Listopad",
    "Grudzień",
  ];
  months.forEach((month, index) => monthSelect.add(new Option(month, index)));
  // Fill years select options (current year and 2 years before and after)
  const currentYear = new Date().getFullYear();
  for (let i = currentYear - 2; i <= currentYear + 2; i++)
    yearSelect.add(new Option(i, i));
  // Header. Setup day of week
  const dayHeaders = ["Pn", "Wt", "Śr", "Cz", "Pt", "So", "Nd"];
  dayHeaders.forEach(
    (header) =>
      (dayHeadersGrid.innerHTML += `<div class="day-header">${header}</div>`)
  );
  // Setup actual month and year select
  monthSelect.value = new Date().getMonth();
  yearSelect.value = currentYear;
  // Set listeners for month and year select
  monthSelect.onchange = () =>
    generateCalendar(parseInt(yearSelect.value), parseInt(monthSelect.value));
  yearSelect.onchange = () =>
    generateCalendar(parseInt(yearSelect.value), parseInt(monthSelect.value));
  // Generate calendar for actual month and year (default)
  generateCalendar(currentYear, new Date().getMonth());
}

/**
 * @description
 * Toggles the menu and changes the hamburger icon to an X.
 * @param {Event} event - The event object.
 */
function toggleMenu(event) {
  // Stop the event from bubbling up
  event.stopPropagation();
  // Toggle the open class on the hamburger menu
  event.currentTarget.classList.toggle("open");
  // Toggle the show class on the dropdown content
  document.getElementById("logout-dropdown").classList.toggle("show");
}

/**
 * @description
 * Hides the menu and changes the hamburger icon to an X when clicking outside of the hamburger menu.
 * @param {Event} event - The event object.
 */
window.onclick = function (event) {
  if (!event.target.closest(".hamburger-menu")) {
    // Get all dropdown content elements
    const dropdowns = document.getElementsByClassName("dropdown-content");
    // Remove the show class from all dropdown content elements
    for (let i = 0; i < dropdowns.length; i++)
      dropdowns[i].classList.remove("show");
    // Get all hamburger icon elements
    const icons = document.getElementsByClassName("hamburger-icon");
    // Remove the open class from all hamburger icon elements
    for (let i = 0; i < icons.length; i++) icons[i].classList.remove("open");
  }
};

/**
 * @description
 * Checks if the user is logged in and shows the calendar and hides the login button.
 * If the user is not logged in, hides the hamburger menu.
 */
window.onload = () => {
  if (document.cookie.includes("google_token_present=true")) {
    document.getElementById("scheduler").style.display = "block";
    document.querySelector(".button-google").style.display = "none";
    document.getElementById("login-prompt").style.display = "none";
    setupControls();
  } else {
    const hamburger = document.querySelector(".hamburger-menu");
    if (hamburger) hamburger.style.display = "none";
  }
};
