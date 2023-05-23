// Obtener elementos del DOM
const todayDateElement = document.querySelector(".today-date");
const comidasElement = document.querySelector(".comidas");
const agregarComidaWrapper = document.querySelector(".agregar-comida-wrapper");
const agregarComidaCloseBtn = document.querySelector(".agregar-comida-header i");
const comidaNameInput = document.querySelector(".comida-name");
const comidaTimeFromInput = document.querySelector(".comida-time-from");
const comidaTimeToInput = document.querySelector(".comida-time-to");
const comidaDescripcionInput = document.querySelector(".comida-descripcion");
const comidaIngredientesInput = document.querySelector(".comida-ingredientes");
const comidaMiembroInput = document.querySelector(".comida-miembro");
const comidaExtraInput = document.querySelector(".comida-extra");
const agregarComidaBtn = document.querySelector(".agregar-comida-btn");
const calendar = document.querySelector(".calendar"),
    daysContainer = document.querySelector(".days"),
    prev = document.querySelector(".prev"),
    next = document.querySelector(".next"),
    todayBtn = document.querySelector(".today-btn"),
    gotoBtn = document.querySelector(".goto-btn"),
    dateInput = document.querySelector(".date-input"),
    eventDay = document.querySelector(".comida-day"),
    eventDate = document.querySelector(".comida-date"),
    addEventCloseBtn = document.querySelector(".close ");
 
let today = new Date();
let activeDay;

  
const eventsArr = [];
getEvents();
console.log(eventsArr);
// Obtener la fecha actual
const currentDate = new Date();
const currentDay = currentDate.toLocaleDateString("es-ES", {
  weekday: "long",
});
const currentMonth = currentDate.toLocaleDateString("es-ES", {
  month: "long",
  year: "numeric",
});
const currentDateString = currentDate.toISOString().split("T")[0];

// Mostrar la fecha actual en la interfaz
todayDateElement.querySelector(".comida-day").textContent = currentDay;
todayDateElement.querySelector(".comida-date").textContent = currentDateString;

// Agregar listener al botón para mostrar el formulario de agregar comida
document.querySelector(".agregar-comida").addEventListener("click", () => {
  agregarComidaWrapper.style.display = "block";
});

let month = today.getMonth();
let year = today.getFullYear();

const months = [
  "Enero",
  "Febrero",
  "Marzo",
  "Abril",
  "Mayo",
  "Junio",
  "Julio",
  "Agosto",
  "Septiembre",
  "Octubre",
  "Noviembre",
  "Diciembre",
];

// Agregar listener al botón de cerrar formulario de agregar comida
agregarComidaCloseBtn.addEventListener("click", () => {
  agregarComidaWrapper.style.display = "none";
});

// Función para agregar una comida
function addComida() {
  const name = comidaNameInput.value.trim();
  const timeFrom = comidaTimeFromInput.value.trim();
  const timeTo = comidaTimeToInput.value.trim();
  const descripcion = comidaDescripcionInput.value.trim();
  const ingredientes = comidaIngredientesInput.value.trim();
  const miembro = comidaMiembroInput.value.trim();
  const extra = comidaExtraInput.value.trim();

  if (name !== "" && timeFrom !== "" && timeTo !== "") {
    // Crear el elemento de comida
    const comidaElement = document.createElement("div");
    comidaElement.className = "comida";
    comidaElement.textContent = name;

    // Agregar la comida al contenedor de comidas
    comidasElement.appendChild(comidaElement);

    // Limpiar los campos de entrada
    comidaNameInput.value = "";
    comidaTimeFromInput.value = "";
    comidaTimeToInput.value = "";
    comidaDescripcionInput.value = "";
    comidaIngredientesInput.value = "";
    comidaMiembroInput.value = "";
    comidaExtraInput.value = "";

    // Ocultar el formulario de agregar comida
    agregarComidaWrapper.style.display = "none";
  }
}

// Agregar listener al botón de agregar comida
agregarComidaBtn.addEventListener("click", addComida);

// Obtén el elemento de días del calendario
const daysElement = document.querySelector(".days");

// Generar los elementos de día para el calendario
function generateCalendarDays() {
  // Obtener el primer día del mes actual
  const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
  const firstDayOfWeek = firstDayOfMonth.getDay();

  // Obtener el último día del mes anterior
  const lastDayOfPrevMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 0);
  const lastDayOfPrevMonthDate = lastDayOfPrevMonth.getDate();

  // Obtener el último día del mes actual
  const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
  const lastDayOfMonthDate = lastDayOfMonth.getDate();

  // Calcular los días que se deben mostrar del mes anterior
  const prevDaysCount = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

  // Calcular los días que se deben mostrar del mes siguiente
  const nextDaysCount = 7 - ((prevDaysCount + lastDayOfMonthDate) % 7);

  // Limpiar los días anteriores
  daysElement.innerHTML = "";

  // Generar los días del mes anterior
  for (let i = prevDaysCount; i > 0; i--) {
    const dayElement = document.createElement("div");
    dayElement.classList.add("prev-month-day");
    dayElement.textContent = lastDayOfPrevMonthDate - i + 1;
    daysElement.appendChild(dayElement);
  }

  // Generar los días del mes actual
  for (let i = 1; i <= lastDayOfMonthDate; i++) {
    const dayElement = document.createElement("div");
    dayElement.classList.add("current-month-day");
    dayElement.textContent = i;
    daysElement.appendChild(dayElement);

    // Marcar el día actual
    if (currentDate.getDate() === i) {
      dayElement.classList.add("today");
    }
  }

  // Generar los días del mes siguiente
  for (let i = 1; i <= nextDaysCount; i++) {
    const dayElement = document.createElement("div");
    dayElement.classList.add("next-month-day");
    dayElement.textContent = i;
    daysElement.appendChild(dayElement);
  }
}

// Generar los días del calendario al cargar la página
generateCalendarDays();

// Función para eliminar una comida
function eliminarComida() {
  // Obtener el ID de la comida que se va a eliminar
  const comidaId = this.dataset.comidaId;

  alert("La comida ha sido eliminada");
}

