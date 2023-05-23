// Obtener elementos del DOM
const todayDateElement = document.querySelector(".today-date");
const comidasElement = document.querySelector(".comidas");
const agregarComidaWrapper = document.querySelector(".agregar-comida-wrapper");
const agregarComidaCloseBtn = document.querySelector(".agregar-comida-header i");
const comidaNameInput = document.querySelector(".comida-name");
const comidaTimeFromInput = document.querySelector(".comida-time-from");
const comidaTimeToInput = document.querySelector(".comida-time-to");
const agregarComidaBtn = document.querySelector(".agregar-comida-btn");

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

// Agregar listener al botón de cerrar formulario de agregar comida
agregarComidaCloseBtn.addEventListener("click", () => {
  agregarComidaWrapper.style.display = "none";
});


// Función para agregar una comida
function addComida() {
  const name = comidaNameInput.value.trim();
  const timeFrom = comidaTimeFromInput.value.trim();
  const timeTo = comidaTimeToInput.value.trim();
  const tipo = comidaTipoInput.value;
  const descripcion = comidaDescripcionInput.value.trim();
  const ingredientes = comidaIngredientesInput.value.trim();
  const miembro = comidaMiembroInput.value.trim();
  const extra = comidaExtraInput.value.trim();

  if (name !== "" && timeFrom !== "" && timeTo !== "" && tipo !== "") {
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
    comidaTipoInput.value = "";
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


/* VERSION ANTERIOR
const calendar = document.querySelector(".calendar"),
  date = document.querySelector(".date"),
  daysContainer = document.querySelector(".days"),
  prev = document.querySelector(".prev"),
  next = document.querySelector(".next"),
  todayBtn = document.querySelector(".today-btn"),
  gotoBtn = document.querySelector(".goto-btn"),
  dateInput = document.querySelector(".date-input"),
  eventDay = document.querySelector(".comida-day"),
  eventDate = document.querySelector(".comida-date"),
  eventsContainer = document.querySelector(".comidas"),
  addEventBtn = document.querySelector(".agregar-comida"),
  addEventWrapper = document.querySelector(".agregar-comida-wrapper "),
  addEventCloseBtn = document.querySelector(".close "),
  addEventTitle = document.querySelector(".comida-name "),
  addEventFrom = document.querySelector(".comida-time-from "),
  addEventTo = document.querySelector(".comida-time-to "),
  addEventSubmit = document.querySelector(".agregar-comida-btn ");

let today = new Date();
let activeDay;
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

const eventsArr = [];
getEvents();
console.log(eventsArr);
function initCalendar() {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const prevLastDay = new Date(year, month, 0);
  const prevDays = prevLastDay.getDate();
  const lastDate = lastDay.getDate();
  const day = firstDay.getDay();
  const nextDays = 7 - lastDay.getDay() - 1;

  date.innerHTML = months[month] + " " + year;

  let days = "";

  for (let x = day; x > 0; x--) {
    days += `<div class="day prev-date">${prevDays - x + 1}</div>`;
  }

  for (let i = 1; i <= lastDate; i++) {
    //chequear si la comida es ese dia
    let event = false;
    eventsArr.forEach((eventObj) => {
      if (
        eventObj.day === i &&
        eventObj.month === month + 1 &&
        eventObj.year === year
      ) {
        event = true;
      }
    });
    if (
      i === new Date().getDate() &&
      year === new Date().getFullYear() &&
      month === new Date().getMonth()
    ) {
      activeDay = i;
      getActiveDay(i);
      updateEvents(i);
      if (event) {
        days += `<div class="day today active event">${i}</div>`;
      } else {
        days += `<div class="day today active">${i}</div>`;
      }
    } else {
      if (event) {
        days += `<div class="day event">${i}</div>`;
      } else {
        days += `<div class="day ">${i}</div>`;
      }
    }
  }

  for (let j = 1; j <= nextDays; j++) {
    days += `<div class="day next-date">${j}</div>`;
  }
  daysContainer.innerHTML = days;
  addListner();
}
// adherir mes, año en el pboton previo y proximo 
function prevMonth() {
  month--;
  if (month < 0) {
    month = 11;
    year--;
  }
  initCalendar();
}

function nextMonth() {
  month++;
  if (month > 11) {
    month = 0;
    year++;
  }
  initCalendar();
}

prev.addEventListener("click", prevMonth);
next.addEventListener("click", nextMonth);

initCalendar();

//agregar el active en el dia
function addListner() {
  const days = document.querySelectorAll(".day");
  days.forEach((day) => {
    day.addEventListener("click", (e) => {
      getActiveDay(e.target.innerHTML);
      updateEvents(Number(e.target.innerHTML));
      activeDay = Number(e.target.innerHTML);
      //quitar el avctive
      days.forEach((day) => {
        day.classList.remove("active");
      });
      //si cliqueas prev-date y tal te lleva al mes
      if (e.target.classList.contains("prev-date")) {
        prevMonth();
        //agregar active al cliquear el dia despues de que el mes es cambiado 
        setTimeout(() => {
          //agregar active cuando no hay fecha previa ni post
          const days = document.querySelectorAll(".day");
          days.forEach((day) => {
            if (
              !day.classList.contains("prev-date") &&
              day.innerHTML === e.target.innerHTML
            ) {
              day.classList.add("active");
            }
          });
        }, 100);
      } else if (e.target.classList.contains("next-date")) {
        nextMonth();
        //agregar active al cliquear el dia despues de que el mes es cambiado d
        setTimeout(() => {
          const days = document.querySelectorAll(".day");
          days.forEach((day) => {
            if (
              !day.classList.contains("next-date") &&
              day.innerHTML === e.target.innerHTML
            ) {
              day.classList.add("active");
            }
          });
        }, 100);
      } else {
        e.target.classList.add("active");
      }
    });
  });
}

todayBtn.addEventListener("click", () => {
  today = new Date();
  month = today.getMonth();
  year = today.getFullYear();
  initCalendar();
});

dateInput.addEventListener("input", (e) => {
  dateInput.value = dateInput.value.replace(/[^0-9/]/g, "");
  if (dateInput.value.length === 2) {
    dateInput.value += "/";
  }
  if (dateInput.value.length > 7) {
    dateInput.value = dateInput.value.slice(0, 7);
  }
  if (e.inputType === "deleteContentBackward") {
    if (dateInput.value.length === 3) {
      dateInput.value = dateInput.value.slice(0, 2);
    }
  }
});

gotoBtn.addEventListener("click", gotoDate);

function gotoDate() {
  console.log("here");
  const dateArr = dateInput.value.split("/");
  if (dateArr.length === 2) {
    if (dateArr[0] > 0 && dateArr[0] < 13 && dateArr[1].length === 4) {
      month = dateArr[0] - 1;
      year = dateArr[1];
      initCalendar();
      return;
    }
  }
  alert("Invalid Date");
}

//function get active day day name and date and update eventday eventdate
function getActiveDay(date) {
  const day = new Date(year, month, date);
  const dayName = day.toString().split(" ")[0];
  eventDay.innerHTML = dayName;
  eventDate.innerHTML = date + " " + months[month] + " " + year;
}

//function update events when a day is active
function updateEvents(date) {
  let events = "";
  eventsArr.forEach((event) => {
    if (
      date === event.day &&
      month + 1 === event.month &&
      year === event.year
    ) {
      event.events.forEach((event) => {
        events += `<div class="event">
            <div class="title">
              <i class="fas fa-circle"></i>
              <h3 class="comida-tiulo">${comida.titulo}</h3>
            </div>
            <div class="comida-tiempo">
              <span class="comida-tiempo">${comida.tiempo}</span>
            </div>
        </div>`;
      });
    }
  });
  if (events === "") {
    events = `<div class="no-comida">
            <h3>Sin comidas</h3>
        </div>`;
  }
  eventsContainer.innerHTML = events;
  saveEvents();
}

//Adherir el evento
addEventBtn.addEventListener("click", () => {
  addEventWrapper.classList.toggle("active");
});

addEventCloseBtn.addEventListener("click", () => {
  addEventWrapper.classList.remove("active");
});

document.addEventListener("click", (e) => {
  if (e.target !== addEventBtn && !addEventWrapper.contains(e.target)) {
    addEventWrapper.classList.remove("active");
  }
});

addEventTitle.addEventListener("input", (e) => {
  addEventTitle.value = addEventTitle.value.slice(0, 60);
});

defineProperty();


addEventFrom.addEventListener("input", (e) => {
  addEventFrom.value = addEventFrom.value.replace(/[^0-9:]/g, "");
  if (addEventFrom.value.length === 2) {
    addEventFrom.value += ":";
  }
  if (addEventFrom.value.length > 5) {
    addEventFrom.value = addEventFrom.value.slice(0, 5);
  }
});

addEventTo.addEventListener("input", (e) => {
  addEventTo.value = addEventTo.value.replace(/[^0-9:]/g, "");
  if (addEventTo.value.length === 2) {
    addEventTo.value += ":";
  }
  if (addEventTo.value.length > 5) {
    addEventTo.value = addEventTo.value.slice(0, 5);
  }
});

//Funcion para adeherir la comida
addEventSubmit.addEventListener("click", () => {
  const eventTitle = addEventTitle.value;
  const eventTimeFrom = addEventFrom.value;
  const eventTimeTo = addEventTo.value;
  if (eventTitle === "" || eventTimeFrom === "" || eventTimeTo === "") {
    alert("Por favor coloca todos los espacios");
    return;
  }

  //Correcto formato de 24 hs
  const timeFromArr = eventTimeFrom.split(":");
  const timeToArr = eventTimeTo.split(":");
  if (
    timeFromArr.length !== 2 ||
    timeToArr.length !== 2 ||
    timeFromArr[0] > 23 ||
    timeFromArr[1] > 59 ||
    timeToArr[0] > 23 ||
    timeToArr[1] > 59
  ) {
    alert("Formato invalido");
    return;
  }

  const timeFrom = convertTime(eventTimeFrom);
  const timeTo = convertTime(eventTimeTo);

  //Chequear si esta todo agregado correctamente
  let eventExist = false;
  eventsArr.forEach((event) => {
    if (
      event.day === activeDay &&
      event.month === month + 1 &&
      event.year === year
    ) {
      event.events.forEach((event) => {
        if (event.title === eventTitle) {
          eventExist = true;
        }
      });
    }
  });
  if (eventExist) {
    alert("La comida ya esta agregada");
    return;
  }
  const newEvent = {
    title: eventTitle,
    time: timeFrom + " - " + timeTo,
  };
  console.log(newEvent);
  console.log(activeDay);
  let eventAdded = false;
  if (eventsArr.length > 0) {
    eventsArr.forEach((item) => {
      if (
        item.day === activeDay &&
        item.month === month + 1 &&
        item.year === year
      ) {
        item.events.push(newEvent);
        eventAdded = true;
      }
    });
  }

  if (!eventAdded) {
    eventsArr.push({
      day: activeDay,
      month: month + 1,
      year: year,
      events: [newEvent],
    });
  }

  console.log(eventsArr);
  addEventWrapper.classList.remove("active");
  addEventTitle.value = "";
  addEventFrom.value = "";
  addEventTo.value = "";
  updateEvents(activeDay);
  //seleccionar y agregar
  const activeDayEl = document.querySelector(".day.active");
  if (!activeDayEl.classList.contains("event")) {
    activeDayEl.classList.add("event");
  }
});

//funcion de eliminar al seleccionar
eventsContainer.addEventListener("click", (e) => {
  if (e.target.classList.contains("event")) {
    if (confirm("¿Desea eliminar la comida programada?")) {
      const eventTitle = e.target.children[0].children[1].innerHTML;
      eventsArr.forEach((event) => {
        if (
          event.day === activeDay &&
          event.month === month + 1 &&
          event.year === year
        ) {
          event.events.forEach((item, index) => {
            if (item.title === eventTitle) {
              event.events.splice(index, 1);
            }
          });
          //remover
          if (event.events.length === 0) {
            eventsArr.splice(eventsArr.indexOf(event), 1);
            //rEMOVER LA COMIDA DEL DIA
            const activeDayEl = document.querySelector(".day.active");
            if (activeDayEl.classList.contains("event")) {
              activeDayEl.classList.remove("event");
            }
          }
        }
      });
      updateEvents(activeDay);
    }
  }
});

//Guardar los eventos de forma local
function saveEvents() {
  localStorage.setItem("events", JSON.stringify(eventsArr));
}


function getEvents() {
  //chequeo
  if (localStorage.getItem("events") === null) {
    return;
  }
  eventsArr.push(...JSON.parse(localStorage.getItem("events")));
}

function convertTime(time) {
  //convertir tiempo en 24 horaws
  let timeArr = time.split(":");
  let timeHour = timeArr[0];
  let timeMin = timeArr[1];
  let timeFormat = timeHour >= 12 ? "PM" : "AM";
  timeHour = timeHour % 12 || 12;
  time = timeHour + ":" + timeMin + " " + timeFormat;
  return time;
}
*/